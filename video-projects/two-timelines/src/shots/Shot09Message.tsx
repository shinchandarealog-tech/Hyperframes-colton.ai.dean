import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COLORS, FONTS, TYPE } from "../theme";
import { MESSAGE, SHOTS, SMART_EASE } from "../timing";
import { prog, smooth } from "../lib/anim";

const Word: React.FC<{ frame: number; i: number; children: React.ReactNode }> = ({ frame, i, children }) => {
  const t = smooth(frame, MESSAGE.wordsStart + i * MESSAGE.wordStagger, MESSAGE.wordIn);
  return (
    <span style={{ display: "inline-block", opacity: t, transform: `translateY(${(1 - t) * MESSAGE.wordRise}px)` }}>
      {children}
    </span>
  );
};

export const Shot09Message: React.FC = () => {
  const frame = useCurrentFrame() + SHOTS.message.from;
  const box = prog(frame, MESSAGE.highlight.from, MESSAGE.highlight.from + MESSAGE.highlight.len, SMART_EASE);
  const out = prog(frame, SHOTS.message.to - 6, SHOTS.message.to, SMART_EASE);
  const line: React.CSSProperties = {
    position: "absolute",
    left: 0,
    width: "100%",
    display: "flex",
    justifyContent: "center",
    transform: "translateY(-50%)",
    fontFamily: FONTS.inter,
    fontWeight: 700,
    fontSize: TYPE.message,
    lineHeight: 1.15,
    letterSpacing: -2,
    color: COLORS.white,
    whiteSpace: "pre",
  };
  return (
    <AbsoluteFill style={{ opacity: 1 - out, transform: `translateY(${-out * 20}px)` }}>
      <div style={{ ...line, top: 860 }}>
        <Word frame={frame} i={0}>Work </Word>
        <Word frame={frame} i={1}>
          <span style={{ position: "relative", display: "inline-block" }}>
            {/* green box grows left -> right behind the word */}
            <span
              style={{
                position: "absolute",
                left: -12,
                top: 4,
                bottom: 0,
                width: `calc(${box * 100}% + ${box * 20}px)`,
                background: COLORS.green,
                borderRadius: 10,
              }}
            />
            <span style={{ position: "relative" }}>smarter</span>
            {/* dark copy revealed exactly where the box covers it */}
            <span
              style={{
                position: "absolute",
                left: 0,
                top: 0,
                color: COLORS.onGreen,
                clipPath: `inset(-20px calc(${(1 - box) * 100}% - ${box * 20 - 12}px) -20px -20px)`,
              }}
            >
              smarter
            </span>
          </span>
          <span style={{ marginLeft: 8 }}>,</span>
        </Word>
      </div>
      <div style={{ ...line, top: 980 }}>
        <Word frame={frame} i={2}>not </Word>
        <Word frame={frame} i={3}>longer.</Word>
      </div>
    </AbsoluteFill>
  );
};
