#!/usr/bin/env python3
"""Generates index.html for the Abhira Green Energy reel.
Edit the SHOTS / TEXTS tables below, then run: python3 edit-data/build.py
"""
import json, os

FPS = 30
TOTAL = 78.0

def snap(t):
    return round(round(t * FPS) / FPS, 4)

# ---- Footage edit (start, end, clip, media_start) — synced to voiceover phrases
# None as clip = text-only kinetic stage
SHOTS = [
    (0.00, 4.50, "c10", 0.00),   # bijli ka bill kam karna hai (worried man + bill)
    (4.50, 7.90, "c01", 2.60),   # solar energy behtar option (home turns solar)
    (7.90, 11.90, "c07", 1.50),  # electricity ki zaroorat badh rahi (home appliances)
    (11.90, 14.90, "c04", 0.00), # solar panel lagwana (installation)
    (14.90, 17.45, "c08", 1.45), # kharche kam, achha kadam (bill -> panel in window)
    (17.45, 23.48, "c05", 0.00), # Abhira ke saath ghar ya business
    (23.48, 27.30, "c06", 0.00), # suraj ki roshni se bijli
    (27.30, 32.00, "c03", 0.80), # din ke samay zaroorat poori
    (32.00, 34.30, "c10", 5.70), # bill mein bachat (same man, now smiling)
    (34.30, 38.10, "c02", 0.10), # sabse khaas baat, rooftop solar
    (38.10, 42.10, "c09", 0.00), # sarkari yojana, subsidy
    (42.10, 45.40, None, 0),     # TEXT-ONLY: badhte kharche ke baare mein sochiye mat
    (45.40, 48.40, "c04", 3.00), # smart solution ki taraf kadam
    (48.40, 54.44, "c11", 0.00), # solar installation + subsidy jaankari, Abhira card
    (54.44, 60.48, "c12", 0.00), # address (city -> address card)
    (60.48, 64.00, None, 0),     # TEXT-ONLY: Patna 800020
    (64.00, 68.00, "c13", 0.00), # contact number
    (68.00, 74.00, "c14", 0.00), # Abhira end card, aaj ki bachat kal ka behtar future
    (74.00, TOTAL, None, 0),     # OUTRO hold card
]

# ---- Kinetic typography (start, end, position, [ (text, size, colour, anim) ... ])
# colour: w = white chrome, g = sun gold, l = leaf green;   anim: rise | slam | slide | pop | drop
# position: low = lower band (y 1120+), top = upper band (y 300+), mid = centre (text-only stages)
TEXTS = [
    (0.05, 2.55, "low", [("बिजली का", 74, "w", "rise"), ("बिल", 150, "g", "slam"), ("कम करना है?", 82, "w", "rise")]),
    (2.60, 4.50, "low", [("फ्यूचर के लिए", 58, "w", "slide"), ("स्मार्ट इन्वेस्टमेंट", 92, "g", "pop")]),
    (4.70, 6.55, "low", [("सोलर", 140, "g", "slam"), ("एनर्जी", 110, "w", "rise")]),
    (6.60, 7.90, "low", [("बेहतर", 120, "l", "pop"), ("ऑप्शन", 96, "w", "rise")]),
    (8.05, 9.85, "low", [("आज के समय में", 78, "w", "slide")]),
    (9.90, 11.90, "low", [("बिजली की ज़रूरत", 84, "w", "rise"), ("लगातार बढ़ रही है", 72, "g", "drop")]),
    (12.10, 14.90, "low", [("सोलर पैनल", 124, "g", "slam"), ("लगवाना", 92, "w", "rise")]),
    (14.90, 16.00, "low", [("खर्चे", 120, "g", "slam"), ("कम", 120, "w", "pop")]),
    (16.05, 17.45, "low", [("एक अच्छा", 80, "w", "slide"), ("कदम", 140, "l", "slam")]),
    (17.55, 19.80, "low", [("अभीरा ग्रीन एनर्जी", 86, "l", "rise"), ("के साथ", 66, "w", "slide")]),
    (19.85, 21.65, "low", [("घर", 140, "g", "slam"), ("या बिज़नेस", 96, "w", "rise")]),
    (21.70, 23.48, "low", [("ज़रूरत के हिसाब से", 62, "w", "slide"), ("सोलर सॉल्यूशन", 104, "g", "pop")]),
    (24.10, 25.90, "low", [("सूरज की", 86, "w", "rise"), ("रोशनी", 132, "g", "slam")]),
    (25.95, 27.30, "low", [("से", 70, "w", "slide"), ("बिजली", 150, "l", "pop")]),
    (27.45, 29.60, "low", [("दिन के", 84, "w", "rise"), ("समय", 132, "g", "slam")]),
    (29.65, 32.00, "low", [("ज़रूरत का हिस्सा", 80, "w", "slide"), ("पूरा", 140, "l", "pop")]),
    (32.15, 34.30, "low", [("बिल में", 92, "w", "rise"), ("बचत", 170, "g", "slam")]),
    (34.45, 36.95, "low", [("सबसे", 100, "w", "drop"), ("ख़ास बात!", 136, "g", "slam")]),
    (37.05, 38.10, "low", [("रूफटॉप सोलर", 104, "w", "pop")]),
    (38.85, 39.95, "top", [("सरकारी योजना", 92, "w", "rise")]),
    (40.00, 42.10, "top", [("सब्सिडी का लाभ", 92, "g", "slam")]),
    (42.25, 45.40, "mid", [("सिर्फ", 80, "w", "drop"), ("बढ़ते खर्चे", 150, "g", "slam"), ("के बारे में सोचिए मत", 70, "w", "rise")]),
    (45.55, 46.15, "low", [("बल्कि", 110, "w", "pop")]),
    (46.20, 48.40, "low", [("स्मार्ट सॉल्यूशन", 108, "g", "slam"), ("की तरफ कदम बढ़ाएं", 70, "w", "rise")]),
    (48.45, 51.15, "low", [("सोलर इंस्टॉलेशन", 96, "w", "rise"), ("+ सब्सिडी जानकारी", 80, "g", "slide")]),
    (54.80, 57.25, "low", [("पता", 130, "g", "slam"), ("101, कराज भवन", 84, "w", "rise")]),
    (60.55, 64.00, "mid", [("कंकड़बाग,", 78, "w", "slide"), ("पटना", 190, "g", "slam"), ("800020", 110, "w", "pop")]),
]

OUTRO_START = 74.0

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

html_videos, html_stages, html_texts, js = [], [], [], []

# --- footage + stages
cuts = []
for i, (a, b, clip, ms) in enumerate(SHOTS):
    a, b = snap(a), snap(b)
    if i > 0:
        cuts.append(a)
    if clip:
        html_videos.append(
            f'<div class="vwrap" id="vw{i}"><video id="v{i}" src="assets/clips/{clip}.mp4" '
            f'data-start="{a}" data-duration="{round(b-a,4)}" data-media-start="{ms}" '
            f'data-track-index="{i % 2}" muted playsinline></video></div>')
        # zoom-blur entry then slow push (camera never sleeps)
        js.append(f'tl.fromTo("#vw{i}",{{scale:1.16,filter:"blur(14px)"}},{{scale:1.0,filter:"blur(0px)",duration:0.4667,ease:"expo.out"}},{a});')
        js.append(f'tl.to("#vw{i}",{{scale:1.07,duration:{round(b-a-0.4667,4)},ease:"none"}},{round(a+0.4667,4)});')
    else:
        outro = abs(a - OUTRO_START) < 0.01
        sid = f"st{i}"
        inner = ""
        if outro:
            inner = ('<div class="outro"><div class="logo-disc"></div><img id="outro-logo" src="assets/logo.png" alt="">'
                     '<div class="outro-tag" id="outro-tag"><div class="ln"><span class="k w">आज की बचत,</span></div><div class="ln"><span class="k g">कल का बेहतर फ्यूचर</span></div></div>'
                     '<div class="outro-phone" id="outro-phone">संपर्क: 8809215769</div></div>')
        html_stages.append(
            f'<div class="stage clip" id="{sid}" data-start="{a}" data-duration="{round(b-a,4)}" data-track-index="2">'
            f'<div class="glow"></div><div class="grid" id="{sid}-grid"></div>{inner}</div>')
        js.append(f'tl.fromTo("#{sid}",{{scale:1.12,filter:"blur(12px)"}},{{scale:1,filter:"blur(0px)",duration:0.5,ease:"expo.out"}},{a});')
        js.append(f'tl.fromTo("#{sid}-grid",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"0px 240px",duration:{round(b-a,4)},ease:"none"}},{a});')
        if outro:
            js.append(f'tl.from("#outro-logo",{{scale:0.55,opacity:0,filter:"blur(16px)",duration:0.9,ease:"expo.out"}},{a+0.15});')
            js.append(f'tl.from("#outro-tag",{{y:50,opacity:0,duration:0.6,ease:"power3.out"}},{a+0.6});')
            js.append(f'tl.from("#outro-phone",{{y:30,opacity:0,duration:0.5,ease:"back.out(1.6)"}},{a+0.9});')
            js.append(f'tl.to("#outro-logo",{{scale:1.05,duration:{round(b-a-1.1,4)},ease:"sine.inOut"}},{a+1.05});')
            js.append(f'tl.to(["#outro-logo","#outro-tag","#outro-phone"],{{opacity:0,duration:0.6,ease:"power2.in"}},{b-0.7});')

# --- light-flash on every cut (hides the cut)
for c in cuts:
    js.append(f'tl.to("#flash",{{opacity:0.72,duration:0.1333,ease:"power2.in"}},{round(c-0.1333,4)});')
    js.append(f'tl.to("#flash",{{opacity:0,duration:0.3,ease:"power2.out"}},{c});')

# --- kinetic type
ANIM = {
    "rise":  '{y:70,opacity:0,filter:"blur(10px)",duration:0.4,ease:"expo.out"}',
    "slam":  '{scale:2.4,opacity:0,filter:"blur(12px)",duration:0.3667,ease:"back.out(1.7)"}',
    "slide": '{x:-120,opacity:0,filter:"blur(8px)",duration:0.3667,ease:"power3.out"}',
    "pop":   '{scale:0.3,opacity:0,duration:0.4667,ease:"elastic.out(1,0.55)"}',
    "drop":  '{y:-80,opacity:0,filter:"blur(8px)",duration:0.3667,ease:"power4.out"}',
}
for i, (a, b, pos, lines) in enumerate(TEXTS):
    a, b = snap(a), snap(b)
    tid = f"t{i}"
    spans = []
    for j, (txt, size, col, anim) in enumerate(lines):
        spans.append(f'<div class="ln"><span id="{tid}l{j}" class="k {col}" style="font-size:{size}px">{esc(txt)}</span></div>')
        js.append(f'tl.from("#{tid}l{j}",{ANIM[anim]},{round(a + 0.12 + j*0.14, 4)});')
    strike = ""
    if pos == "mid" and i == 21:  # strike-through on "बढ़ते खर्चे"
        strike = '<div class="strike" id="strike"></div>'
    html_texts.append(
        f'<div class="txt {pos} clip" id="{tid}" data-start="{a}" data-duration="{round(b-a,4)}" data-track-index="{3 + i % 2}">'
        f'<div class="stack">{"".join(spans)}{strike}</div></div>')
    # gentle drift while on screen
    js.append(f'tl.fromTo("#{tid} .stack",{{scale:1}},{{scale:1.045,duration:{round(b-a,4)},ease:"none"}},{a});')
    if strike:
        js.append('tl.fromTo("#strike",{scaleX:0},{scaleX:1,duration:0.3,ease:"power4.out"},44.70);')

# --- corner logo: entrance, gentle breathe, exits as the outro takes over
js.append('tl.from("#logo",{scale:0.4,opacity:0,rotation:-12,duration:0.7,ease:"back.out(1.8)"},0.2);')
js.append(f'tl.to("#logo",{{scale:1.04,duration:2,ease:"sine.inOut",yoyo:true,repeat:{int((OUTRO_START-1)/2)-1}}},1.0);')
js.append(f'tl.to("#logo",{{opacity:0,scale:0.8,duration:0.4,ease:"power2.in"}},{OUTRO_START-0.3});')
js.append('tl.from("#logo-glow",{opacity:0,duration:0.6,ease:"power2.out"},0.2);')
js.append(f'tl.to("#logo-glow",{{opacity:0,duration:0.4,ease:"power2.in"}},{OUTRO_START-0.3});')
js.append(f'tl.from(".logo-disc",{{opacity:0,scale:0.6,duration:0.9,ease:"expo.out"}},{OUTRO_START+0.1});')
js.append(f'tl.to(".logo-disc",{{opacity:0,duration:0.6,ease:"power2.in"}},{TOTAL-0.7});')
# grain jitter
js.append(f'tl.to("#grain",{{x:-40,y:-30,duration:{TOTAL},ease:"steps({int(TOTAL*12)})"}},0);')
js.append(f'tl.set({{}},{{}},{TOTAL});')

TEMPLATE = open(os.path.join(os.path.dirname(__file__), "template.html"), encoding="utf-8").read()
out = (TEMPLATE
       .replace("/*TOTAL*/", str(TOTAL))
       .replace("<!--VIDEOS-->", "\n    ".join(html_videos))
       .replace("<!--STAGES-->", "\n    ".join(html_stages))
       .replace("<!--TEXTS-->", "\n    ".join(html_texts))
       .replace("/*JS*/", "\n      ".join(js)))
open(os.path.join(os.path.dirname(__file__), "..", "index.html"), "w", encoding="utf-8").write(out)
print("index.html written:", len(SHOTS), "shots,", len(TEXTS), "text beats,", len(cuts), "cuts")
