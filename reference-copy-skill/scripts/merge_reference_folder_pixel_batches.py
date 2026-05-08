#!/usr/bin/env python3
"""Merge pixel-plane batch JSON reports into one folder-level report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from measure_reference_folder_pixels import kmeans_palette, markdown, stat, top_quantized  # noqa: E402


def weighted_palette_pixels(images: list[dict[str, object]], scale: int = 18) -> list[tuple[int, int, int]]:
    pixels: list[tuple[int, int, int]] = []
    for report in images:
        palette = report["global"].get("palette", [])
        for item in palette:
            rgb = tuple(int(v) for v in item["rgb"])
            repeats = max(1, int(round(float(item["pct"]) * scale)))
            pixels.extend([rgb] * repeats)
    return pixels


def aggregate_from_images(images: list[dict[str, object]], palette_pixels: list[tuple[int, int, int]]) -> dict[str, object]:
    metric_names = [
        "luma_p10",
        "luma_p50",
        "luma_p90",
        "mean_saturation",
        "clipped_bloom_pct",
        "highlight_plane_pct_luma_ge_215",
        "light_mid_plane_pct_luma_160_215",
        "mid_shadow_plane_pct_luma_95_160",
        "dark_anchor_pct_luma_le_65",
        "warm_bright_pct",
        "cool_shadow_pct",
    ]
    metric_stats = {}
    for name in metric_names:
        metric_stats[name] = stat(float(report["global"][name]) for report in images)
    metric_stats["edge_density_pct"] = stat(
        float(report["global"]["edge"]["edge_density_pct"]) for report in images
    )
    grid_summary = {}
    for cell in [f"r{gy}c{gx}" for gy in range(1, 4) for gx in range(1, 4)]:
        grid_summary[cell] = {
            "luma_p50": stat(float(report["grid"][cell]["luma_p50"]) for report in images),
            "clipped_bloom_pct": stat(float(report["grid"][cell]["clipped_bloom_pct"]) for report in images),
            "dark_anchor_pct": stat(float(report["grid"][cell]["dark_anchor_pct_luma_le_65"]) for report in images),
            "edge_density_pct": stat(float(report["grid"][cell]["edge"]["edge_density_pct"]) for report in images),
        }
    return {
        "image_count": len(images),
        "metric_stats": metric_stats,
        "palette": kmeans_palette(palette_pixels, k=14, rounds=12, max_points=36_000),
        "top_quantized": top_quantized(palette_pixels, limit=18),
        "grid_summary": grid_summary,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge folder pixel-plane batch reports.")
    parser.add_argument("batch_json", type=Path, nargs="+", help="Batch JSON files")
    parser.add_argument("--out-md", type=Path, required=True, help="Merged Markdown report path")
    parser.add_argument("--out-json", type=Path, required=True, help="Merged JSON report path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    images: list[dict[str, object]] = []
    failures: list[str] = []
    source_dir = ""
    image_count_seen = 0
    for path in args.batch_json:
        data = json.loads(path.read_text(encoding="utf-8"))
        source_dir = source_dir or data.get("source_dir", "")
        image_count_seen = max(image_count_seen, int(data.get("image_count_seen", 0)))
        images.extend(data.get("images", []))
        failures.extend(data.get("failures", []))
    images.sort(key=lambda item: item["relative_path"])
    palette_pixels = weighted_palette_pixels(images)
    merged = {
        "source_dir": source_dir,
        "image_count_seen": image_count_seen,
        "failures": failures,
        "aggregate": aggregate_from_images(images, palette_pixels),
        "images": images,
        "merge_note": "Palette clusters are weighted approximations from per-image palette clusters; plane and edge metrics are exact per-image summaries from the batch analyses.",
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    args.out_md.write_text(markdown(merged), encoding="utf-8")
    print(args.out_md)
    print(args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
