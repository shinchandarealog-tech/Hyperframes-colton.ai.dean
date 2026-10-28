import React from "react";
import { AbsoluteFill } from "remotion";
import { COLORS } from "../theme";

export const Glow: React.FC<{ opacity?: number; bg?: string }> = ({ opacity = 1, bg }) => (
  <AbsoluteFill style={{ backgroundColor: bg }}>
    <AbsoluteFill
      style={{
        opacity,
        background: `radial-gradient(circle at 50% 50%, ${COLORS.glow} 0%, ${COLORS.glow}00 62%)`,
      }}
    />
  </AbsoluteFill>
);
