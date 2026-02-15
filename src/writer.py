from __future__ import annotations

import csv
from pathlib import Path

from .parser import ExamItem


def write_results_csv(path: Path, rows: list[tuple[ExamItem, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["原文", "翻译"])
        for item, translation in rows:
            writer.writerow([item.source, translation])
