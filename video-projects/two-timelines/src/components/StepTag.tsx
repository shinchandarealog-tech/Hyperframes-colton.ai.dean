import React from "react";
import { COLORS, FONTS, LAYOUT, TYPE } from "../theme";
import { jerky, pop } from "../lib/anim";

/** "Step 1 · Script" pill under the half label. */
export const StepTag: React.FC<{ frame: number; start: number; side: "top" | "bottom"; text: string }> = ({
  frame,
  start,
  side,
  text,
}) => {
  const smart = side === "bottom";
  const p = pop(frame, start);
  const j = jerky(frame, start, 6, 2);
  return (
    <div
      style={{
        position: "absolute",
        left: LAYOUT.labelX,
        top: side === "top" ? LAYOUT.topStepY : LAYOUT.bottomStepY,
        transform: smart ? `scale(${p.scale})` : `translateY(${(1 - j) * 10}px)`,
        transformOrigin: "0% 50%",
        opacity: smart ? p.opacity : j > 0 ? 1 : 0,
        fontFamily: FONTS.inter,
        fontWeight: 600,
        fontSize: TYPE.step,
        lineHeight: 1.2,
        color: COLORS.white,
        padding: "6px 18px",
        borderRadius: 999,
        background: smart ? "rgba(47,208,107,0.14)" : "rgba(255,255,255,0.10)",
        border: `1.5px solid ${smart ? "rgba(47,208,107,0.55)" : "rgba(255,255,255,0.22)"}`,
        whiteSpace: "nowrap",
      }}
    >
      {text}
    </div>
  );
};
