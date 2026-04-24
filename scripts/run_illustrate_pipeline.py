#!/usr/bin/env python3
"""Final gate for validated illustrate-skill specs before image-generation handoff."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validate_illustrate_spec import (
    extract_field,
    is_placeholder,
    lower_value,
    print_results,
    validate_spec_path,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the final illustrate pipeline gate.")
    parser.add_argument("spec_path", type=Path, help="Path to the filled illustrate spec markdown file")
    parser.add_argument(
        "--strict-object-research",
        action="store_true",
        help="Pass through strict object-research enforcement to the validator.",
    )
    parser.add_argument(
        "--emit-image-prompt",
        type=Path,
        help="Optional path to write the final IMAGE_GEN_HANDOFF_PROMPT after all checks pass.",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the final IMAGE_GEN_HANDOFF_PROMPT to stdout after all checks pass.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate_spec_path(args.spec_path, strict_object_research=args.strict_object_research)
    print_results(result.errors, result.warnings)
    if result.errors:
        return 1

    image_ready = lower_value(extract_field(result.text, "IMAGE_GEN_READY"))
    if image_ready != "yes":
        print("PIPELINE BLOCKED")
        print("- ERROR: IMAGE_GEN_READY must be 'yes' before final image-generation handoff.")
        return 1

    prompt = extract_field(result.text, "IMAGE_GEN_HANDOFF_PROMPT")
    if is_placeholder(prompt):
        print("PIPELINE BLOCKED")
        print("- ERROR: IMAGE_GEN_HANDOFF_PROMPT is missing or still a placeholder.")
        return 1

    if args.emit_image_prompt:
        args.emit_image_prompt.parent.mkdir(parents=True, exist_ok=True)
        args.emit_image_prompt.write_text((prompt or "") + "\n", encoding="utf-8")

    if args.print_prompt:
        print("IMAGE_GEN_HANDOFF_PROMPT")
        print(prompt)

    print("PIPELINE READY")
    print(f"- Spec: {args.spec_path.resolve()}")
    if args.emit_image_prompt:
        print(f"- Prompt file: {args.emit_image_prompt.resolve()}")
    print("- Status: Safe to hand off to image generation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
