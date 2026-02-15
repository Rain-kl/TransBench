from __future__ import annotations

import argparse
import random
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
TASK_SEED_OFFSETS = {"zh_en": 11, "en_zh": 29}


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
    parser.add_argument("--zh_en_limit", type=int, default=None, help="Random sample size for zh_en; -1 for unlimited")
    parser.add_argument("--en_zh_limit", type=int, default=None, help="Random sample size for en_zh; -1 for unlimited")
    parser.add_argument("--random_seed", type=int, default=None, help="Random seed for sampling")
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


def sample_items(task: str, items: list[ExamItem], limit: int, random_seed: int) -> list[ExamItem]:
    if limit == -1 or limit >= len(items):
        return items
    if limit == 0:
        return []

    rng = random.Random(random_seed + TASK_SEED_OFFSETS[task])
    sampled_indexes = sorted(rng.sample(range(len(items)), limit))
    return [items[idx] for idx in sampled_indexes]


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
    config = load_config(
        continue_on_error=continue_on_error,
        workers=args.workers,
        zh_en_limit=args.zh_en_limit,
        en_zh_limit=args.en_zh_limit,
        random_seed=args.random_seed,
    )

    logs_dir, output_dir = ensure_dirs(base_dir, args.outdir)
    log_path = configure_logger(logs_dir)

    selected_tasks = parse_selected_tasks(args.tasks)
    input_path = base_dir / args.input

    logger.info("Starting translation benchmark")
    logger.info(
        "Config model={}, input={}, outdir={}, tasks={}, workers={}, limits={{'zh_en': {}, 'en_zh': {}}}, seed={}, continue_on_error={}",
        config.model_name,
        input_path,
        output_dir,
        selected_tasks,
        config.workers,
        config.zh_en_limit,
        config.en_zh_limit,
        config.random_seed,
        config.continue_on_error,
    )

    parsed = parse_exam(input_path)
    for task in selected_tasks:
        logger.info("Parsed {} items for {}", len(parsed.tasks[task]), task)

    translator = Translator(config)

    start = perf_counter()
    total_success = 0
    total_failed = 0
    combined_rows: list[tuple[ExamItem, str]] = []

    for task in selected_tasks:
        raw_items = parsed.tasks[task]
        task_limit = config.zh_en_limit if task == "zh_en" else config.en_zh_limit
        items = sample_items(task=task, items=raw_items, limit=task_limit, random_seed=config.random_seed)
        logger.info("Task {} selected {}/{} items", task, len(items), len(raw_items))
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
        combined_rows.extend(rows)

    combine_output_path = output_dir / "result_combine.csv"
    write_results_csv(combine_output_path, combined_rows)
    logger.info("Wrote {} rows to {}", len(combined_rows), combine_output_path)

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
