#!/usr/bin/env python3
"""Create a ControlNet-like image-generation handoff manifest from a spec.

The local ChatGPT image tool may only expose a text prompt in some runtimes,
while API/GUI image generators may accept image inputs. This script makes that
boundary explicit: it packages the final prompt plus the source image, approved
visual guide composite, and optional clay/lineart/depth passes as ordered image
inputs. If a runtime cannot supply those images to image generation, the run
must be treated as blocked/text-only fallback rather than true structure
conditioning.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from validate_illustrate_spec import (
    extract_field,
    extract_image_generation_prompt,
    is_placeholder,
    normalize_text,
    resolve_reference_path,
)


PASS_RE = re.compile(r"\b(clay|lineart|wire|depth|normal|mask)\s*=\s*([^|,\n]+)", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an image_gen conditioning handoff manifest.")
    parser.add_argument("spec_path", type=Path, help="Filled illustrate spec markdown file")
    parser.add_argument("--out", required=True, type=Path, help="Output JSON manifest path")
    parser.add_argument(
        "--prompt-out",
        type=Path,
        help="Optional text file containing the prompt plus ordered image-input instructions.",
    )
    parser.add_argument(
        "--provider",
        default="openai_image_generation",
        help="Provider/runtime label for the manifest.",
    )
    return parser.parse_args()


def field_path(text: str, field: str, spec_path: Path) -> tuple[str, Path | None]:
    raw = extract_field(text, field)
    if not raw or is_placeholder(raw) or raw.strip().lower() == "not_applicable":
        return "", None
    resolved = resolve_reference_path(raw.strip(), spec_path)
    return raw.strip(), resolved


def add_image_input(
    inputs: list[dict[str, Any]],
    *,
    role: str,
    raw_path: str,
    resolved_path: Path | None,
    required: bool,
    purpose: str,
    strength: str,
) -> None:
    if not raw_path:
        if required:
            inputs.append(
                {
                    "role": role,
                    "path": "",
                    "exists": False,
                    "required": True,
                    "purpose": purpose,
                    "conditioning_strength": strength,
                    "error": "missing path in spec",
                }
            )
        return
    inputs.append(
        {
            "role": role,
            "path": raw_path,
            "resolved_path": str(resolved_path) if resolved_path else "",
            "exists": bool(resolved_path and resolved_path.exists()),
            "required": required,
            "purpose": purpose,
            "conditioning_strength": strength,
        }
    )


def parse_pass_outputs(text: str, spec_path: Path) -> list[dict[str, Any]]:
    raw = extract_field(text, "BLENDER_PASS_OUTPUTS") or ""
    outputs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for match in PASS_RE.finditer(raw):
        role = match.group(1).lower()
        if role == "wire":
            role = "lineart"
        if role in seen:
            continue
        seen.add(role)
        raw_path = match.group(2).strip()
        resolved = resolve_reference_path(raw_path, spec_path)
        strength = "strict_structure" if role in {"lineart", "depth", "normal", "mask"} else "medium_structure"
        outputs.append(
            {
                "role": f"blockout_{role}",
                "path": raw_path,
                "resolved_path": str(resolved),
                "exists": resolved.exists(),
                "required": role in {"lineart", "depth"},
                "purpose": f"{role} pass supporting the approved visual guide composite",
                "conditioning_strength": strength,
            }
        )
    return outputs


def build_manifest(spec_path: Path, out_path: Path, provider: str) -> dict[str, Any]:
    text = normalize_text(spec_path)
    prompt = extract_image_generation_prompt(text)
    prompt_source = "FINAL_IMAGE_PROMPT_COMPILED" if prompt == extract_field(text, "FINAL_IMAGE_PROMPT_COMPILED") else "IMAGE_GEN_HANDOFF_PROMPT"

    image_inputs: list[dict[str, Any]] = []

    source_raw = extract_field(text, "SOURCE_IMAGE_REFERENCE") or extract_field(text, "SOURCE_IMAGE_PATH") or ""
    source_resolved = resolve_reference_path(source_raw, spec_path) if source_raw and not is_placeholder(source_raw) else None
    source_conditioning = (extract_field(text, "SOURCE_IMAGE_ACTUAL_CONDITIONING") or "").strip().lower()
    add_image_input(
        image_inputs,
        role="source_image",
        raw_path=source_raw.strip() if source_raw and not is_placeholder(source_raw) else "",
        resolved_path=source_resolved,
        required=source_conditioning == "yes",
        purpose="source/development reference for retained subject identity and composition lineage",
        strength="medium_reference",
    )

    composite_raw, composite_resolved = field_path(text, "VISUAL_GUIDE_COMPOSITE_PATH", spec_path)
    add_image_input(
        image_inputs,
        role="visual_guide_composite",
        raw_path=composite_raw,
        resolved_path=composite_resolved,
        required=True,
        purpose="strict camera, perspective, scale, support/contact, cut/grip, and object-placement structure reference",
        strength="strict_structure",
    )

    image_inputs.extend(parse_pass_outputs(text, spec_path))

    missing_required = [item["role"] for item in image_inputs if item.get("required") and not item.get("exists")]
    pre_composite_evidence_stack = {
        "immutable_user_commands": extract_field(text, "IMMUTABLE_USER_COMMANDS_VERBATIM") or "",
        "source_image_reference": source_raw.strip() if source_raw and not is_placeholder(source_raw) else "",
        "source_image_actual_conditioning": source_conditioning or "not_applicable",
        "object_research_artifact": extract_field(text, "OBJECT_RESEARCH_ARTIFACT_PATH") or "",
        "perspective_transfer": extract_field(text, "PROJECTED_BASELINE_TO_HERO_POSITION") or "",
        "scale_proxy_projection": extract_field(text, "SCALE_PROXY_DUMMY_TO_HERO_PROJECTION") or "",
        "scale_proxy_trace": extract_field(text, "SCALE_PROXY_TRACE_OVERLAY") or "",
        "blender_scene": extract_field(text, "BLENDER_SCENE_PATH") or "",
        "blender_pass_outputs": extract_field(text, "BLENDER_PASS_OUTPUTS") or "",
        "blender_visibility_report": extract_field(text, "BLENDER_VISIBILITY_REPORT_PATH") or "",
        "visual_guide_composite": composite_raw,
        "final_prompt_source": prompt_source,
    }
    manifest = {
        "schema": "illustrate-image-gen-conditioning-manifest.v1",
        "provider": provider,
        "spec_path": str(spec_path.resolve()),
        "prompt_source": prompt_source,
        "prompt": prompt or "",
        "conditioning_mode": extract_field(text, "IMAGE_GEN_STRUCTURE_CONDITIONING_MODE")
        or "openai_high_fidelity_image_inputs",
        "input_fidelity": "high",
        "structure_strength": extract_field(text, "IMAGE_GEN_STRUCTURE_CONDITIONING_STRENGTH")
        or "strict_structure",
        "controlnet_equivalence": (
            "ControlNet-like handoff via ordered high-fidelity image inputs. "
            "This is not pixel-perfect ControlNet unless the selected provider explicitly supports ControlNet/depth/lineart controls."
        ),
        "pre_composite_evidence_stack": pre_composite_evidence_stack,
        "composite_role": (
            "The visual guide composite is one strong structure reference in the handoff stack. "
            "It does not replace immutable user commands, source-image conditioning, object research, perspective math, "
            "scale-proxy projection, Blender passes, visibility review, or the compiled final prompt. "
            "For scale specifically, the approved composite's markers, baselines, footpoints, and scale-proxy trace are binding."
        ),
        "image_inputs": image_inputs,
        "missing_required_inputs": missing_required,
        "tool_instruction": (
            "Generate/edit with the prompt, ALL existing image_inputs, and the pre_composite_evidence_stack. "
            "Treat visual_guide_composite as a strict structure reference for camera, perspective, scale, support/contact, "
            "and object placement, but not as the sole authority. SCALE MUST FOLLOW THE APPROVED COMPOSITE: protagonist/object sizes, "
            "footpoints, door/passenger/container ratios, and screen occupancy must obey the composite overlays; if style/action/beauty wording conflicts, composite scale wins. "
            "Preserve source/user/object/perspective/blockout/final-prompt locks. "
            "Use high input fidelity where supported. Do not copy guide labels, arrows, gray clay material, measurement text, "
            "or the temporary scale dummy into the final art. "
            "If the runtime cannot attach image inputs, do not generate; report blocked_text_only."
        ),
        "post_image_required": True,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def write_prompt_file(manifest: dict[str, Any], prompt_out: Path) -> None:
    lines = [
        "# Image generation handoff",
        "",
        "Use the prompt below with the ordered image inputs in the manifest.",
        "If image inputs cannot be attached, stop: this is blocked_text_only, not true conditioning.",
        "",
        "## Ordered image inputs",
    ]
    for idx, item in enumerate(manifest.get("image_inputs", []), start=1):
        lines.append(
            f"{idx}. {item.get('role')}: {item.get('path')} "
            f"[exists={item.get('exists')}, strength={item.get('conditioning_strength')}]"
        )
    lines.extend(["", "## Prompt", manifest.get("prompt", "")])
    prompt_out.parent.mkdir(parents=True, exist_ok=True)
    prompt_out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    manifest = build_manifest(args.spec_path, args.out, args.provider)
    if args.prompt_out:
        write_prompt_file(manifest, args.prompt_out)
    missing = manifest.get("missing_required_inputs", [])
    if missing:
        print(f"IMAGE_GEN HANDOFF BLOCKED: missing required image inputs: {', '.join(missing)}")
        print(f"Manifest written for repair: {args.out}")
        return 1
    print(f"Created image_gen conditioning handoff package: {args.out}")
    if args.prompt_out:
        print(f"Created handoff prompt file: {args.prompt_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
