#!/usr/bin/env python3
"""Inline src/fx.css + src/fx.js into every src/scenes/*.html → compositions/*.html.

Edit scenes in src/scenes/, then run:  python3 scripts/build-comps.py
(compositions/ is generated — don't hand-edit it.)
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
css = (root / "src/fx.css").read_text()
js = (root / "src/fx.js").read_text()
out = root / "compositions"
out.mkdir(exist_ok=True)
for src in sorted((root / "src/scenes").glob("*.html")):
    html = src.read_text()
    assert "/*@FX_CSS*/" in html and "/*@FX_JS*/" in html, f"{src.name}: missing FX placeholders"
    html = html.replace("/*@FX_CSS*/", css).replace("/*@FX_JS*/", js)
    banner = f"<!-- GENERATED from src/scenes/{src.name} by scripts/build-comps.py — edit the source, not this file. -->\n"
    (out / src.name).write_text(banner + html)
    print("built", src.name)
