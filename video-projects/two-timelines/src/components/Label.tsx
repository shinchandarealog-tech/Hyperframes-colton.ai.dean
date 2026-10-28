import React from "react";
import { COLORS, FONTS, LAYOUT, TYPE } from "../theme";
import { SPLIT } from "../timing";

/** Half label that types on, 2 frames per character. */
export const Label: React.FC<{ frame: number; side: "top" | "bottom"; text: string }> = ({ frame, side, text }) => {
  const n = Math.max(0, Math.min(text.length, Math.floor((frame - SPLIT.labelsType) / SPLIT.framesPerChar) + 1));
  if (frame < SPLIT.labelsType) return null;
  const shown = text.slice(0, n);
  const onGreen = side === "bottom";
  return (
    <div
      style={{
        position: "absolute",
        left: LAYOUT.labelX,
        top: side === "top" ? LAYOUT.topLabelY : LAYOUT.bottomLabelY,
        fontFamily: FONTS.inter,
        fontWeight: 700,
        fontSize: TYPE.label,
        lineHeight: 1.15,
        letterSpacing: 0.5,
        color: onGreen ? COLORS.onGreen : COLORS.white,
        background: onGreen ? COLORS.green : "transparent",
        padding: onGreen ? "8px 18px" : 0,
        borderRadius: 8,
        whiteSpace: "pre",
      }}
    >
      {shown}
    </div>
  );
};
