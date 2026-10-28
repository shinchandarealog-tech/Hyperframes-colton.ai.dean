import React from "react";

/** Check mark drawn as SVG (no font glyph dependency). */
export const Check: React.FC<{ size: number; color: string; stroke?: number; progress?: number }> = ({
  size,
  color,
  stroke = 3.2,
  progress = 1,
}) => {
  const len = 30;
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" style={{ display: "inline-block", verticalAlign: "-0.12em" }}>
      <path
        d="M4 12.5 L9.5 18 L20 6.5"
        fill="none"
        stroke={color}
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={len}
        strokeDashoffset={len * (1 - progress)}
      />
    </svg>
  );
};
