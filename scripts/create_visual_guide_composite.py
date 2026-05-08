#!/usr/bin/env python3
"""Create an annotated visual-guide composite from blockout passes.

The illustrate workflow uses this as the render-bound bridge between
perspective math and image generation: clay/lineart/depth passes become a
single user-reviewable reference image with scale/perspective annotations.

This script intentionally uses Windows PowerShell + System.Drawing so the
project does not need a new Python imaging dependency.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an annotated visual guide composite PNG.")
    parser.add_argument("--clay", required=True, type=Path, help="Clay/solid blockout PNG used as the base image.")
    parser.add_argument("--lineart", type=Path, help="Lineart/wire/blockout PNG to overlay.")
    parser.add_argument("--depth", type=Path, help="Depth/normal/mask PNG shown as an inset.")
    parser.add_argument("--out", required=True, type=Path, help="Output composite PNG path.")
    parser.add_argument("--title", default="VISUAL GUIDE COMPOSITE", help="Title label drawn on the composite.")
    parser.add_argument(
        "--note",
        action="append",
        default=[],
        help="Annotation note drawn under the title. May be repeated.",
    )
    parser.add_argument(
        "--line",
        action="append",
        default=[],
        metavar="LABEL:X1,Y1,X2,Y2:COLOR",
        help="Draw a labeled line. Color is #RRGGBB. May be repeated.",
    )
    parser.add_argument(
        "--box",
        action="append",
        default=[],
        metavar="LABEL:X,Y,W,H:COLOR",
        help="Draw a labeled rectangle. Color is #RRGGBB. May be repeated.",
    )
    return parser.parse_args()


def parse_annot(raw: str, expected_numbers: int) -> dict[str, object]:
    try:
        label, numbers, color = raw.rsplit(":", 2)
        coords = [int(float(part.strip())) for part in numbers.split(",")]
    except ValueError as exc:
        raise SystemExit(f"Invalid annotation format: {raw!r}") from exc
    if len(coords) != expected_numbers:
        raise SystemExit(f"Invalid annotation coordinate count in {raw!r}: expected {expected_numbers}")
    return {"label": label.strip(), "coords": coords, "color": color.strip() or "#00FFFF"}


def main() -> int:
    args = parse_args()
    for label, path in (("clay", args.clay), ("lineart", args.lineart), ("depth", args.depth)):
        if path and not path.exists():
            print(f"ERROR: {label} image not found: {path}", file=sys.stderr)
            return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    config = {
        "clay": str(args.clay.resolve()),
        "lineart": str(args.lineart.resolve()) if args.lineart else "",
        "depth": str(args.depth.resolve()) if args.depth else "",
        "out": str(args.out.resolve()),
        "title": args.title,
        "notes": args.note,
        "lines": [parse_annot(item, 4) for item in args.line],
        "boxes": [parse_annot(item, 4) for item in args.box],
    }

    ps = r"""
param([string]$ConfigPath)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing
$cfg = Get-Content -LiteralPath $ConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
function ColorFromHex([string]$hex) {
  if ([string]::IsNullOrWhiteSpace($hex)) { $hex = "#00FFFF" }
  if ($hex.StartsWith("#")) { $hex = $hex.Substring(1) }
  return [System.Drawing.Color]::FromArgb(
    255,
    [Convert]::ToInt32($hex.Substring(0,2), 16),
    [Convert]::ToInt32($hex.Substring(2,2), 16),
    [Convert]::ToInt32($hex.Substring(4,2), 16)
  )
}
$base = [System.Drawing.Image]::FromFile([string]$cfg.clay)
$bmp = New-Object System.Drawing.Bitmap($base.Width, $base.Height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.DrawImage($base, 0, 0, $base.Width, $base.Height)
if ($cfg.lineart) {
  $line = [System.Drawing.Image]::FromFile([string]$cfg.lineart)
  $g.DrawImage($line, 0, 0, $base.Width, $base.Height)
  $line.Dispose()
}
if ($cfg.depth) {
  $depth = [System.Drawing.Image]::FromFile([string]$cfg.depth)
  $insetW = [Math]::Max(220, [int]($base.Width * 0.24))
  $insetH = [int]($insetW * $depth.Height / $depth.Width)
  $x = $base.Width - $insetW - 20
  $y = $base.Height - $insetH - 20
  $g.FillRectangle((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(180,0,0,0))), $x-8, $y-28, $insetW+16, $insetH+36)
  $g.DrawImage($depth, $x, $y, $insetW, $insetH)
  $g.DrawString("depth / structure inset", (New-Object System.Drawing.Font("Arial", 14, [System.Drawing.FontStyle]::Bold)), [System.Drawing.Brushes]::White, $x, $y-24)
  $depth.Dispose()
}
$titleFont = New-Object System.Drawing.Font("Arial", 24, [System.Drawing.FontStyle]::Bold)
$noteFont = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Regular)
$g.FillRectangle((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(170,0,0,0))), 12, 12, [Math]::Min(900,$base.Width-24), 50 + 24 * $cfg.notes.Count)
$g.DrawString($cfg.title, $titleFont, [System.Drawing.Brushes]::White, 24, 20)
$ny = 52
foreach ($note in $cfg.notes) {
  $g.DrawString([string]$note, $noteFont, [System.Drawing.Brushes]::White, 24, $ny)
  $ny += 24
}
foreach ($item in $cfg.lines) {
  $c = ColorFromHex([string]$item.color)
  $pen = New-Object System.Drawing.Pen($c, 4)
  $coords = @($item.coords)
  $g.DrawLine($pen, $coords[0], $coords[1], $coords[2], $coords[3])
  $g.DrawString([string]$item.label, $noteFont, (New-Object System.Drawing.SolidBrush($c)), $coords[2] + 6, $coords[3] + 6)
  $pen.Dispose()
}
foreach ($item in $cfg.boxes) {
  $c = ColorFromHex([string]$item.color)
  $pen = New-Object System.Drawing.Pen($c, 4)
  $coords = @($item.coords)
  $g.DrawRectangle($pen, $coords[0], $coords[1], $coords[2], $coords[3])
  $g.DrawString([string]$item.label, $noteFont, (New-Object System.Drawing.SolidBrush($c)), $coords[0], [Math]::Max(0, $coords[1]-24))
  $pen.Dispose()
}
$bmp.Save([string]$cfg.out, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose(); $base.Dispose()
"""
    with tempfile.TemporaryDirectory() as td:
        config_path = Path(td) / "visual-guide-config.json"
        script_path = Path(td) / "visual-guide-composite.ps1"
        config_path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
        script_path.write_text(ps, encoding="utf-8")
        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script_path),
                "-ConfigPath",
                str(config_path),
            ],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
    if completed.returncode != 0:
        print(completed.stdout, file=sys.stdout)
        print(completed.stderr, file=sys.stderr)
        return completed.returncode
    if not args.out.exists():
        print(completed.stdout, file=sys.stdout)
        print(completed.stderr, file=sys.stderr)
        print(f"ERROR: composite output was not created: {args.out}", file=sys.stderr)
        return 1
    print(f"Created visual guide composite: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
