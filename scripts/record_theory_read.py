#!/usr/bin/env python3
"""Record theory-read evidence for illustrate-skill runs."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys


STEP_FIELD_MAP = {
    "step1": "STEP_1_FILES_READ",
    "step2": "STEP_2_FILES_READ",
    "step3": "STEP_3_FILES_READ",
    "step4": "STEP_4_FILES_READ",
    "step5": "STEP_5_FILES_READ",
    "step6": "STEP_6_FILES_READ",
    "step7": "STEP_7_FILES_READ",
    "step8": "STEP_8_FILES_READ",
    "style-guide": "STYLE_GUIDE_FILES_READ",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record theory-file reads in a proof artifact.")
    parser.add_argument("proof_path", type=Path, help="Path to the theory-read-proof markdown file")
    parser.add_argument(
        "step",
        choices=sorted(STEP_FIELD_MAP.keys()),
        help="Which step's theory field to update (or style-guide).",
    )
    parser.add_argument("files", nargs="+", help="One or more theory file paths to record")
    parser.add_argument("--mark-ready", action="store_true", help="Also set PROOF_READY to yes.")
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def get_field(text: str, field_name: str) -> str:
    prefix = f"{field_name}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    raise ValueError(f"Missing field: {field_name}")


def set_field(text: str, field_name: str, value: str) -> str:
    prefix = f"{field_name}:"
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = f"{prefix} {value}".rstrip()
            break
    else:
        raise ValueError(f"Missing field: {field_name}")
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def normalize_entries(raw_value: str) -> list[str]:
    if not raw_value:
        return []
    parts = [part.strip() for part in raw_value.split(" | ")]
    return [part for part in parts if part]


def merge_entries(existing: list[str], new_entries: list[str]) -> list[str]:
    seen = set(existing)
    merged = list(existing)
    for entry in new_entries:
        if entry not in seen:
            merged.append(entry)
            seen.add(entry)
    return merged


def append_event(text: str, message: str) -> str:
    current = get_field(text, "READ_EVENTS")
    current_entries = normalize_entries(current)
    current_entries.append(message)
    return set_field(text, "READ_EVENTS", " | ".join(current_entries))


def main() -> int:
    args = parse_args()
    proof_path = args.proof_path
    if not proof_path.exists():
        print(f"ERROR: proof file not found: {proof_path}")
        return 1

    text = read_text(proof_path)
    field_name = STEP_FIELD_MAP[args.step]
    current = normalize_entries(get_field(text, field_name))
    merged = merge_entries(current, args.files)
    text = set_field(text, field_name, " | ".join(merged))

    timestamp = datetime.now(timezone.utc).isoformat()
    event_message = f"{timestamp} :: {args.step} :: {' ; '.join(args.files)}"
    text = append_event(text, event_message)

    if args.mark_ready:
        text = set_field(text, "PROOF_READY", "yes")

    proof_path.write_text(text, encoding="utf-8")
    print(f"Recorded theory-read proof for {args.step} in {proof_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
