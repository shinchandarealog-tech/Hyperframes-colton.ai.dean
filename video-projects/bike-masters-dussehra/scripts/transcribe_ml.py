import json, sys, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[3], device="cpu", compute_type="int8")
audio = np.fromfile(sys.argv[1], np.int16).astype(np.float32)/32768
segs, info = m.transcribe(audio, word_timestamps=True, task=sys.argv[4] if len(sys.argv)>4 else "transcribe")
print("lang", info.language, info.language_probability)
out=[]
for s in segs:
    out += [{"text":w.word.strip(),"start":round(w.start,3),"end":round(w.end,3)} for w in s.words]
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
json.dump(out, open(sys.argv[2],"w"), indent=1, ensure_ascii=False)
