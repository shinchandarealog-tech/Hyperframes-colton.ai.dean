import { Easing, interpolate, random, spring } from "remotion";
import { FPS, POP_FRAMES, SMART_EASE } from "../timing";

const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

/** 0..1 progress between two absolute frames with an optional easing. */
export const prog = (
  frame: number,
  from: number,
  to: number,
  easing: (t: number) => number = (t) => t,
) => interpolate(frame, [from, to], [0, 1], { ...clamp, easing });

/** Smart-side eased progress. */
export const smooth = (frame: number, from: number, len: number) =>
  prog(frame, from, from + len, SMART_EASE);

/** Linear map with clamping. */
export const lerp = (
  frame: number,
  input: number[],
  output: number[],
  easing?: (t: number) => number,
) => interpolate(frame, input, output, { ...clamp, easing });

/** "Pop": scale 0.85 -> 1.03 -> 1.0 over POP_FRAMES, plus opacity. */
export const pop = (frame: number, start: number) => {
  if (frame < start) return { scale: 0.85, opacity: 0 };
  const s = spring({
    frame: frame - start,
    fps: FPS,
    config: { damping: 12, stiffness: 260, mass: 0.6 },
    durationInFrames: POP_FRAMES,
  });
  return {
    scale: 0.85 + 0.15 * s,
    opacity: lerp(frame, [start, start + 3], [0, 1]),
  };
};

/** Hard-side "jerky" progress: linear, quantized into a few steps. */
export const jerky = (frame: number, from: number, len: number, steps = 4) => {
  const p = prog(frame, from, from + len);
  return Math.floor(p * steps) / steps;
};

/** Characters typed so far between two frames. */
export const typed = (text: string, frame: number, from: number, to: number) =>
  text.slice(0, Math.round(prog(frame, from, to) * text.length));

/** Gravity fall with one small bounce. Returns 0 (start) .. 1 (landed). */
export const fallBounce = (frame: number, start: number, len: number) => {
  const fallEnd = start + len;
  if (frame <= fallEnd) return { y: prog(frame, start, fallEnd, Easing.in(Easing.quad)), squash: 0 };
  const b = prog(frame, fallEnd, fallEnd + 8);
  const hop = Math.sin(b * Math.PI) * 0.08; // bounce height relative to fall
  return { y: 1 - hop, squash: frame < fallEnd + 2 ? 1 : 0 };
};

/** Smooth seeded noise (piecewise linear between random keys). */
export const noise = (seed: string, t: number) => {
  const i = Math.floor(t);
  const f = t - i;
  const a = random(`${seed}-${i}`) * 2 - 1;
  const b = random(`${seed}-${i + 1}`) * 2 - 1;
  return a + (b - a) * f;
};

/** Overshoot ease (4%). */
export const overshoot = Easing.out(Easing.back(1.2));
