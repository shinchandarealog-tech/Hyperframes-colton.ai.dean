import React from "react";
import { interpolate } from "remotion";
import { COLORS, FONTS, LAYOUT, TYPE, W } from "../theme";
import { SPLIT, TIMER_BLINK_EVERY, TIMER_KEYS } from "../timing";
import { lerp } from "../lib/anim";

const minutesAt = (frame: number, side: "top" | "bottom") =>
  interpolate(
    frame,
    TIMER_KEYS.map((k) => k[0]),
    TIMER_KEYS.map((k) => (side === "top" ? k[1] : k[2])),
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

export const formatTimer = (mins: number, side: "top" | "bottom") => {
  const m = Math.floor(mins);
  if (side === "bottom") return `${m}m`;
  return `${Math.floor(m / 60)}h ${String(m % 60).padStart(2, "0")}m`;
};

export const Timer: React.FC<{ frame: number; side: "top" | "bottom" }> = ({ frame, side }) => {
  if (frame < SPLIT.timersIn) return null;
  const freezeAt = TIMER_KEYS[TIMER_KEYS.length - 1][0];
  const fadeIn = lerp(frame, [SPLIT.timersIn, SPLIT.timersIn + 8], [0, 1]);
  const blinkOn = side === "bottom" || frame < freezeAt || Math.floor((frame - freezeAt) / TIMER_BLINK_EVERY) % 2 === 0;
  return (
    <div
      style={{
        position: "absolute",
        right: W - LAYOUT.timerRightX,
        top: (side === "top" ? LAYOUT.topLabelY : LAYOUT.bottomLabelY) + 2,
        fontFamily: FONTS.inter,
        fontWeight: 700,
        fontSize: TYPE.timer,
        lineHeight: 1.15,
        fontVariantNumeric: "tabular-nums",
        color: side === "top" ? COLORS.red : COLORS.green,
        opacity: fadeIn * (blinkOn ? 1 : 0.15),
        whiteSpace: "nowrap",
      }}
    >
      {formatTimer(minutesAt(frame, side), side)}
    </div>
  );
};
