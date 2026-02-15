from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

VALID_TASKS = {"zh_en", "en_zh"}


@dataclass(slots=True)
class ExamItem:
    source: str
    line_no: int


@dataclass(slots=True)
class ParseResult:
    tasks: dict[str, list[ExamItem]]


def parse_exam(path: Path) -> ParseResult:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    tasks: dict[str, list[ExamItem]] = {"zh_en": [], "en_zh": []}
    inside_exam = False
    seen_exam_start = False
    seen_exam_end = False
    current_task: str | None = None

    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            stripped = raw.strip()

            if stripped == "<exam>":
                inside_exam = True
                seen_exam_start = True
                current_task = None
                continue

            if stripped == "</exam>":
                inside_exam = False
                seen_exam_end = True
                current_task = None
                break

            if not inside_exam:
                continue

            if stripped in {"<zh_en>", "<en_zh>"}:
                current_task = stripped[1:-1]
                continue

            if stripped in {"</zh_en>", "</en_zh>"}:
                current_task = None
                continue

            if current_task is None:
                continue

            if not stripped or stripped.startswith("#"):
                continue

            tasks[current_task].append(ExamItem(source=stripped, line_no=line_no))

    if inside_exam or (seen_exam_start and not seen_exam_end):
        raise ValueError("Malformed exam.txt: missing </exam>")
    if not seen_exam_start:
        raise ValueError("Malformed exam.txt: missing <exam> container")

    return ParseResult(tasks=tasks)
