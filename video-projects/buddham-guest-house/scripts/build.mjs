// Generates index.html for the Buddham Guest House reel.
// Shot list + caption timings are synced to assets/voiceover.mp3 (Hindi VO, 49.3s).
// Run from the project folder: node scripts/build.mjs
import { readFileSync, writeFileSync } from "node:fs";

const TOTAL = 50.5;
const HALF = 0.2; // half of each transition window (shots overlap by 2*HALF)

// [clip, source time where the shot starts (incl. transition lead-in), cut time, transition into this shot]
// Source ranges were picked from ffmpeg blurdetect scores — sharp, steady stretches only.
const SHOTS = [
  ["buddham", 0.0, 0.0, "none"], // aerial — Phulwari Sharif
  ["dipak", 1.9, 0.8, "fade"], // building — "thaharne ke liye chahiye"
  ["dipak", 11.0, 2.4, "slide"], // bed — "aaram, sukoon"
  ["phulwari", 14.25, 3.9, "fade"], // AC — "badhiya suvidhayein"
  ["phulwari", 0.0, 5.1, "slide"], // facade — "to aapka swagat hai"
  ["phulwari", 32.3, 6.55, "slide"], // signboard — "Buddham Guest House mein"
  ["dipak", 7.0, 8.7, "slide"], // teal room — "parivar ke saath"
  ["dipak", 13.0, 10.2, "fade"], // pink room — "couple stay"
  ["dipak", 17.7, 11.5, "slide"], // bed — "aaramdayak jagah chahiye"
  ["phulwari", 28.2, 13.0, "fade"], // balcony — "Buddham GH mein paaiye"
  ["dipak", 8.8, 14.8, "slide"], // fan room — "apni zaroorat ke hisaab se"
  ["phulwari", 20.3, 16.5, "slide"], // corridor — "thaharne ki suvidha"
  ["phulwari", 1.85, 17.7, "leak"], // bed — "aaramdayak kamre"
  ["dipak", 6.0, 18.75, "fade"], // white bed — "kamre"
  ["phulwari", 16.0, 19.2, "slide"], // blue room — "family aur couple stay"
  ["phulwari", 26.85, 20.1, "fade"], // room with AC — "stay ki suvidha"
  ["dipak", 28.3, 21.0, "fade"], // reception desk — "24x7 check-in"
  ["phulwari", 11.15, 22.5, "slide"], // TV — "free WiFi"
  ["dipak", 20.0, 23.7, "slide"], // bathroom — "taaki aapka har stay bane aaramdayak"
  ["buddham", 5.3, 26.5, "leak"], // Babhanpura sign — "location note kar lijiye"
  ["dipak", 35.3, 28.2, "slide"], // road — "S. Janipur road ... Shiv mandir se 200m purv"
  ["phulwari", 30.4, 32.5, "slide"], // Gonapura sign — "Gonapura road"
  ["dipak", 40.0, 33.7, "fade"], // road to building — "Phulwari Sharif, Patna ... baar baar"
  ["phulwari", 32.3, 37.1, "leak"], // signboard callback — "jagah mat dhoondhiye"
  ["phulwari", 4.0, 39.2, "slide"], // facade — "Buddham GH se aaj hi sampark kijiye"
];
const CALL_AT = 40.8;
const OUTRO_AT = 45.1;

const HL = (s) => `<span class="hl">${s}</span>`;
const ICON = {
  bed: `<svg viewBox="0 0 48 48"><path d="M5 36V12M5 28h38v8M43 28v-4a6 6 0 0 0-6-6H22v10M10 24a4 4 0 1 0 8 0a4 4 0 1 0-8 0"/></svg>`,
  family: `<svg viewBox="0 0 48 48"><circle cx="15" cy="12" r="5"/><circle cx="33" cy="12" r="5"/><circle cx="24" cy="26" r="4"/><path d="M6 40v-8a9 9 0 0 1 18 0M24 32a9 9 0 0 1 18 0v8M18 42v-4a6 6 0 0 1 12 0v4"/></svg>`,
  clock: `<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="18"/><path d="M24 13v11l7 5"/></svg>`,
  wifi: `<svg viewBox="0 0 48 48"><path d="M6 19a26 26 0 0 1 36 0M12 26a17 17 0 0 1 24 0M18 33a8 8 0 0 1 12 0"/><circle cx="24" cy="39" r="2.5"/></svg>`,
  pin: `<svg viewBox="0 0 48 48"><path d="M24 44s14-13 14-24a14 14 0 0 0-28 0c0 11 14 24 14 24z"/><circle cx="24" cy="20" r="5"/></svg>`,
  phone: `<svg viewBox="0 0 48 48"><path d="M14 6l6 10-4 4a24 24 0 0 0 12 12l4-4 10 6-3 7c-17 2-33-14-31-31z"/></svg>`,
};

// Lower-plate captions [start, end, html, icon?]
const CAPS = [
  [0.1, 2.35, `फुलवारी शरीफ़ में ठहरने के लिए चाहिए…`],
  [2.35, 5.1, `${HL("आराम")}, ${HL("सुकून")} और बढ़िया सुविधाएँ?`],
  [5.1, 8.7, `तो आपका स्वागत है ${HL("BUDDHAM GUEST HOUSE")} में!`],
  [8.7, 10.2, `चाहे परिवार के साथ ठहरना हो`],
  [10.2, 13.15, `या कपल स्टे के लिए आरामदायक जगह चाहिए`],
  [13.15, 15.2, `${HL("BUDDHAM GUEST HOUSE")} में पाइए`],
  [15.2, 17.7, `अपनी ज़रूरत के हिसाब से ठहरने की सुविधा!`],
  [17.7, 19.2, `आरामदायक ${HL("कमरे")}`, "bed"],
  [19.2, 21.1, `${HL("फैमिली")} और ${HL("कपल")} स्टे`, "family"],
  [21.1, 22.5, `${HL("24×7")} चेक-इन`, "clock"],
  [22.5, 23.7, `${HL("फ्री")} वाई-फाई`, "wifi"],
  [23.7, 26.5, `ताकि आपका हर स्टे बने ${HL("आरामदायक")}!`],
  [26.5, 35.4, `लोकेशन ${HL("नोट")} कर लीजिए`, "pin"],
  [35.4, 38.1, `तो ठहरने के लिए बार-बार जगह मत ढूँढिए!`],
  [38.1, CALL_AT + HALF, `${HL("BUDDHAM GUEST HOUSE")} से आज ही संपर्क कीजिए!`],
];

// Address lines, revealed as the VO reads them
const ADDR = [
  [28.2, `एस जानीपुर रोड, बभनपुरा`],
  [30.3, `शिव मंदिर से 200 मीटर पूर्व`],
  [32.5, `गोनापुरा रोड`],
  [33.7, `फुलवारी शरीफ़, पटना`],
];

// Kinetic words over the "aaram / sukoon / suvidhayein" beat
const SLAMS = [
  [2.4, 3.0, "आराम"],
  [3.0, 3.9, "सुकून"],
  [3.9, 5.1, "सुविधाएँ"],
];

const r3 = (n) => Math.round(n * 1000) / 1000;
const fonts = readFileSync(new URL("../assets/fonts/fonts.css", import.meta.url), "utf8");

// ---------- DOM ----------
let shotsHtml = "";
SHOTS.forEach(([clip, src, cut], i) => {
  const next = i + 1 < SHOTS.length ? SHOTS[i + 1][2] : CALL_AT;
  const start = i === 0 ? 0 : cut - HALF;
  const end = next + HALF;
  const mediaStart = src;
  shotsHtml += `
      <div class="shot" id="shot${i}" style="z-index:${i + 1}"><div class="kb" id="kb${i}">
        <video id="v${i}" src="assets/${clip}.mp4" muted playsinline data-start="${r3(start)}" data-duration="${r3(end - start)}" data-media-start="${r3(mediaStart)}" data-track-index="${1 + (i % 2)}"></video>
      </div></div>`;
});

const capsHtml = CAPS.map(
  ([, , html, icon], i) =>
    `<div class="cap${icon ? " has-icon" : ""}" id="cap${i}">${icon ? `<span class="ico">${ICON[icon]}</span>` : ""}<span class="txt">${html}</span></div>`,
).join("\n          ");

const addrHtml = ADDR.map(([, t], i) => `<div class="aline" id="al${i}"><span class="dot"></span>${t}</div>`).join("\n          ");
const slamsHtml = SLAMS.map(([, , t], i) => `<div class="slam" id="slam${i}">${t}</div>`).join("\n        ");

// ---------- Timeline ----------
let js = "";
const T = (s) => r3(s);

// Shot transitions + ken burns
SHOTS.forEach(([, , cut, tr], i) => {
  const next = i + 1 < SHOTS.length ? SHOTS[i + 1][2] : CALL_AT;
  const start = i === 0 ? 0 : cut - HALF;
  const end = next + HALF;
  // Barely-there drift so stills breathe without zooming into the room
  js += `  tl.fromTo("#kb${i}", { scale: 1.0 }, { scale: 1.03, duration: ${T(end - start)}, ease: "none" }, ${T(start)});\n`;
  if (i === 0) return;
  const t0 = T(cut - HALF);
  const D = T(2 * HALF);
  const out = `#shot${i - 1}`;
  const inn = `#shot${i}`;
  // Soft, blur-free transitions: the incoming shot is fully sharp the moment it settles.
  switch (tr) {
    case "slide":
      js += `  tl.fromTo("${inn}", { x: 1080 }, { x: 0, duration: ${D}, ease: "power3.inOut" }, ${t0});\n`;
      js += `  tl.to("${out}", { x: -320, duration: ${D}, ease: "power3.inOut" }, ${t0});\n`;
      break;
    case "up":
      js += `  tl.fromTo("${inn}", { y: 1920 }, { y: 0, duration: ${D}, ease: "power3.inOut" }, ${t0});\n`;
      js += `  tl.to("${out}", { y: -560, duration: ${D}, ease: "power3.inOut" }, ${t0});\n`;
      break;
    case "fade":
      js += `  tl.fromTo("${inn}", { opacity: 0 }, { opacity: 1, duration: ${D}, ease: "sine.inOut" }, ${t0});\n`;
      break;
    case "leak":
      js += `  tl.fromTo("${inn}", { opacity: 0 }, { opacity: 1, duration: ${D}, ease: "sine.inOut" }, ${t0});\n`;
      js += `  tl.fromTo("#leak", { opacity: 0, scale: 0.8 }, { opacity: 0.75, scale: 1.2, duration: 0.25, ease: "sine.out", immediateRender: false }, ${t0});\n`;
      js += `  tl.to("#leak", { opacity: 0, scale: 1.5, duration: 0.4, ease: "sine.in" }, ${T(cut + 0.05)});\n`;
      break;
  }
});

// Lower plate
js += `  tl.from("#plate", { scaleX: 0.2, opacity: 0, duration: 0.45, ease: "back.out(1.4)" }, 0.1);\n`;
CAPS.forEach(([s, e, , icon], i) => {
  js += `  tl.fromTo("#cap${i}", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, ${T(s)});\n`;
  js += `  tl.fromTo("#cap${i} .hl", { color: "#FFF6E6" }, { color: "#F7B731", duration: 0.25, ease: "power1.out", stagger: 0.18 }, ${T(s + 0.15)});\n`;
  if (icon) js += `  tl.from("#cap${i} .ico", { scale: 0, rotation: -40, duration: 0.4, ease: "back.out(2.2)" }, ${T(s + 0.05)});\n`;
  if (i < CAPS.length - 1) js += `  tl.set("#cap${i}", { opacity: 0 }, ${T(e)});\n`;
});

// Location chip over the opening aerial
js += `  tl.from("#band .bt", { opacity: 0, x: -40, duration: 0.5, ease: "power2.out" }, 0.35);\n`;
js += `  tl.from("#band .bs", { opacity: 0, x: -30, duration: 0.5, ease: "power2.out" }, 0.5);\n`;


// Word slams
SLAMS.forEach(([s, e], i) => {
  js += `  tl.fromTo("#slam${i}", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power2.out" }, ${T(s)});\n`;
  if (i < SLAMS.length - 1) js += `  tl.set("#slam${i}", { opacity: 0 }, ${T(e)});\n`;
});

// Logo badge pops on "Buddham Guest House"
js += `  tl.from("#badge", { scale: 0, rotation: -90, duration: 0.6, ease: "back.out(1.6)" }, 0.3);\n`;
js += `  tl.fromTo("#badge .shine", { x: -260 }, { x: 260, duration: 0.7, ease: "power2.inOut" }, 7.5);\n`;
js += `  tl.fromTo("#badge .shine", { x: -260 }, { x: 260, duration: 0.7, ease: "power2.inOut", immediateRender: false }, 13.3);\n`;
js += `  tl.fromTo("#badge .shine", { x: -260 }, { x: 260, duration: 0.7, ease: "power2.inOut", immediateRender: false }, 38.2);\n`;

// Address card
js += `  tl.from("#addr", { y: 80, opacity: 0, scale: 0.9, duration: 0.5, ease: "back.out(1.5)" }, 27.9);\n`;
js += `  tl.from("#addr .apin", { y: -70, opacity: 0, duration: 0.5, ease: "bounce.out" }, 28.0);\n`;
ADDR.forEach(([s], i) => {
  js += `  tl.from("#al${i}", { x: -60, opacity: 0, duration: 0.35, ease: "expo.out" }, ${T(s)});\n`;
  js += `  tl.from("#al${i} .dot", { scale: 0, duration: 0.3, ease: "back.out(3)" }, ${T(s + 0.1)});\n`;
});

// Call-now card (iris open from the centre)
js += `  tl.fromTo("#call", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(100% at 50% 50%)", duration: 0.5, ease: "power3.inOut" }, ${T(CALL_AT - HALF)});\n`;
js += `  tl.fromTo("#call .rays", { rotation: 0 }, { rotation: 40, duration: 4.6, ease: "none" }, ${T(CALL_AT - HALF)});\n`;
js += `  tl.from("#call .pbtn", { scale: 0, duration: 0.5, ease: "back.out(2)" }, ${T(CALL_AT + 0.1)});\n`;
js += `  tl.to("#call .pbtn svg", { rotation: 14, duration: 0.07, ease: "none", yoyo: true, repeat: 9 }, ${T(CALL_AT + 0.7)});\n`;
js += `  tl.to("#call .pbtn svg", { rotation: 14, duration: 0.07, ease: "none", yoyo: true, repeat: 9 }, ${T(CALL_AT + 2.4)});\n`;
js += `  tl.fromTo("#call .ring", { scale: 1, opacity: 0.7 }, { scale: 2.2, opacity: 0, duration: 1.1, ease: "power1.out", stagger: 0.35, repeat: 2 }, ${T(CALL_AT + 0.6)});\n`;
js += `  tl.from("#call .k1", { y: 50, opacity: 0, duration: 0.4, ease: "expo.out" }, ${T(CALL_AT + 0.1)});\n`;
js += `  tl.from("#call .k2", { y: 40, opacity: 0, duration: 0.4, ease: "power3.out" }, ${T(CALL_AT + 0.25)});\n`;
js += `  tl.from("#call .dg", { y: 70, opacity: 0, scale: 0.5, duration: 0.3, ease: "back.out(2)", stagger: 0.09 }, ${T(CALL_AT + 0.9)});\n`;
js += `  tl.from("#call .uline", { scaleX: 0, duration: 0.6, ease: "power2.out" }, ${T(CALL_AT + 2.2)});\n`;
js += `  tl.from("#call .k3", { opacity: 0, y: 20, duration: 0.4, ease: "power2.out" }, ${T(CALL_AT + 2.5)});\n`;

// Outro (cream iris from the phone button)
js += `  tl.fromTo("#outro", { clipPath: "circle(0% at 50% 40%)" }, { clipPath: "circle(130% at 50% 40%)", duration: 0.6, ease: "power3.inOut" }, ${T(OUTRO_AT - HALF)});\n`;
js += `  tl.fromTo("#outro .rays", { rotation: 0 }, { rotation: 25, duration: ${T(TOTAL - OUTRO_AT + HALF)}, ease: "none" }, ${T(OUTRO_AT - HALF)});\n`;
js += `  tl.from("#outro .logo", { scale: 0.6, opacity: 0, filter: "blur(14px)", duration: 0.9, ease: "expo.out" }, ${T(OUTRO_AT + 0.2)});\n`;
js += `  tl.to("#outro .logo", { scale: 1.04, duration: ${T(TOTAL - OUTRO_AT - 1.1)}, ease: "none" }, ${T(OUTRO_AT + 1.1)});\n`;
js += `  tl.from("#outro .t1", { y: 50, opacity: 0, duration: 0.5, ease: "power3.out" }, 46.95);\n`;
js += `  tl.from("#outro .t2", { y: 50, opacity: 0, duration: 0.5, ease: "back.out(1.6)" }, 48.15);\n`;
js += `  tl.from("#outro .pill", { y: 40, opacity: 0, duration: 0.5, ease: "expo.out" }, 48.9);\n`;
js += `  tl.from("#outro .loc", { opacity: 0, duration: 0.5, ease: "power1.out" }, 49.2);\n`;

// Grain jitter (deterministic)
js += `  tl.to("#grain", { backgroundPosition: "137px 59px", duration: 0.1, ease: "steps(1)", repeat: ${Math.ceil(TOTAL / 0.2) - 1}, yoyo: true }, 0);\n`;
js += `  tl.to({}, { duration: ${TOTAL} }, 0);\n`;

const html = `<!doctype html>
<html lang="hi" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
${fonts}
      :root {
        --navy: #14215E;
        --saffron: #F28C1B;
        --gold: #F7B731;
        --leaf: #2E7D32;
        --cream: #FFF6E6;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0b1136; }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0b1136; font-family: "Baloo 2", sans-serif; }
      .shot { position: absolute; inset: 0; overflow: hidden; }
      .kb { position: absolute; inset: 0; }
      .kb video { width: 100%; height: 100%; object-fit: cover; display: block; }

      #grade { position: absolute; inset: 0; z-index: 40; pointer-events: none;
        background: radial-gradient(ellipse 85% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(8,10,40,0.55) 100%),
                    linear-gradient(180deg, rgba(10,14,50,0.45) 0%, rgba(10,14,50,0) 16%, rgba(10,14,50,0) 62%, rgba(10,14,50,0.55) 100%); }
      #grain { position: absolute; inset: -20px; z-index: 95; pointer-events: none; opacity: 0.09; mix-blend-mode: overlay;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='7'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
      #leak { position: absolute; left: -200px; top: 300px; width: 1480px; height: 1480px; z-index: 45; pointer-events: none; opacity: 0;
        background: radial-gradient(circle, rgba(255,214,120,0.95) 0%, rgba(247,183,49,0.7) 25%, rgba(242,140,27,0.35) 50%, rgba(242,140,27,0) 70%); mix-blend-mode: screen; }

      /* Opening location chip */
      /* Top brand band — hides the clips' old burned-in titles; text sits below Instagram's top bar */
      #band { position: absolute; left: 0; right: 0; top: 0; height: 330px; z-index: 56; padding: 150px 250px 0 54px;
        background: linear-gradient(180deg, #0f1a52 0%, #1b2a73 100%); border-bottom: 6px solid var(--gold);
        box-shadow: 0 10px 30px rgba(0,0,0,0.35); display: flex; flex-direction: column; gap: 6px; }
      #band .bt { color: var(--cream); font-family: "Poppins", sans-serif; font-weight: 800; font-size: 58px; line-height: 1.1; white-space: nowrap; }
      #band .bs { color: var(--gold); font-size: 40px; font-weight: 600; line-height: 1.2; white-space: nowrap; }
      #foot { position: absolute; left: 0; right: 0; bottom: 0; height: 160px; z-index: 55;
        background: linear-gradient(180deg, #1b2a73 0%, #0e1646 100%); border-top: 4px solid var(--gold); }
      #hook .chip { display: flex; align-items: center; gap: 18px; padding: 14px 40px 14px 18px; border-radius: 999px;
        background: rgba(20,33,94,0.88); border: 3px solid var(--gold); color: var(--cream); font-size: 54px; font-weight: 800; line-height: 1.1; }
      #hook .ico { width: 70px; height: 70px; border-radius: 50%; background: var(--saffron); display: grid; place-items: center; }
      #hook .ico svg { width: 44px; height: 44px; fill: none; stroke: #fff; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }

      /* Kinetic slams */
      .slam { position: absolute; left: 0; right: 0; top: 400px; z-index: 50; text-align: center; font-size: 170px; font-weight: 800; line-height: 1.2;
        color: var(--cream); text-shadow: 0 0 40px rgba(247,183,49,0.85), 0 8px 0 var(--saffron), 0 14px 30px rgba(0,0,0,0.55); }

      /* Logo badge */
      #badge { position: absolute; top: 140px; right: 44px; width: 170px; height: 170px; border-radius: 50%; z-index: 90; overflow: hidden;
        background: var(--cream); border: 6px solid var(--gold); box-shadow: 0 10px 30px rgba(0,0,0,0.45), 0 0 30px rgba(247,183,49,0.5);
        display: grid; place-items: center; }
      #badge img { width: 144px; height: auto; margin-top: 6px; }
      #badge .shine { position: absolute; top: -40px; left: 50%; width: 60px; height: 280px; margin-left: -30px; transform: rotate(25deg);
        background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.85), rgba(255,255,255,0)); }

      /* Lower caption plate */
      #plate { position: absolute; left: 48px; right: 48px; bottom: 330px; height: 290px; z-index: 60; border-radius: 34px;
        background: linear-gradient(160deg, rgba(27,42,115,0.96), rgba(14,22,70,0.96)); border: 4px solid rgba(247,183,49,0.9);
        box-shadow: 0 18px 50px rgba(0,0,0,0.55), inset 0 0 40px rgba(247,183,49,0.12); }
      #plate::before { content: ""; position: absolute; left: 40px; right: 40px; top: -4px; height: 8px; border-radius: 8px;
        background: linear-gradient(90deg, var(--saffron), var(--gold), var(--saffron)); }
      .cap { position: absolute; inset: 0; padding: 26px 110px; display: flex; align-items: center; justify-content: center; gap: 28px;
        color: var(--cream); font-size: 64px; font-weight: 800; line-height: 1.25; text-align: center; opacity: 0; }
      .cap.has-icon { font-size: 84px; }
      .cap .txt { max-width: 900px; }
      .cap .hl { color: var(--gold); }
      .cap .ico { flex: 0 0 auto; width: 130px; height: 130px; border-radius: 50%; background: var(--saffron); display: grid; place-items: center;
        box-shadow: 0 0 0 8px rgba(242,140,27,0.25); }
      .cap .ico svg { width: 80px; height: 80px; fill: none; stroke: #fff; stroke-width: 3.6; stroke-linecap: round; stroke-linejoin: round; }

      /* Address card */
      #addr { position: absolute; left: 60px; right: 150px; bottom: 646px; z-index: 58; padding: 40px 50px 44px; border-radius: 30px;
        background: rgba(255,246,230,0.97); border: 4px solid var(--saffron); box-shadow: 0 18px 50px rgba(0,0,0,0.5);
        display: flex; flex-direction: column; gap: 14px; }
      #addr .ahead { display: flex; align-items: center; gap: 20px; white-space: nowrap; color: var(--navy); font-size: 54px; font-weight: 800; line-height: 1.1;
        padding-bottom: 14px; border-bottom: 4px solid rgba(242,140,27,0.5); }
      #addr .apin { width: 84px; height: 84px; border-radius: 50%; background: var(--saffron); display: grid; place-items: center; }
      #addr .apin svg { width: 52px; height: 52px; fill: none; stroke: #fff; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }
      .aline { display: flex; align-items: center; gap: 22px; color: var(--navy); font-size: 54px; font-weight: 600; line-height: 1.25; }
      .aline .dot { flex: 0 0 auto; width: 22px; height: 22px; border-radius: 50%; background: var(--leaf); box-shadow: 0 0 0 6px rgba(46,125,50,0.2); }

      /* Call card */
      #call { position: absolute; inset: 0; z-index: 70; overflow: hidden;
        background: radial-gradient(circle at 50% 42%, #2a3c9a 0%, #14215E 45%, #0a1140 100%);
        display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 30px; padding: 0 60px 120px; }
      .rays { position: absolute; left: 50%; top: 42%; width: 2600px; height: 2600px; margin: -1300px 0 0 -1300px; opacity: 0.16; pointer-events: none;
        background: repeating-conic-gradient(from 0deg, rgba(247,183,49,1) 0deg 6deg, rgba(247,183,49,0) 6deg 18deg);
        -webkit-mask-image: radial-gradient(circle, #000 0%, rgba(0,0,0,0) 60%); mask-image: radial-gradient(circle, #000 0%, rgba(0,0,0,0) 60%); }
      #call .pwrap { position: relative; width: 240px; height: 240px; display: grid; place-items: center; margin-bottom: 20px; }
      #call .ring { position: absolute; inset: 0; border-radius: 50%; border: 6px solid var(--gold); }
      #call .pbtn { position: relative; width: 240px; height: 240px; border-radius: 50%; display: grid; place-items: center;
        background: radial-gradient(circle at 35% 30%, #ffb35c, var(--saffron) 60%, #d86f00); box-shadow: 0 0 60px rgba(247,183,49,0.7); }
      #call .pbtn svg { width: 120px; height: 120px; fill: #fff; stroke: #fff; stroke-width: 2; stroke-linejoin: round; }
      #call .k1 { position: relative; color: var(--cream); font-size: 120px; font-weight: 800; line-height: 1.1; }
      #call .k2 { position: relative; color: var(--gold); font-family: "Poppins", sans-serif; font-size: 50px; font-weight: 600; letter-spacing: 0.32em; }
      #call .num { position: relative; display: flex; gap: 2px; font-family: "Poppins", sans-serif; font-weight: 800; font-size: 128px; color: #fff;
        font-variant-numeric: tabular-nums; text-shadow: 0 0 30px rgba(247,183,49,0.6); margin-top: 10px; }
      #call .num .sep { color: var(--saffron); }
      #call .uline { position: relative; width: 820px; height: 10px; border-radius: 10px; background: linear-gradient(90deg, var(--saffron), var(--gold)); }
      #call .k3 { position: relative; color: var(--cream); font-size: 54px; font-weight: 600; opacity: 0.92; margin-top: 10px; }

      /* Outro */
      #outro { position: absolute; inset: 0; z-index: 80; overflow: hidden;
        background: radial-gradient(circle at 50% 33%, #fffdf6 0%, var(--cream) 45%, #f8e3bf 100%);
        display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 120px 60px 300px; gap: 26px; }
      #outro .rays { top: 30%; opacity: 0.22; }
      #outro .logo { position: relative; width: 900px; height: auto; }
      #outro .t1, #outro .t2 { position: relative; font-family: "Poppins", sans-serif; font-weight: 800; font-size: 82px; line-height: 1.1; color: var(--navy); }
      #outro .t2 { color: var(--saffron); margin-top: -10px; }
      #outro .pill { position: relative; margin-top: 40px; display: flex; align-items: center; gap: 22px; padding: 18px 44px 18px 22px; border-radius: 999px;
        background: var(--navy); color: #fff; font-family: "Poppins", sans-serif; font-weight: 800; font-size: 64px; }
      #outro .pill .pi { width: 84px; height: 84px; border-radius: 50%; background: var(--saffron); display: grid; place-items: center; }
      #outro .pill svg { width: 50px; height: 50px; fill: #fff; }
      #outro .loc { position: relative; color: var(--leaf); font-size: 54px; font-weight: 800; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${TOTAL}" data-width="1080" data-height="1920">
${shotsHtml}

      <div id="grade"></div>
      <div id="leak"></div>

      <div id="band" class="clip" data-start="0" data-duration="${r3(CALL_AT + HALF)}" data-track-index="5">
        <div class="bt">BUDDHAM GUEST HOUSE</div>
        <div class="bs">फुलवारी शरीफ़, पटना · 790-310-2149</div>
      </div>
      <div id="foot" class="clip" data-start="0" data-duration="${r3(CALL_AT + HALF)}" data-track-index="12"></div>

      <div id="slams" class="clip" data-start="2.4" data-duration="2.7" data-track-index="6">
        ${slamsHtml}
      </div>

      <div id="badge" class="clip" data-start="0" data-duration="${TOTAL}" data-track-index="7">
        <img src="assets/emblem.png" alt="Buddham Guest House" /><div class="shine"></div>
      </div>

      <div id="addr" class="clip" data-start="27.9" data-duration="${r3(35.4 + HALF - 27.9)}" data-track-index="8">
        <div class="ahead"><span class="apin">${ICON.pin}</span>BUDDHAM GUEST HOUSE</div>
          ${addrHtml}
      </div>

      <div id="plate" class="clip" data-start="0.1" data-duration="${r3(CALL_AT + HALF - 0.1)}" data-track-index="9">
          ${capsHtml}
      </div>

      <div id="call" class="clip" data-start="${r3(CALL_AT - HALF)}" data-duration="${r3(OUTRO_AT - CALL_AT + 2 * HALF + 0.3)}" data-track-index="10">
        <div class="rays"></div>
        <div class="pwrap"><div class="ring"></div><div class="ring"></div><div class="ring"></div><div class="pbtn">${ICON.phone}</div></div>
        <div class="k1">अभी कॉल करें</div>
        <div class="k2">CALL NOW</div>
        <div class="num">${"790-310-2149"
          .split("")
          .map((c) => `<span class="dg${c === "-" ? " sep" : ""}">${c}</span>`)
          .join("")}</div>
        <div class="uline"></div>
        <div class="k3">BUDDHAM GUEST HOUSE, फुलवारी शरीफ़</div>
      </div>

      <div id="outro" class="clip" data-start="${r3(OUTRO_AT - HALF)}" data-duration="${r3(TOTAL - OUTRO_AT + HALF)}" data-track-index="11">
        <div class="rays"></div>
        <img class="logo" src="assets/logo.png" alt="Buddham Guest House logo" />
        <div class="t1">Stay Peacefully…</div>
        <div class="t2">Feel Like Home!</div>
        <div class="pill"><span class="pi">${ICON.phone}</span>790-310-2149</div>
        <div class="loc">फुलवारी शरीफ़, पटना</div>
      </div>

      <div id="grain"></div>

      <audio id="mix" src="assets/mix.m4a" data-start="0" data-duration="${TOTAL}" data-track-index="20" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
${js}      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;

writeFileSync(new URL("../index.html", import.meta.url), html);
console.log("wrote index.html");
