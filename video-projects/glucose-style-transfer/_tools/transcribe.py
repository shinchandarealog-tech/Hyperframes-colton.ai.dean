import sys,json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[3] if len(sys.argv)>3 else 'small',device='cpu',compute_type='int8')
import soundfile as sf
aud,_=sf.read(sys.argv[1],dtype="float32")
segs,info=m.transcribe(aud,word_timestamps=True)
out=[];print('lang',info.language)
for s in segs:
    print(round(s.start,2),round(s.end,2),s.text)
    for w in s.words: out.append(dict(w=w.word.strip(),s=round(w.start,3),e=round(w.end,3),p=round(w.probability,3)))
json.dump(out,open(sys.argv[2],'w'),indent=0)
