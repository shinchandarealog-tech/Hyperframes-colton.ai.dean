import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadCaveat } from "@remotion/google-fonts/Caveat";
import { loadFont as loadLocal } from "@remotion/fonts";
import { staticFile } from "remotion";
import { hasStatic } from "./lib/files";

// ---------- Fonts ----------
// Prefer the self-hosted copies in public/fonts (offline, deterministic renders);
// fall back to Google Fonts when they are missing.
const LOCAL_INTER = "fonts/inter-latin-var.woff2";
const LOCAL_CAVEAT = "fonts/caveat-700.woff2";

const interFamily = (() => {
  if (hasStatic(LOCAL_INTER)) {
    loadLocal({ family: "Inter", url: staticFile(LOCAL_INTER), weight: "100 900" });
    return "Inter";
  }
  return loadInter("normal", { weights: ["500", "600", "700", "900"], subsets: ["latin"] }).fontFamily;
})();

const caveatFamily = (() => {
  if (hasStatic(LOCAL_CAVEAT)) {
    loadLocal({ family: "Caveat", url: staticFile(LOCAL_CAVEAT), weight: "700" });
    return "Caveat";
  }
  return loadCaveat("normal", { weights: ["700"], subsets: ["latin"] }).fontFamily;
})();

export const FONTS = {
  inter: interFamily,
  caveat: caveatFamily,
};

// ---------- Colors ----------
export const COLORS = {
  pageBg: "#0D0E0D",
  glow: "#1B1F1B",
  topPanel: "#2B2B2B",
  bottomPanel: "#111311",
  divider: "#3A3A3A",
  green: "#2FD06B",
  onGreen: "#06210F",
  red: "#F0645A",
  white: "#FFFFFF",
  muted: "#9AA196",
  card: "#FFFFFF",
  // UI-internal colors (only used *inside* white cards / mock-ups)
  cardText: "#1B1D1B",
  cardMuted: "#8A8F87",
  bubble: "#EEF0EC",
  hardInk: "#C9C9C9",
  hardMid: "#5A5A5A",
  hardDark: "#3B3B3B",
};

export const CARD_RADIUS = 28;
export const CARD_SHADOW = "0 20px 60px rgba(0,0,0,0.45)";

// Hard-way grade + texture
export const HARD_FILTER = "saturate(0.2) contrast(0.95)";
export const GRAIN_OPACITY = 0.15;

// ---------- Layout (1080 x 1920) ----------
export const W = 1080;
export const H = 1920;
export const LAYOUT = {
  topPanel: { y: 0, h: 957 },
  divider: { y: 957, h: 6 },
  bottomPanel: { y: 963, h: 957 },
  labelX: 80,
  topLabelY: 260,
  bottomLabelY: 1020,
  timerRightX: 860,
  topStepY: 334,
  bottomStepY: 1100,
  // safe zones for text
  topContent: { y0: 330, y1: 930 },
  bottomContent: { y0: 1080, y1: 1500 },
  safeRight: 940,
};

// ---------- Type sizes ----------
export const TYPE = {
  label: 46,
  timer: 52,
  step: 30,
  hook: 84,
  note: 44,
  message: 96,
};

// ---------- Copy ----------
export const COPY = {
  hook: ["Same video.", "Same deadline.", "Two editors."],
  topLabel: "THE HARD WAY",
  bottomLabel: "THE SMART WAY",
  message: ["Work smarter,", "not longer."],
  cta: {
    comment: "Comment",
    keyword: "“EDIT”",
    line: "for my exact prompts",
    handle: "@hey.rishish",
  },
};
