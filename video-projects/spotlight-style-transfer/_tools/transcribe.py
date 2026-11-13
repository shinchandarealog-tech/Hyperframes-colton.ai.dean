import json,sys
from faster_whisper import WhisperModel
m=WhisperModel("medium.en",device="cpu",compute_type="int8")
import soundfile as sf
a,_=sf.read(sys.argv[1],dtype="float32")
segs,_=m.transcribe(a,word_timestamps=True,beam_size=5)
W=[]
for s in segs:
    print(round(s.start,2),round(s.end,2),s.text)
    for w in s.words: W.append(dict(w=w.word.strip(),s=round(w.start,3),e=round(w.end,3),p=round(w.probability,3)))
json.dump(W,open(sys.argv[2],"w"),indent=0)
print(len(W),"words")
