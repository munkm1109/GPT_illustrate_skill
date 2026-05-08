#!/usr/bin/env python3
"""Measure full-resolution folder-level pixel-plane signals for reference sets.

The report is designed for illustration wrappers: it measures value planes,
palette clusters, bloom/dark-anchor proportions, edge behavior, and coarse
3x3 composition regions across an entire reference folder.

Images are not resized by default. Expensive operations use deterministic
stride sampling over the original pixel coordinate plane, so the analysis keeps
the source resolution geometry without forcing all pixels into memory.
"""

from __future__ import annotations

import argparse
import colorsys
import json
import math
import warnings
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Iterable

from PIL import Image, ImageOps

warnings.filterwarnings(
    "ignore",
    message="Image.Image.getdata is deprecated.*",
    category=DeprecationWarning,
)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def srgb_luma(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def hue_sat(rgb: tuple[int, int, int]) -> tuple[float, float]:
    r, g, b = [v / 255 for v in rgb]
    h, s, _ = colorsys.rgb_to_hsv(r, g, b)
    return h * 360, s


def hex_color(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def quantize(rgb: tuple[int, int, int], step: int = 16) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(round(v / step) * step))) for v in rgb)


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * p))))
    return ordered[index]


def sample_pixels(image: Image.Image, max_pixels: int = 120_000) -> list[tuple[int, int, int]]:
    total = image.size[0] * image.size[1]
    data = image.getdata()
    if total <= max_pixels:
        return list(data)
    stride = max(1, total // max_pixels)
    return [data[index] for index in range(0, total, stride)][:max_pixels]


def top_quantized(pixels: list[tuple[int, int, int]], limit: int = 12) -> list[dict[str, object]]:
    total = len(pixels) or 1
    counts = Counter(quantize(px) for px in pixels)
    return [
        {"hex": hex_color(rgb), "rgb": rgb, "pct": round(count / total * 100, 2)}
        for rgb, count in counts.most_common(limit)
    ]


def kmeans_palette(
    pixels: list[tuple[int, int, int]],
    k: int = 12,
    rounds: int = 10,
    max_points: int = 18_000,
) -> list[dict[str, object]]:
    if not pixels:
        return []
    stride = max(1, len(pixels) // max_points)
    points = pixels[::stride]
    if len(points) < k:
        k = max(1, len(points))
    seeds = [points[int(i * (len(points) - 1) / max(1, k - 1))] for i in range(k)]
    centers = [(float(r), float(g), float(b)) for r, g, b in seeds]
    assignments: list[int] = [0] * len(points)
    for _ in range(rounds):
        buckets: list[list[tuple[int, int, int]]] = [[] for _ in range(k)]
        for idx, px in enumerate(points):
            nearest = min(
                range(k),
                key=lambda c: (px[0] - centers[c][0]) ** 2
                + (px[1] - centers[c][1]) ** 2
                + (px[2] - centers[c][2]) ** 2,
            )
            assignments[idx] = nearest
            buckets[nearest].append(px)
        for idx, bucket in enumerate(buckets):
            if bucket:
                centers[idx] = (
                    mean(p[0] for p in bucket),
                    mean(p[1] for p in bucket),
                    mean(p[2] for p in bucket),
                )
    counts = Counter(assignments)
    total = len(assignments) or 1
    result = []
    for idx, count in counts.most_common():
        rgb = tuple(int(round(v)) for v in centers[idx])
        hue, sat = hue_sat(rgb)
        result.append(
            {
                "hex": hex_color(rgb),
                "rgb": rgb,
                "pct": round(count / total * 100, 2),
                "luma": round(srgb_luma(rgb), 1),
                "hue": round(hue, 1),
                "sat": round(sat, 3),
            }
        )
    return result


def edge_stats(image: Image.Image, max_samples: int = 260_000) -> dict[str, float]:
    gray = image.convert("L")
    w, h = gray.size
    pix = gray.load()
    edge_values: list[int] = []
    edge_lumas: list[int] = []
    step = max(2, int(math.sqrt(max(1, w * h) / max_samples)))
    sample_count = 0
    for y in range(1, h - 1, step):
        for x in range(1, w - 1, step):
            sample_count += 1
            gx = int(pix[x + 1, y]) - int(pix[x - 1, y])
            gy = int(pix[x, y + 1]) - int(pix[x, y - 1])
            mag = int(math.sqrt(gx * gx + gy * gy))
            if mag > 26:
                edge_values.append(mag)
                edge_lumas.append(int(pix[x, y]))
    sample_count = max(1, sample_count)
    return {
        "edge_density_pct": round(len(edge_values) / sample_count * 100, 2),
        "edge_strength_p50": round(percentile(edge_values, 0.5), 1),
        "edge_strength_p90": round(percentile(edge_values, 0.9), 1),
        "edge_luma_p10": round(percentile(edge_lumas, 0.1), 1),
        "edge_luma_p50": round(percentile(edge_lumas, 0.5), 1),
    }


def summarize_pixels(pixels: list[tuple[int, int, int]]) -> dict[str, object]:
    lumas = [srgb_luma(px) for px in pixels]
    sats = [hue_sat(px)[1] for px in pixels]
    total = max(1, len(pixels))
    clipped = [px for px in pixels if max(px) >= 248 and srgb_luma(px) >= 235]
    highlight = [px for px in pixels if srgb_luma(px) >= 215]
    light = [px for px in pixels if 160 <= srgb_luma(px) < 215]
    mid = [px for px in pixels if 95 <= srgb_luma(px) < 160]
    dark = [px for px in pixels if srgb_luma(px) <= 65]
    warm_bright = [
        px
        for px in pixels
        if srgb_luma(px) >= 210 and px[0] >= px[2] + 12 and px[1] >= px[2] + 4
    ]
    cool_shadow = [
        px
        for px in pixels
        if srgb_luma(px) <= 140 and px[2] >= px[0] + 6 and px[2] >= px[1] - 4
    ]
    return {
        "pixel_count": len(pixels),
        "luma_p05": round(percentile(lumas, 0.05), 1),
        "luma_p10": round(percentile(lumas, 0.10), 1),
        "luma_p25": round(percentile(lumas, 0.25), 1),
        "luma_p50": round(percentile(lumas, 0.50), 1),
        "luma_p75": round(percentile(lumas, 0.75), 1),
        "luma_p90": round(percentile(lumas, 0.90), 1),
        "luma_p95": round(percentile(lumas, 0.95), 1),
        "mean_saturation": round(mean(sats) if sats else 0, 3),
        "clipped_bloom_pct": round(len(clipped) / total * 100, 2),
        "highlight_plane_pct_luma_ge_215": round(len(highlight) / total * 100, 2),
        "light_mid_plane_pct_luma_160_215": round(len(light) / total * 100, 2),
        "mid_shadow_plane_pct_luma_95_160": round(len(mid) / total * 100, 2),
        "dark_anchor_pct_luma_le_65": round(len(dark) / total * 100, 2),
        "warm_bright_pct": round(len(warm_bright) / total * 100, 2),
        "cool_shadow_pct": round(len(cool_shadow) / total * 100, 2),
        "top_quantized": top_quantized(pixels),
    }


def crop_fraction(image: Image.Image, box: tuple[float, float, float, float]) -> Image.Image:
    w, h = image.size
    x0, y0, x1, y1 = box
    return image.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))


def grid_metrics(image: Image.Image) -> dict[str, dict[str, object]]:
    result = {}
    for gy in range(3):
        for gx in range(3):
            name = f"r{gy + 1}c{gx + 1}"
            crop = crop_fraction(image, (gx / 3, gy / 3, (gx + 1) / 3, (gy + 1) / 3))
            pixels = sample_pixels(crop, max_pixels=18_000)
            summary = summarize_pixels(pixels)
            result[name] = {
                "luma_p50": summary["luma_p50"],
                "clipped_bloom_pct": summary["clipped_bloom_pct"],
                "dark_anchor_pct_luma_le_65": summary["dark_anchor_pct_luma_le_65"],
                "mean_saturation": summary["mean_saturation"],
                "edge": edge_stats(crop),
            }
    return result


def image_paths(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def analyze_image(path: Path, root: Path, max_size: int) -> tuple[dict[str, object] | None, str | None]:
    try:
        with Image.open(path) as raw:
            image = ImageOps.exif_transpose(raw).convert("RGB")
            original_size = image.size
            if max_size > 0 and max(original_size) > max_size:
                image.thumbnail((max_size, max_size))
            pixels = sample_pixels(image)
            sample_for_aggregate = sample_pixels(image, max_pixels=5_000)
            global_summary = summarize_pixels(pixels)
            return (
                {
                    "path": str(path),
                    "relative_path": str(path.relative_to(root)),
                    "original_size": original_size,
                    "analysis_size": image.size,
                    "global": {
                        **global_summary,
                        "edge": edge_stats(image),
                        "palette": kmeans_palette(pixels, k=8, rounds=8),
                    },
                    "grid": grid_metrics(image),
                    "aggregate_sample": sample_for_aggregate,
                },
                None,
            )
    except Exception as exc:  # noqa: BLE001
        return None, f"{path}: {exc}"


def stat(values: Iterable[float]) -> dict[str, float]:
    data = list(values)
    if not data:
        return {"mean": 0, "median": 0, "p10": 0, "p90": 0}
    return {
        "mean": round(mean(data), 2),
        "median": round(median(data), 2),
        "p10": round(percentile(data, 0.10), 2),
        "p90": round(percentile(data, 0.90), 2),
    }


def aggregate(reports: list[dict[str, object]], aggregate_pixels: list[tuple[int, int, int]]) -> dict[str, object]:
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
        metric_stats[name] = stat(float(report["global"][name]) for report in reports)
    metric_stats["edge_density_pct"] = stat(
        float(report["global"]["edge"]["edge_density_pct"]) for report in reports
    )
    grid_summary = {}
    for cell in [f"r{gy}c{gx}" for gy in range(1, 4) for gx in range(1, 4)]:
        grid_summary[cell] = {
            "luma_p50": stat(float(report["grid"][cell]["luma_p50"]) for report in reports),
            "clipped_bloom_pct": stat(float(report["grid"][cell]["clipped_bloom_pct"]) for report in reports),
            "dark_anchor_pct": stat(float(report["grid"][cell]["dark_anchor_pct_luma_le_65"]) for report in reports),
            "edge_density_pct": stat(
                float(report["grid"][cell]["edge"]["edge_density_pct"]) for report in reports
            ),
        }
    return {
        "image_count": len(reports),
        "metric_stats": metric_stats,
        "palette": kmeans_palette(aggregate_pixels, k=14, rounds=12, max_points=36_000),
        "top_quantized": top_quantized(aggregate_pixels, limit=18),
        "grid_summary": grid_summary,
    }


def sort_top(reports: list[dict[str, object]], metric_path: tuple[str, ...], reverse: bool = True) -> list[dict[str, object]]:
    def read(report: dict[str, object]) -> float:
        value: object = report
        for key in metric_path:
            value = value[key]  # type: ignore[index]
        return float(value)

    return sorted(reports, key=read, reverse=reverse)[:8]


def markdown(data: dict[str, object]) -> str:
    aggregate_data = data["aggregate"]
    metric_stats = aggregate_data["metric_stats"]
    lines = [
        "# Reference Pixel-Plane Batch Analysis",
        "",
        f"SOURCE_DIR: {data['source_dir']}",
        f"IMAGE_COUNT: {aggregate_data['image_count']}",
        f"FAILED_COUNT: {len(data['failures'])}",
        "",
        "## Aggregate Plane Metrics",
        "",
        "| metric | mean | median | p10 | p90 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    metric_labels = [
        ("luma_p10", "luma p10"),
        ("luma_p50", "luma p50"),
        ("luma_p90", "luma p90"),
        ("mean_saturation", "mean saturation"),
        ("clipped_bloom_pct", "clipped bloom %"),
        ("highlight_plane_pct_luma_ge_215", "highlight plane L>=215 %"),
        ("light_mid_plane_pct_luma_160_215", "light-mid plane L160-215 %"),
        ("mid_shadow_plane_pct_luma_95_160", "mid-shadow plane L95-160 %"),
        ("dark_anchor_pct_luma_le_65", "dark anchor L<=65 %"),
        ("warm_bright_pct", "warm bright %"),
        ("cool_shadow_pct", "cool shadow %"),
        ("edge_density_pct", "edge density %"),
    ]
    for key, label in metric_labels:
        stats = metric_stats[key]
        lines.append(f"| {label} | {stats['mean']} | {stats['median']} | {stats['p10']} | {stats['p90']} |")
    lines.extend(["", "## Aggregate Palette Clusters", "", "| hex | pct | luma | hue | sat |", "| --- | ---: | ---: | ---: | ---: |"])
    for item in aggregate_data["palette"]:
        lines.append(f"| {item['hex']} | {item['pct']} | {item['luma']} | {item['hue']} | {item['sat']} |")
    lines.extend(["", "## Top Quantized Colors", ""])
    lines.append(", ".join(f"{item['hex']} {item['pct']}%" for item in aggregate_data["top_quantized"]))
    lines.extend(["", "## 3x3 Composition Grid Signature", ""])
    lines.append("Cells are r1c1 through r3c3, top-left to bottom-right. Values are cross-image medians.")
    lines.extend(["", "| cell | luma p50 | clipped bloom % | dark anchor % | edge density % |", "| --- | ---: | ---: | ---: | ---: |"])
    for cell, stats in aggregate_data["grid_summary"].items():
        lines.append(
            f"| {cell} | {stats['luma_p50']['median']} | {stats['clipped_bloom_pct']['median']} | "
            f"{stats['dark_anchor_pct']['median']} | {stats['edge_density_pct']['median']} |"
        )
    lines.extend(["", "## Strongest Exemplars", ""])
    exemplar_specs = [
        ("highest clipped bloom", ("global", "clipped_bloom_pct")),
        ("highest dark anchors", ("global", "dark_anchor_pct_luma_le_65")),
        ("highest edge density", ("global", "edge", "edge_density_pct")),
        ("highest mean saturation", ("global", "mean_saturation")),
        ("highest warm bright", ("global", "warm_bright_pct")),
    ]
    for label, path in exemplar_specs:
        lines.extend([f"### {label}", "", "| file | value | luma p50 | sat | bloom % | dark % | edge % |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"])
        for report in sort_top(data["images"], path):
            value: object = report
            for key in path:
                value = value[key]  # type: ignore[index]
            g = report["global"]
            lines.append(
                f"| {report['relative_path']} | {float(value):.2f} | {g['luma_p50']} | {g['mean_saturation']} | "
                f"{g['clipped_bloom_pct']} | {g['dark_anchor_pct_luma_le_65']} | {g['edge']['edge_density_pct']} |"
            )
        lines.append("")
    lines.extend(["## Per-Image Summary", "", "| file | size | luma p10/50/90 | sat | bloom % | dark % | warm % | edge % | main palette |", "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |"])
    for report in data["images"]:
        g = report["global"]
        palette = ", ".join(item["hex"] for item in g["palette"][:5])
        lines.append(
            f"| {report['relative_path']} | {report['original_size'][0]}x{report['original_size'][1]} | "
            f"{g['luma_p10']}/{g['luma_p50']}/{g['luma_p90']} | {g['mean_saturation']} | "
            f"{g['clipped_bloom_pct']} | {g['dark_anchor_pct_luma_le_65']} | {g['warm_bright_pct']} | "
            f"{g['edge']['edge_density_pct']} | {palette} |"
        )
    if data["failures"]:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {failure}" for failure in data["failures"])
    lines.extend(
        [
            "",
            "## Production Translation",
            "",
            "- Treat the palette clusters as paint pools, not exact swatches.",
            "- Preserve clipped or near-clipped lights only as intentional bloom planes; keep face and silhouette edge readability.",
            "- Keep dark anchors compact and structural: eyelids, lashes, garment separations, hair shadow masses, weapon/armor seams when present.",
            "- Use edge-density and edge-luma numbers to avoid generic thick black outlines; line color should lean toward local material and local shadow temperature.",
            "- Use the 3x3 grid medians as composition pressure guidance: where the folder repeatedly places bright planes, dark anchors, and edge detail.",
        ]
    )
    return "\n".join(lines) + "\n"


def strip_samples(report: dict[str, object]) -> dict[str, object]:
    clean = dict(report)
    clean.pop("aggregate_sample", None)
    return clean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure pixel-plane style traits across a reference folder.")
    parser.add_argument("source_dir", type=Path, help="Folder containing reference images")
    parser.add_argument("--out-md", type=Path, required=True, help="Markdown report path")
    parser.add_argument("--out-json", type=Path, required=True, help="JSON report path")
    parser.add_argument(
        "--max-size",
        type=int,
        default=0,
        help="Optional max analysis dimension. 0 keeps full source resolution.",
    )
    parser.add_argument("--offset", type=int, default=0, help="Start index in sorted image list")
    parser.add_argument("--limit", type=int, default=0, help="Maximum number of images to analyze; 0 means all")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.source_dir.resolve()
    all_paths = image_paths(root)
    if args.offset < 0:
        raise SystemExit("--offset must be >= 0")
    if args.limit < 0:
        raise SystemExit("--limit must be >= 0")
    paths = all_paths[args.offset : args.offset + args.limit] if args.limit else all_paths[args.offset :]
    reports: list[dict[str, object]] = []
    failures: list[str] = []
    aggregate_pixels: list[tuple[int, int, int]] = []
    for path in paths:
        report, failure = analyze_image(path, root, args.max_size)
        if failure:
            failures.append(failure)
            continue
        assert report is not None
        aggregate_pixels.extend(report.pop("aggregate_sample"))
        reports.append(report)
    if not reports:
        raise SystemExit(f"No analyzable images found in {root}")
    data = {
        "source_dir": str(root),
        "image_count_seen": len(all_paths),
        "batch_offset": args.offset,
        "batch_limit": args.limit,
        "batch_image_count": len(paths),
        "failures": failures,
        "aggregate": aggregate(reports, aggregate_pixels),
        "images": [strip_samples(report) for report in reports],
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    args.out_md.write_text(markdown(data), encoding="utf-8")
    print(args.out_md)
    print(args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
