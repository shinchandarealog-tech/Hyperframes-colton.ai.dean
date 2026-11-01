"""Render every ported template from the Hook & Captions pack.

usage: python render_library.py [names...]      e.g. "Caption 07" "Hook 03"
Each template renders with texts/<slug>.json if present (otherwise its original text),
30 fps, 180-degree motion blur, over home-tour footage; hooks get assets/media_porch.mp4
in every media slot. Outputs renders/<slug>.mov (alpha) and renders/<slug>_preview.mp4.
"""
import subprocess, sys, pathlib, concurrent.futures as cf
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TOOL = ROOT / "tools/aep_port/render.py"
SPECS = ROOT / "_reference/templates/hook-captions/specs"
BGS = ["bg_kitchen.mp4", "bg_drone.mp4", "bg_stairs.mp4"]
ALL = [f"Caption {i:02d}" for i in range(1, 16)] + [f"Hook {i:02d}" for i in range(1, 6)]

def render(i_name):
    i, name = i_name
    slug = name.lower().replace(" ", "")
    args = ["python3", str(TOOL), str(SPECS / f"Render - {name}.json"), str(HERE / "renders" / slug),
            "--fps", "30", "--shutter", "180", "--bg", str(HERE / "assets" / BGS[i % 3])]
    texts = HERE / "texts" / f"{slug}.json"
    if texts.exists(): args += ["--texts", str(texts)]
    if name.startswith("Hook"):
        for slot in ("Media 01", "Media 02"): args += ["--media", f"{slot}={HERE / 'assets/media_porch.mp4'}"]
    else: args += ["--duration", "3.5"]
    r = subprocess.run(args, capture_output=True, text=True)
    return name, r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:]

if __name__ == "__main__":
    names = sys.argv[1:] or ALL
    with cf.ThreadPoolExecutor(4) as ex:
        for name, rc, tail in ex.map(render, list(enumerate(names))): print(name, "ok" if rc == 0 else f"FAILED rc={rc}", *tail, flush=True)
