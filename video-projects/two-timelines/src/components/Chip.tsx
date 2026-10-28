import React from "react";
import { COLORS, FONTS } from "../theme";
import { pop } from "../lib/anim";
import { Check } from "./Check";

/** Green chip, e.g. "Cut list ✓". Pops in at `start`. */
export const Chip: React.FC<{ frame: number; start: number; x: number; y: number; label: string; size?: number }> = ({
  frame,
  start,
  x,
  y,
  label,
  size = 30,
}) => {
  const p = pop(frame, start);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `scale(${p.scale})`,
        opacity: p.opacity,
        background: COLORS.green,
        color: COLORS.onGreen,
        fontFamily: FONTS.inter,
        fontWeight: 700,
        fontSize: size,
        padding: "10px 22px",
        borderRadius: 999,
        display: "flex",
        alignItems: "center",
        gap: 10,
        boxShadow: "0 12px 30px rgba(0,0,0,0.35)",
        whiteSpace: "nowrap",
      }}
    >
      {label}
      <Check size={size} color={COLORS.onGreen} />
    </div>
  );
};
