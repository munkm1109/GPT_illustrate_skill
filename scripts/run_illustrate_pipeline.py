#!/usr/bin/env python3
"""Final gate for validated illustrate-skill specs before image-generation handoff."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from validate_illustrate_spec import (
    extract_image_generation_prompt,
    extract_field,
    is_pre_image_handoff_ready,
    is_post_image_verdict_required,
    is_placeholder,
    lower_value,
    parse_visual_verdict_json,
    print_results,
    validate_spec_path,
)
from create_image_gen_handoff_package import build_manifest, write_prompt_file


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
        help="Optional path to write the final compiled image prompt after all checks pass.",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the final compiled image prompt to stdout after all checks pass.",
    )
    parser.add_argument(
        "--stream-safe",
        action="store_true",
        help=(
            "Keep stdout short for fragile chat/API streams. Full validation details "
            "and the selected prompt are written to --log-file instead of stdout."
        ),
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help=(
            "Optional pipeline log path. With --stream-safe, defaults to "
            "<spec-stem>-pipeline.log beside the spec."
        ),
    )
    parser.add_argument(
        "--emit-conditioning-manifest",
        type=Path,
        help="Optional path to write an image_gen conditioning manifest with source/composite/pass image inputs.",
    )
    parser.add_argument(
        "--emit-conditioning-prompt",
        type=Path,
        help="Optional path to write a human-readable handoff prompt with ordered image inputs.",
    )
    return parser.parse_args()


def select_pipeline_prompt(text: str) -> tuple[str | None, str]:
    """Choose the prompt that is allowed to advance from the current spec.

    A pre-generation spec emits FINAL_IMAGE_PROMPT_COMPILED when present, with
    IMAGE_GEN_HANDOFF_PROMPT retained as a legacy fallback. Once a generated
    image has failed POST_IMAGE_VISUAL_VERDICT, the next handoff must use the
    compiled POST_IMAGE_NEXT_DRAFT_PROMPT so the same failed prompt is not rerun.
    """
    if is_post_image_verdict_required(text) and lower_value(extract_field(text, "POST_IMAGE_ACCEPTED")) == "no":
        verdict, _ = parse_visual_verdict_json(text)
        if verdict and verdict.get("rerender_required") is True:
            return extract_field(text, "POST_IMAGE_NEXT_DRAFT_PROMPT"), "POST_IMAGE_NEXT_DRAFT_PROMPT"
    prompt = extract_image_generation_prompt(text)
    if prompt == extract_field(text, "FINAL_IMAGE_PROMPT_COMPILED"):
        return prompt, "FINAL_IMAGE_PROMPT_COMPILED"
    return prompt, "IMAGE_GEN_HANDOFF_PROMPT"


def stream_log_path(args: argparse.Namespace) -> Path | None:
    if args.log_file:
        return args.log_file
    if args.stream_safe:
        return args.spec_path.with_name(f"{args.spec_path.stem}-pipeline.log")
    return None


def print_validation_results(errors: Sequence[str], warnings: Sequence[str], *, stream_safe: bool) -> None:
    if not stream_safe:
        print_results(list(errors), list(warnings))
        return

    if errors:
        print("VALIDATION FAILED")
        print(f"- Errors: {len(errors)}")
        preview_count = min(5, len(errors))
        for item in list(errors)[:preview_count]:
            print(f"- ERROR: {item}")
        if len(errors) > preview_count:
            print(f"- More errors suppressed: {len(errors) - preview_count}")
    else:
        print("VALIDATION PASSED")
    if warnings:
        print(f"- Warnings: {len(warnings)} (suppressed from stream-safe stdout)")


def write_pipeline_log(
    log_path: Path | None,
    *,
    spec_path: Path,
    errors: Sequence[str],
    warnings: Sequence[str],
    prompt: str | None = None,
    prompt_source: str | None = None,
    status: str | None = None,
) -> None:
    if log_path is None:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Illustrate Pipeline Log",
        f"SPEC_PATH: {spec_path.resolve()}",
        f"STATUS: {status or 'unknown'}",
        f"ERROR_COUNT: {len(errors)}",
        f"WARNING_COUNT: {len(warnings)}",
        "",
        "## Errors",
    ]
    lines.extend(f"- {item}" for item in errors)
    if not errors:
        lines.append("- none")
    lines.append("")
    lines.append("## Warnings")
    lines.extend(f"- {item}" for item in warnings)
    if not warnings:
        lines.append("- none")
    if prompt_source or prompt:
        lines.extend(["", "## Selected Prompt", f"PROMPT_SOURCE: {prompt_source or 'unknown'}", prompt or ""])
    log_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    log_path = stream_log_path(args)
    result = validate_spec_path(args.spec_path, strict_object_research=args.strict_object_research)
    print_validation_results(result.errors, result.warnings, stream_safe=args.stream_safe)
    if result.errors:
        write_pipeline_log(
            log_path,
            spec_path=args.spec_path,
            errors=result.errors,
            warnings=result.warnings,
            status="validation_failed",
        )
        if args.stream_safe and log_path:
            print(f"- Full log: {log_path.resolve()}")
        return 1

    if not is_pre_image_handoff_ready(result.text):
        print("PIPELINE BLOCKED")
        print("- ERROR: PRE_IMAGE_HANDOFF_READY must be 'yes' before final image-generation handoff.")
        write_pipeline_log(
            log_path,
            spec_path=args.spec_path,
            errors=["PRE_IMAGE_HANDOFF_READY must be 'yes' before final image-generation handoff."],
            warnings=result.warnings,
            status="blocked_pre_image_handoff_not_ready",
        )
        if args.stream_safe and log_path:
            print(f"- Full log: {log_path.resolve()}")
        return 1

    prompt, prompt_source = select_pipeline_prompt(result.text)
    if is_placeholder(prompt):
        print("PIPELINE BLOCKED")
        print(f"- ERROR: {prompt_source} is missing or still a placeholder.")
        write_pipeline_log(
            log_path,
            spec_path=args.spec_path,
            errors=[f"{prompt_source} is missing or still a placeholder."],
            warnings=result.warnings,
            status="blocked_missing_prompt",
        )
        if args.stream_safe and log_path:
            print(f"- Full log: {log_path.resolve()}")
        return 1

    if args.emit_image_prompt:
        args.emit_image_prompt.parent.mkdir(parents=True, exist_ok=True)
        args.emit_image_prompt.write_text((prompt or "") + "\n", encoding="utf-8")

    if args.emit_conditioning_manifest:
        manifest = build_manifest(args.spec_path, args.emit_conditioning_manifest, "openai_image_generation")
        missing_inputs = manifest.get("missing_required_inputs", [])
        if args.emit_conditioning_prompt:
            write_prompt_file(manifest, args.emit_conditioning_prompt)
        if missing_inputs:
            print("PIPELINE BLOCKED")
            print("- ERROR: Missing required image conditioning inputs: " + ", ".join(missing_inputs))
            write_pipeline_log(
                log_path,
                spec_path=args.spec_path,
                errors=["Missing required image conditioning inputs: " + ", ".join(missing_inputs)],
                warnings=result.warnings,
                prompt=prompt,
                prompt_source=prompt_source,
                status="blocked_missing_conditioning_inputs",
            )
            if args.stream_safe and log_path:
                print(f"- Full log: {log_path.resolve()}")
            return 1

    write_pipeline_log(
        log_path,
        spec_path=args.spec_path,
        errors=result.errors,
        warnings=result.warnings,
        prompt=prompt,
        prompt_source=prompt_source,
        status="ready",
    )

    if args.print_prompt and not args.stream_safe:
        print(prompt_source)
        print(prompt)
    elif args.print_prompt and args.stream_safe:
        print(f"- Prompt suppressed from stdout by --stream-safe ({len(prompt or '')} chars).")

    print("PIPELINE READY")
    print(f"- Spec: {args.spec_path.resolve()}")
    if args.stream_safe and log_path:
        print(f"- Full log: {log_path.resolve()}")
    if args.emit_image_prompt:
        print(f"- Prompt file: {args.emit_image_prompt.resolve()}")
    if args.emit_conditioning_manifest:
        print(f"- Conditioning manifest: {args.emit_conditioning_manifest.resolve()}")
    if args.emit_conditioning_prompt:
        print(f"- Conditioning prompt file: {args.emit_conditioning_prompt.resolve()}")
    print(f"- Prompt source: {prompt_source}")
    if is_post_image_verdict_required(result.text):
        accepted = lower_value(extract_field(result.text, "POST_IMAGE_ACCEPTED"))
        if accepted == "yes":
            print("- Status: Generated image has a passing post-image verdict and may be accepted.")
        else:
            print("- Status: Safe to hand off to repaired draft image generation; previous output is not accepted.")
    else:
        print("- Status: Safe to hand off to draft image generation. The generated image is not accepted until POST_IMAGE_VISUAL_VERDICT passes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
