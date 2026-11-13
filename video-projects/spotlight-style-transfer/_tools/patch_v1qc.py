# QC fixes found on v1 frame review: big-word word spacing, script ink width (13 px gap like the ref), lone big word timing.
p = 'web/builder/index.html'; s = open(p).read()
rep = [
 # big word: keep a visible space between words despite -0.06em tracking (+0.16em word spacing)
 ("let s=bg_.s, m=measure(tbig,bg_.f,s,bg_.w,st.bigTrack*s);\n    if(m.w>st.bigMax){s*=st.bigMax/m.w;m=measure(tbig,bg_.f,s,bg_.w,st.bigTrack*s)}",
  "const ws=s0=>0.16*s0, mB=s0=>{const r=measure(tbig.replace(/ /g,'\\u2002'),bg_.f,s0,bg_.w,st.bigTrack*s0);return r};\n    let s=bg_.s, m=mB(s);\n    if(m.w>st.bigMax){s*=st.bigMax/m.w;m=mB(s)}"),
 ("'letter-spacing':st.bigTrack*s,fill:'url(#bigGrad)'},g);t.textContent=tbig;",
  "'letter-spacing':st.bigTrack*s,fill:'url(#bigGrad)'},g);t.textContent=tbig.replace(/ /g,'\\u2002');"),
 # a big word that is the only text on its page lands on the beat's first spoken word (no empty card)
 ("els.push({g,kind:'pop',t0:T(R.big),cx,cy});",
  "const bigT=(!tl1&&!tsc&&!tsm)?wt(BEATS[b].w[0])-lead:T(R.big);\n    els.push({g,kind:'pop',t0:bigT,cx,cy});"),
 ("els.push({g:dg,kind:'dotpop',t0:T(R.big)+.22,", "els.push({g:dg,kind:'dotpop',t0:bigT+.22,"),
 # script width = ink width (Italianno's advance adds ~30 px of empty space; ref gap is 13 px ink-to-ink)
 ("const scW=tsc?measure(tsc,sc.f,sc.s,400,0).w:0,",
  "const scW=tsc?inkW(tsc,sc.s):0,"),
 ("const measure=(()=>{", "const inkW=(()=>{const c=document.createElement('canvas').getContext('2d');return(str,size)=>{c.font=`${size}px Italianno`;const m=c.measureText(str);return m.actualBoundingBoxRight-Math.min(0,-m.actualBoundingBoxLeft)}})();\nconst measure=(()=>{"),
]
for a, b in rep:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
open(p, 'w').write(s); print('patched')
