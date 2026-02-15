from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from time import perf_counter

from loguru import logger
from tqdm import tqdm

from .config import ensure_dirs, load_config
from .parser import ExamItem, parse_exam
from .translator import Translator
from .writer import write_results_csv


VALID_TASKS = {"zh_en", "en_zh"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM translation benchmark runner")
    parser.add_argument("--input", default="exam.txt", help="Input exam file path")
    parser.add_argument("--outdir", default="outputs", help="Output directory")
    parser.add_argument("--tasks", default="zh_en,en_zh", help="Comma separated tasks: zh_en,en_zh")
    parser.add_argument(
        "--continue_on_error",
        default="true",
        choices=["true", "false"],
        help="Continue when one item fails",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of concurrent worker threads",
    )
    return parser.parse_args()


def parse_selected_tasks(raw: str) -> list[str]:
    tasks = [token.strip() for token in raw.split(",") if token.strip()]
    for task in tasks:
        if task not in VALID_TASKS:
            raise ValueError(f"Unsupported task: {task}")
    return tasks


def configure_logger(logs_dir: Path) -> Path:
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = logs_dir / f"run_{ts}.log"
    logger.add(log_path, level="INFO", encoding="utf-8")
    return log_path


def translate_task(
    task: str,
    items: list[ExamItem],
    translator: Translator,
    continue_on_error: bool,
    workers: int,
) -> tuple[list[tuple[ExamItem, str]], int, int]:
    if not items:
        return [], 0, 0

    rows: list[tuple[ExamItem, str]] = [(item, "") for item in items]
    success_count = 0
    fail_count = 0

    executor = ThreadPoolExecutor(max_workers=workers)
    futures = {executor.submit(translator.translate, task, item.source): idx for idx, item in enumerate(items)}

    try:
        with tqdm(total=len(items), desc=f"Translating {task}", unit="line") as pbar:
            for future in as_completed(futures):
                idx = futures[future]
                item = items[idx]
                result = future.result()
                if result.error is not None:
                    fail_count += 1
                    rows[idx] = (item, "")
                    logger.opt(exception=result.error).error(
                        "Translate failed task={} line={} source='{}'",
                        task,
                        item.line_no,
                        item.source[:120],
                    )
                    if not continue_on_error:
                        for pending in futures:
                            pending.cancel()
                        raise result.error
                else:
                    success_count += 1
                    rows[idx] = (item, result.text)
                pbar.update(1)
    finally:
        executor.shutdown(wait=True, cancel_futures=False)

    return rows, success_count, fail_count


def run() -> int:
    args = parse_args()
    base_dir = Path.cwd()

    continue_on_error = args.continue_on_error.lower() == "true"
    config = load_config(continue_on_error=continue_on_error, workers=args.workers)

    logs_dir, output_dir = ensure_dirs(base_dir, args.outdir)
    log_path = configure_logger(logs_dir)

    selected_tasks = parse_selected_tasks(args.tasks)
    input_path = base_dir / args.input

    logger.info("Starting translation benchmark")
    logger.info(
        "Config model={}, input={}, outdir={}, tasks={}, workers={}, continue_on_error={}",
        config.model_name,
        input_path,
        output_dir,
        selected_tasks,
        config.workers,
        config.continue_on_error,
    )

    parsed = parse_exam(input_path)
    for task in selected_tasks:
        logger.info("Parsed {} items for {}", len(parsed.tasks[task]), task)

    translator = Translator(config)

    start = perf_counter()
    total_success = 0
    total_failed = 0

    for task in selected_tasks:
        items = parsed.tasks[task]
        rows, success_count, fail_count = translate_task(
            task=task,
            items=items,
            translator=translator,
            continue_on_error=config.continue_on_error,
            workers=config.workers,
        )
        total_success += success_count
        total_failed += fail_count

        output_path = output_dir / f"result_{task}.csv"
        write_results_csv(output_path, rows)
        logger.info("Wrote {} rows to {}", len(rows), output_path)

    elapsed = perf_counter() - start
    logger.info(
        "Finished. success={}, failed={}, elapsed={:.2f}s, log_file={}",
        total_success,
        total_failed,
        elapsed,
        log_path,
    )
    return 0


def main() -> None:
    try:
        raise SystemExit(run())
    except Exception as exc:  # noqa: BLE001
        logger.exception("Run failed: {}", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
