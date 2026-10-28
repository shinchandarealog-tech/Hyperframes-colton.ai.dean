import React from "react";
import { COLORS } from "../theme";

export const ProgressBar: React.FC<{
  x: number;
  y: number;
  w: number;
  h?: number;
  progress: number;
  fill: string;
  track?: string;
}> = ({ x, y, w, h = 28, progress, fill, track = "rgba(255,255,255,0.12)" }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      height: h,
      borderRadius: h / 2,
      background: track,
      overflow: "hidden",
      border: `2px solid ${COLORS.divider}`,
    }}
  >
    <div style={{ width: `${Math.max(0, Math.min(1, progress)) * 100}%`, height: "100%", background: fill, borderRadius: h / 2 }} />
  </div>
);
