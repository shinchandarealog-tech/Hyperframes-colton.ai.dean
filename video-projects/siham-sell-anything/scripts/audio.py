"""Audio: voice cut from the take (-14 LUFS), ducked music bed, whooshes on transitions, pops on cards/script words."""
import json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TL = json.load(open(os.path.join(HERE, "timeline.json")))
SFX = json.load(open(os.path.join(HERE, "sfx.json")))
DUR = TL["duration"]
RAW = os.path.join(ROOT, "raw-media/raw/take.mp4")
A = lambda f: os.path.join(ROOT, "assets", f)
OUT = os.path.join(ROOT, "renders")
SEG = {s["id"]: s for s in TL["segments"]}


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def voice():
    parts, labels = [], []
    for i, s in enumerate(TL["segments"]):
        d = s["src_out"] - s["src_in"]
        parts.append(f"[0:a]atrim={s['src_in']}:{s['src_out']},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d=0.012,afade=t=out:st={d - 0.015:.4f}:d=0.015[v{i}]")
        labels.append(f"[v{i}]")
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1,apad=whole_dur={DUR},highpass=f=70[v]"
    tmp = os.path.join(OUT, "voice_cut.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", RAW, "-filter_complex", fc, "-map", "[v]", "-ar", "48000", "-ac", "2", tmp])
    # two-pass loudnorm to -14 LUFS
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    out = os.path.join(OUT, "voice.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af",
         f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
         f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000", out])
    return out


def mix(vpath):
    # transitions: every cut into / out of B-roll or a graphic, and the drop into the close
    cuts = [SEG["B"]["out_in"], SEG["C"]["out_in"], SEG["D"]["out_in"], 12.63, SEG["J"]["out_in"],
            SEG["K"]["out_in"], SEG["L"]["out_in"], SEG["M"]["out_in"], SEG["P"]["out_in"]]
    whooshes = [("whoosh-04.mp3", 0.89, -4), ("whoosh-03.mp3", 0.70, -9), ("whoosh-06.mp3", 0.74, -9)]
    events = []
    for i, c in enumerate(cuts):
        f, peak, g = whooshes[i % len(whooshes)]
        events.append((f, max(c - peak, 0), g, 0))
    for e in SFX:
        if e["k"] == "pop":
            events.append(("pop.mp3", e["t"] - 0.02, -11, 0))
        elif e["k"] == "popbig":
            events.append(("pop.mp3", e["t"] - 0.02, -7, 0))
        elif e["k"] == "swish":
            events.append(("whoosh.mp3", e["t"] - 0.12, -15, 0))
        elif e["k"] == "paper":
            events.append(("whoosh.mp3", e["t"] - 0.05, -10, 0))
    inputs = ["-i", vpath, "-ss", "6.3", "-i", A("music/bed.mp3")]
    fc = ["[1:a]atrim=0:%.3f,asetpts=PTS-STARTPTS,volume=-21dB,afade=t=in:d=0.4,afade=t=out:st=%.3f:d=1.2,aresample=48000,aformat=channel_layouts=stereo[mus]" % (DUR, DUR - 1.2),
          "[0:a]asplit=2[vo][sc]",
          "[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350:makeup=1[duck]"]
    sfx_labels = []
    for i, (f, t, g, _) in enumerate(events):
        inputs += ["-i", A("sfx/" + f)]
        k = i + 2
        ms = int(round(max(t, 0) * 1000))
        fc.append(f"[{k}:a]volume={g}dB,aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[s{i}]")
        sfx_labels.append(f"[s{i}]")
    fc.append("".join(sfx_labels) + f"amix=inputs={len(sfx_labels)}:normalize=0:duration=longest,atrim=0:{DUR}[sfx]")
    fc.append(f"[vo][duck][sfx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89:level=false,atrim=0:{DUR}[out]")
    out = os.path.join(OUT, "mix.wav")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "48000", out])
    return out, events


if __name__ == "__main__":
    v = voice()
    m, ev = mix(v)
    for p in (v, m):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        print(os.path.basename(p), re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1], "LUFS", re.findall(r"Peak:\s+(-?[\d.]+)", r)[-1], "dBTP")
    print(len(ev), "sfx events")
