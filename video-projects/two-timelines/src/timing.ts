import { Easing } from "remotion";

export const FPS = 30;
export const DURATION = 900;

// ---------- Shots (absolute frames, inclusive start, exclusive end) ----------
export const SHOTS = {
  hook: { from: 0, to: 60 },
  split: { from: 60, to: 120 },
  script: { from: 120, to: 240 },
  cuts: { from: 240, to: 360 },
  captions: { from: 360, to: 450 },
  broll: { from: 450, to: 540 },
  grind: { from: 540, to: 660 },
  exportShot: { from: 660, to: 750 },
  message: { from: 750, to: 840 },
  cta: { from: 840, to: 900 },
} as const;

export type ShotKey = keyof typeof SHOTS;
export const dur = (k: ShotKey) => SHOTS[k].to - SHOTS[k].from;

// ---------- Motion ----------
export const SMART_EASE = Easing.bezier(0.22, 1, 0.36, 1);
export const POP_FRAMES = 10;
export const WIGGLE = {
  start: 80,
  amp: 2,
  ampGrind: 4,
  perSecond: 6,
};

// ---------- Shot 1 ----------
export const HOOK = {
  lineStarts: [0, 15, 30],
  lineIn: 6,
  underline: { from: 30, to: 45 },
};

// ---------- Shot 2 ----------
export const SPLIT = {
  panelsIn: { from: 60, to: 72 },
  hookOut: { from: 60, to: 66 },
  divider: { from: 70, to: 80 },
  labelsType: 74,
  framesPerChar: 2,
  timersIn: 84,
  textureStart: 80,
};

// ---------- Timers ----------
// [frame, top minutes, bottom minutes]
export const TIMER_KEYS: [number, number, number][] = [
  [100, 0, 0],
  [239, 70, 5],
  [359, 185, 12],
  [449, 260, 18],
  [539, 340, 24],
  [659, 410, 40],
  [672, 450, 45],
];
export const TIMER_BLINK_EVERY = 15;
export const TIMERS_OUT = 750;

// ---------- Shot 3 ----------
export const SCRIPT = {
  cursorBlink: 15,
  paperBalls: [150, 180, 210],
  paperFall: 14,
  cardIn: 120,
  typing: { from: 125, to: 160 },
  reply: { from: 165, to: 220 },
  check: 222,
};

// ---------- Shot 4 ----------
export const CUTS = {
  pan: 400,
  scrubPeriod: 40,
  cardIn: 240,
  typing: { from: 244, to: 268 },
  transcriptIn: 272,
  strikeStart: 290,
  strikeLen: 5,
  strikeStagger: 8,
  struckLines: [1, 3], // 0-based -> lines 2 and 4
  chip: 306,
};

// ---------- Shot 5 ----------
export const CAPTIONS = {
  typeStart: 363,
  framesPerLetter: 3,
  squiggle: 400,
  deleteFrom: 410,
  deleteTo: 418,
  cardIn: 360,
  typing: { from: 364, to: 390 },
  srtIn: 394,
  flyStart: 420,
  flyLen: 8,
  flyStagger: 6,
  chip: 436,
};

// ---------- Shot 6 ----------
export const BROLL = {
  tabsStart: 12,
  tabsEnd: 47,
  tabEvery: 2,
  cardIn: 450,
  typing: { from: 453, to: 466 },
  ideaStarts: [470, 475, 480],
  ideaLen: 9,
  ideaTravel: 300,
};

// ---------- Shot 7 ----------
export const GRIND = {
  cups: [550, 570, 590, 610],
  clipSnaps: [560, 580, 600, 620],
  clipLen: 4,
  squash: 2,
};

// ---------- Shot 8 ----------
export const EXPORT = {
  topCrawlTo: 700,
  topPercent: 12,
  errorText: 700,
  bottomFill: { from: 660, to: 672 },
  slam: 672,
  slamLen: 6,
  shakeLen: 2,
  sparkLen: 10,
};

// ---------- Shot 9 ----------
export const MESSAGE = {
  wipe: { from: 750, to: 762 },
  wordsStart: 765,
  wordStagger: 4,
  wordRise: 40,
  wordIn: 8,
  highlight: { from: 775, len: 8 },
};

// ---------- Shot 10 ----------
export const CTA = {
  lineStarts: [840, 845, 850, 855],
  pulseFrom: 870,
  pulsePeriod: 15,
};

// ---------- Music ----------
// Frame of the beat drop *inside public/music.mp3* (measured from the track start).
export const MUSIC_DROP_IN_TRACK_FRAMES = 633; // bundled bed: hit at ~21.1s
// The frame of the video the drop should land on.
export const MUSIC_DROP_TARGET = 660;
// Manual nudge. Positive = music plays later, negative = earlier.
export const MUSIC_OFFSET_FRAMES = 0;
export const MUSIC_VOLUME = 0.35;
export const SFX_VOLUME = 0.6;
