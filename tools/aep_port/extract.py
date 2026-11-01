"""Extract After Effects comps from an .aep into JSON specs (no AE needed).

usage: python extract.py project.aep out_dir "Hook 01" "Caption 01" ...
Writes out_dir/<comp>.json containing the comp and every comp it nests.
Only properties that matter for playback are kept: animated, expression-driven,
or changed from their defaults (we keep all transform values to be safe).
"""
import sys, json, math, pathlib
import py_aep

def jv(v):
    if v is None or isinstance(v, (bool, int, str)): return v
    if isinstance(v, float): return None if math.isnan(v) else round(v, 6)
    if isinstance(v, (list, tuple)): return [jv(x) for x in v]
    if hasattr(v, "__dict__") and type(v).__name__ in ("Shape",):
        return {"vertices": jv(getattr(v, "vertices", None)), "in": jv(getattr(v, "in_tangents", None)),
                "out": jv(getattr(v, "out_tangents", None)), "closed": getattr(v, "closed", None)}
    return repr(v)[:200]

def ease(e):
    return [{"speed": jv(x.speed), "influence": jv(x.influence)} for x in (e or [])]

def text_doc(td):
    keys = ["text", "font", "font_size", "fill_color", "stroke_color", "stroke_width", "apply_fill", "apply_stroke",
            "tracking", "leading", "auto_leading", "justification", "all_caps", "small_caps", "baseline_shift",
            "box_text", "box_text_size", "box_text_pos", "horizontal_scale", "vertical_scale", "font_family", "font_style"]
    out = {}
    for k in keys:
        try: out[k] = jv(getattr(td, k))
        except Exception: pass
    return out

def prop(p, depth=0):
    d = {"name": p.name, "match": p.match_name}
    kids = getattr(p, "properties", None)
    if kids is not None and not hasattr(p, "keyframes"):
        ch = [prop(c, depth + 1) for c in kids]
        ch = [c for c in ch if c]
        if not ch: return None
        d["props"] = ch
        return d
    try:
        ks = p.keyframes
    except Exception:
        ks = None
    expr = getattr(p, "expression", "") or ""
    en = getattr(p, "expression_enabled", True)
    try:
        val = p.value
    except Exception:
        val = None
    if type(val).__name__ == "TextDocument":
        val = text_doc(val)
        if ks: d["keys"] = [{"t": jv(k.time), "v": text_doc(k.value)} for k in ks]
    else:
        val = jv(val)
        if ks:
            d["keys"] = [{"t": jv(k.time), "v": jv(k.value), "ii": str(k.in_interpolation_type).split(".")[-1],
                          "oi": str(k.out_interpolation_type).split(".")[-1], "ie": ease(k.in_temporal_ease),
                          "oe": ease(k.out_temporal_ease), "ist": jv(k.in_spatial_tangent),
                          "ost": jv(k.out_spatial_tangent)} for k in ks]
    if expr and en: d["expr"] = expr
    d["value"] = val
    try: d["mod"] = bool(p.is_modified)
    except Exception: pass
    return d

def layer(L):
    d = {"index": L.index, "name": L.name, "type": type(L).__name__, "in": jv(L.in_point), "out": jv(L.out_point),
         "start": jv(L.start_time), "stretch": jv(L.stretch), "enabled": L.enabled, "parent": L.parent.index if L.parent else None,
         "blend": str(L.blending_mode).split(".")[-1], "threeD": bool(getattr(L, "three_d_layer", False)),
         "adjustment": bool(getattr(L, "adjustment_layer", False)), "null": bool(getattr(L, "null_layer", False)),
         "guide": bool(getattr(L, "guide_layer", False)), "motion_blur": bool(getattr(L, "motion_blur", False)),
         "collapse": bool(getattr(L, "collapse_transformation", False))}
    try:
        if L.has_track_matte or getattr(L, "track_matte_layer", None):
            d["matte"] = {"layer": L.track_matte_layer.index if L.track_matte_layer else None,
                          "type": str(L.track_matte_type).split(".")[-1]}
    except Exception: pass
    src = getattr(L, "source", None)
    if src is not None:
        d["source"] = {"kind": type(src).__name__, "name": src.name, "id": getattr(src, "id", None),
                       "w": getattr(src, "width", None), "h": getattr(src, "height", None)}
        ms = getattr(src, "main_source", None)
        if ms is not None and type(ms).__name__ == "SolidSource": d["source"]["color"] = jv(ms.color)
        if ms is not None and type(ms).__name__ == "FileSource": d["source"]["file"] = str(getattr(ms, "file", ""))
    d["props"] = [x for x in (prop(p) for p in L.properties) if x]
    return d

def comp(c, out, seen):
    if c.id in seen: return
    seen.add(c.id)
    out[str(c.id)] = {"id": c.id, "name": c.name, "w": c.width, "h": c.height, "fps": jv(c.frame_rate),
                      "duration": jv(c.duration), "bg": jv(getattr(c, "bg_color", None)),
                      "motion_blur": bool(getattr(c, "motion_blur", False)),
                      "shutter_angle": jv(getattr(c, "shutter_angle", None)), "shutter_phase": jv(getattr(c, "shutter_phase", None)),
                      "layers": [layer(L) for L in c.layers]}
    for L in c.layers:
        s = getattr(L, "source", None)
        if s is not None and type(s).__name__ == "CompItem": comp(s, out, seen)

def main():
    aep, outdir, names = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3:]
    outdir.mkdir(parents=True, exist_ok=True)
    proj = py_aep.parse(aep).project
    comps = [x for x in proj.items.values() if type(x).__name__ == "CompItem"]
    for n in names:
        root = [c for c in comps if c.name == n][0]
        out = {}; comp(root, out, set())
        (outdir / f"{n}.json").write_text(json.dumps({"root": root.id, "comps": out}, indent=1))
        print(n, "->", len(out), "comps")

if __name__ == "__main__":
    main()
