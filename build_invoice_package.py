#!/usr/bin/env python3
"""Validate invoice CSVs and publish a text-only downloadable CSV artifact."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"
COMBINED = ROOT / "owner_distribution_statement_76051_combined.csv"
DOWNLOADABLE = DIST_DIR / "owner_distribution_statement_76051_downloadable.csv"
VALIDATION_REPORT = ROOT / "validation_report.txt"


def _validate_csv(path: Path) -> tuple[int, int, list[tuple[int, int]]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        raise ValueError(f"{path.name} is empty")

    expected_cols = len(rows[0])
    bad_rows: list[tuple[int, int]] = []
    for i, row in enumerate(rows, start=1):
        if len(row) != expected_cols:
            bad_rows.append((i, len(row)))

    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line and not (line.startswith('"') and line.endswith('"')):
            raise ValueError(
                f"{path.name} line {i} does not appear to use RFC4180 quote-all style"
            )

    return len(rows), expected_cols, bad_rows


def build() -> None:
    if not COMBINED.exists():
        raise FileNotFoundError(f"Missing required file: {COMBINED.name}")

    DIST_DIR.mkdir(exist_ok=True)

    rows, cols, bad_rows = _validate_csv(COMBINED)
    DOWNLOADABLE.write_bytes(COMBINED.read_bytes())

    lines = [
        "CSV Validation Report",
        "=====================",
        "",
        f"File: {COMBINED.name}",
        f"- Expected columns: {cols}",
        f"- Parsed rows: {rows}",
    ]
    if bad_rows:
        lines.append("- Rows that did not parse cleanly:")
        lines.extend([f"  - Row {idx}: {count} columns" for idx, count in bad_rows])
    else:
        lines.append("- Rows that did not parse cleanly: none")
    lines.extend(["", f"Downloadable CSV: {DOWNLOADABLE}"])
    VALIDATION_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Invoice CSV validated and published.")
    print(f"- {COMBINED.name}: {rows} rows, {cols} columns")
    print(f"- Downloadable CSV: {DOWNLOADABLE}")
    print(f"- Validation report: {VALIDATION_REPORT}")


if __name__ == "__main__":
    build()
