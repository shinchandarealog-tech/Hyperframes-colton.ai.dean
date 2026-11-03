// Beat sheet: one spoken keyword = one card. Times come from word-level Whisper (Hindi, chunked)
// and land ~0.1–0.25s ahead of the spoken word. The 24–30s section is timed from the phrase
// transcript + shot cuts (word timing failed under the launch-event music).
export const DURATION = 55.2;

export const BEATS = [
  // --- HOOK ---------------------------------------------------------------------------
  { t: 0.27, end: 0.84, kind: "hero", text: "MG" },                                   // "MG ne…"
  { t: 0.84, end: 1.68, kind: "hero", text: "BAWAAL", sub: "launch" },               // "bawaal launch"
  { t: 1.9, end: 3.6, kind: "num", text: "1000+ KM", sub: "range" },                 // "ek hazaar se zyada km"
  { t: 3.6, end: 4.36, kind: "hero", text: "FULL CHARGE" },                           // "full charge mein"
  { t: 4.36, end: 5.37, kind: "hero", text: "HECTOR" },                               // "MG Hector"
  { t: 5.37, end: 6.44, endB: 5.75, kind: "hero", text: "TOMAHAWK" },
  { t: 5.75, end: 6.44, kind: "stack", lines: ["PHEV"], ld: [0] },                 // covers burned caption               // "Tomahawk PHEV"
  // --- WHAT IS PHEV -------------------------------------------------------------------
  { t: 6.44, end: 8.8, kind: "stack", lines: ["PLUG-IN", "HYBRID", "ELECTRIC VEHICLE"], ld: [0.22, 0.68, 1.2] },
  { t: 9.0, end: 9.8, kind: "num", text: "9 SEC", sub: "sirf" },                     // "sirf 9 second"
  { t: 9.8, end: 11.96, kind: "num", text: "0–100", sub: "km/h" },                   // "100 km/h"
  // --- V2H STORY ----------------------------------------------------------------------
  { t: 12.45, end: 14.2, kind: "hero", text: "INVERTER?", sub: "ghar mein nahi?" },  // "inverter nahi"
  { t: 14.2, end: 15.95, kind: "hero", text: "DIWALI", sub: "no tension" },          // "Diwali… tension nahi"
  { t: 15.95, end: 17.8, kind: "hero", text: "POWER BACKUP", sub: "gaadi se ghar tak" },
  { t: 17.8, end: 18.68, kind: "hero", text: "LIGHTS ON" },                           // "lights jala sakte ho"
  { t: 18.9, end: 21.9, kind: "stack", lines: ["V2H", "VEHICLE TO HOME"], ld: [0.15, 0.55] },
  { t: 21.9, end: 24.2, kind: "num", text: "62 CM", sub: "HD grand view display" },
  { t: 24.2, end: 27.2, kind: "num", text: "70+", sub: "features" },
  // --- LAUNCH EVENT -------------------------------------------------------------------
  { t: 27.2, end: 28.36, kind: "hero", text: "LAUNCH EVENT" },
  { t: 28.36, end: 30.16, kind: "hero", text: "LIVE", sub: "full experience" },
  // --- CTA ----------------------------------------------------------------------------
  { t: 30.16, end: 31.5, kind: "hero", text: "BAWAAL" },                              // callback to the hook
  { t: 31.5, end: 33.15, kind: "hero", text: "1 REEL?", sub: "mushkil hai", front: true },
  { t: 33.15, end: 34.35, kind: "cta", text: "DESCRIPTION" },
  { t: 34.35, end: 36.9, kind: "hero", text: "PRICE", sub: "in description", front: true },
  { t: 36.9, end: 38.4, kind: "cta", text: "COMMENT" },
  { t: 38.4, end: 39.25, kind: "hero", text: "ENJOY" },
  { t: 39.25, end: 41.4, kind: "hero", text: "CINEMATIC", sub: "shots" },
  // --- PAYOFF + OUTRO -----------------------------------------------------------------
  { t: 42.35, end: 50.95, kind: "price", text: "₹25.69 L*", sub: "ex-showroom · approx", subB: "ex-showroom approx" },
  { t: 50.95, end: 55.2, kind: "end", lines: ["HECTOR", "TOMAHAWK"], sub: "PHEV", ld: [0, 0.3] },
];

// Host on screen → person matte active (text can sit behind his head).
export const MATTE_ON = [[0, 1.68], [4.36, 20.72], [22.52, 26.16], [27.2, 28.36], [30.16, 39.84]];

// Punch-in jump zooms inside long takes (plate + matte move together). Never during the
// burned-caption windows, so the cover masks stay aligned.
export const ZOOMS = [
  [0, 1], [0.84, 1.1], [1.68, 1], [4.9, 1.12], [5.75, 1], [9.8, 1.14], [11.96, 1],
  [13.3, 1.14], [14.2, 1], [15.95, 1.16], [17.8, 1.05], [18.68, 1], [24.2, 1.12], [26.16, 1],
  [31.5, 1.15], [33.15, 1], [34.35, 1.14], [36.9, 1], [37.6, 1.12], [38.4, 1], [39.84, 1],
];

// Blur + darken patches over the burned-in captions of the source edit.
export const MASKS = [
  { t: 5.75, end: 8.85, x: 0, y: 1370, w: 1080, h: 350 },     // "MG HECTOR TOMAHAWK PHEV"
  { t: 18.85, end: 22.15, x: 0, y: 1340, w: 1080, h: 310 },   // "V2H TECHNOLOGY"
  { t: 42.3, end: 50.95, x: 190, y: 240, w: 710, h: 200 },   // "EX SHOWROOM PRIZE 25.69…"
];

export const FLASHES = [1.68, 11.96, 27.2, 39.84, 50.95];

// One SFX per beat max; subtle under the VO + original music.
export const SFX = [
  { t: 0.27, f: "slam.mp3", d: 1.0, v: 0.28 },
  { t: 1.64, f: "whoosh.mp3", d: 0.57, v: 0.3 },
  { t: 4.36, f: "hard-cut.mp3", d: 0.2, v: 0.35 },
  { t: 6.5, f: "whoosh.mp3", d: 0.57, v: 0.25 },
  { t: 9.8, f: "slam.mp3", d: 1.0, v: 0.22 },
  { t: 11.92, f: "whoosh.mp3", d: 0.57, v: 0.3 },
  { t: 14.2, f: "hard-cut.mp3", d: 0.2, v: 0.35 },
  { t: 18.9, f: "power-up.mp3", d: 1.2, v: 0.2 },
  { t: 24.2, f: "click.wav", d: 0.46, v: 0.35 },
  { t: 27.16, f: "whoosh.mp3", d: 0.57, v: 0.3 },
  { t: 30.16, f: "slam.mp3", d: 1.0, v: 0.22 },
  { t: 33.15, f: "click.wav", d: 0.46, v: 0.35 },
  { t: 36.9, f: "hard-cut.mp3", d: 0.2, v: 0.35 },
  { t: 39.8, f: "whoosh.mp3", d: 0.57, v: 0.3 },
  { t: 42.35, f: "slam.mp3", d: 1.0, v: 0.25 },
  { t: 50.9, f: "whoosh.mp3", d: 0.57, v: 0.3 },
];
