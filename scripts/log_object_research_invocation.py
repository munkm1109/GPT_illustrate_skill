#!/usr/bin/env python3
"""Record object-research invocation evidence for illustrate-skill handoffs."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys


FIELDS = [
    "PARENT_SPEC_PATH",
    "PARENT_OBJECT_ARTIFACT_PATH",
    "MODE",
    "SCENE_INTENT",
    "SCENE_TYPE",
    "STYLE_MODE",
    "PRIORITY",
    "REQUIRED_OBJECTS",
    "LOOKUP_FIRST",
    "LOCAL_LIBRARY_CHECK",
    "WEB_RESEARCH_USED",
    "OUTPUT_ARTIFACT_PATH",
    "RETURN_SHAPE",
    "INVOCATION_EVENTS",
    "INVOCATION_READY",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record object-research invocation evidence.")
    parser.add_argument("log_path", type=Path, help="Path to the invocation log markdown file")
    parser.add_argument("--parent-spec", required=True, help="Parent illustrate spec path")
    parser.add_argument("--parent-artifact", required=True, help="Parent object-research artifact path")
    parser.add_argument("--mode", required=True, help="Object-research mode used")
    parser.add_argument("--scene-intent", required=True, help="Scene intent summary")
    parser.add_argument("--scene-type", required=True, help="Scene type")
    parser.add_argument("--style-mode", required=True, help="Style mode")
    parser.add_argument("--priority", required=True, help="Priority label")
    parser.add_argument("--required-objects", required=True, help="Required objects summary")
    parser.add_argument("--lookup-first", choices=["yes", "no"], required=True, help="Whether local lookup happened first")
    parser.add_argument("--local-library-check", required=True, help="Summary of local library lookup result")
    parser.add_argument("--web-research-used", choices=["yes", "no"], required=True, help="Whether web research was used")
    parser.add_argument("--output-artifact", required=True, help="Object-research artifact path produced by the call")
    parser.add_argument("--return-shape", required=True, help="Returned shape summary")
    parser.add_argument("--mark-ready", action="store_true", help="Set INVOCATION_READY to yes")
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
    return [part.strip() for part in raw_value.split(" | ") if part.strip()]


def append_event(text: str, message: str) -> str:
    current = normalize_entries(get_field(text, "INVOCATION_EVENTS"))
    current.append(message)
    return set_field(text, "INVOCATION_EVENTS", " | ".join(current))


def main() -> int:
    args = parse_args()
    log_path = args.log_path
    if not log_path.exists():
        print(f"ERROR: invocation log file not found: {log_path}")
        return 1

    text = read_text(log_path)
    updates = {
        "PARENT_SPEC_PATH": args.parent_spec,
        "PARENT_OBJECT_ARTIFACT_PATH": args.parent_artifact,
        "MODE": args.mode,
        "SCENE_INTENT": args.scene_intent,
        "SCENE_TYPE": args.scene_type,
        "STYLE_MODE": args.style_mode,
        "PRIORITY": args.priority,
        "REQUIRED_OBJECTS": args.required_objects,
        "LOOKUP_FIRST": args.lookup_first,
        "LOCAL_LIBRARY_CHECK": args.local_library_check,
        "WEB_RESEARCH_USED": args.web_research_used,
        "OUTPUT_ARTIFACT_PATH": args.output_artifact,
        "RETURN_SHAPE": args.return_shape,
    }
    for field_name, value in updates.items():
        text = set_field(text, field_name, value)

    timestamp = datetime.now(timezone.utc).isoformat()
    event = f"{timestamp} :: mode={args.mode} :: lookup_first={args.lookup_first} :: output={args.output_artifact}"
    text = append_event(text, event)

    if args.mark_ready:
        text = set_field(text, "INVOCATION_READY", "yes")

    log_path.write_text(text, encoding="utf-8")
    print(f"Recorded object-research invocation in {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
