"""Readable summary of an extracted spec: only animated / expression / effect / text / non-default transform props."""
import sys, json
DEFAULT_T = {"ADBE Anchor Point": None, "ADBE Position": None, "ADBE Scale": [100,100,100], "ADBE Rotate Z": 0, "ADBE Opacity": 100}
def short(v, n=90):
    s = json.dumps(v) if not isinstance(v, str) else v
    return s if len(s) <= n else s[:n] + "…"
def walk(p, path, out, in_fx=False, in_text=False):
    m = p.get("match", "")
    here = path + [p["name"]]
    fx = in_fx or m == "ADBE Effect Parade"; tx = in_text or m in ("ADBE Text Properties",)
    if "props" in p:
        for c in p["props"]: walk(c, here, out, fx, tx)
        return
    keys, expr, val = p.get("keys"), p.get("expr"), p.get("value")
    interesting = keys or expr or fx or tx or m in DEFAULT_T or m in ("ADBE Position_0","ADBE Position_1","ADBE Mask Shape","ADBE Mask Opacity","ADBE Mask Feather","ADBE Mask Offset")
    if m in DEFAULT_T and not keys and not expr and DEFAULT_T[m] is not None and val == DEFAULT_T[m]: interesting = False
    if not interesting or val is None and not keys and not expr: return
    s = "/".join(here[1:]) + f" [{m}]"
    if keys: s += "  KEYS " + short([[round(k["t"],3), k["v"]] for k in keys], 160)
    else: s += "  = " + short(val)
    if expr: s += "\n          EXPR: " + expr.replace("\n", " ⏎ ")[:400]
    out.append(s)
spec = json.load(open(sys.argv[1]))
order = [str(spec["root"])] + [k for k in spec["comps"] if k != str(spec["root"])]
for cid in order:
    c = spec["comps"][cid]
    print(f"\n=== COMP {c['name']} ({cid}) {c['w']}x{c['h']} {c['fps']}fps {c['duration']}s mb={c['motion_blur']}")
    for L in c["layers"]:
        src = L.get("source", {})
        print(f"-- L{L['index']} {L['name']} [{L['type']}] in={L['in']:.2f} out={L['out']:.2f} start={L['start']:.2f} parent={L['parent']} src={src.get('kind')}:{src.get('name')} {src.get('color','')} en={L['enabled']} blend={L['blend']} 3d={L['threeD']} matte={L.get('matte')} mb={L['motion_blur']}")
        out = []
        for p in L["props"]:
            if p["match"] in ("ADBE Marker","ADBE Time Remapping","ADBE MTrackers","ADBE Layer Styles","ADBE Plane Options Group","ADBE Extrsn Options Group","ADBE Material Options Group","ADBE Audio Group","ADBE Data Group","ADBE Layer Overrides","ADBE Layer Sets","ADBE Source Options Group"): continue
            walk(p, [], out)
        for s in out: print("     " + s)
