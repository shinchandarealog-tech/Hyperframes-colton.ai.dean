import React from "react";

/** Crumpled paper ball. */
export const PaperBall: React.FC<{ x: number; y: number; size?: number; rot?: number; squash?: number }> = ({
  x,
  y,
  size = 84,
  rot = 0,
  squash = 0,
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 100 100"
    style={{
      position: "absolute",
      left: x - size / 2,
      top: y - size / 2,
      transform: `rotate(${rot}deg) scale(${1 + squash * 0.12}, ${1 - squash * 0.14})`,
      transformOrigin: "50% 50%",
    }}
  >
    <path d="M50 6 L72 12 L90 30 L94 54 L86 78 L64 94 L38 94 L14 80 L6 56 L10 30 L28 12 Z" fill="#EDEDED" />
    <path d="M28 12 L44 36 L72 12 M44 36 L36 62 L14 80 M44 36 L70 52 L94 54 M70 52 L64 94 M36 62 L64 72 L86 78 M10 30 L44 36"
      stroke="#A9A9A9" strokeWidth={3} fill="none" strokeLinejoin="round" />
  </svg>
);
