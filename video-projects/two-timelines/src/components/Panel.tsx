import React from "react";
import { COLORS, H, W } from "../theme";

/**
 * A clipped half of the split screen. Children are laid out in *frame*
 * coordinates (0..1080 x 0..1920) regardless of where the panel sits.
 */
export const Panel: React.FC<{
  top: number; // current clip top (frame coords)
  bottom: number; // current clip bottom
  bg: string;
  offsetY?: number; // slide-in offset
  children: React.ReactNode;
  background?: React.ReactNode;
}> = ({ top, bottom, bg, offsetY = 0, children, background }) => (
  <div
    style={{
      position: "absolute",
      left: 0,
      top,
      width: W,
      height: Math.max(0, bottom - top),
      overflow: "hidden",
      transform: `translateY(${offsetY}px)`,
      backgroundColor: bg,
    }}
  >
    {background}
    <div style={{ position: "absolute", left: 0, top: -top, width: W, height: H }}>{children}</div>
  </div>
);

export const Divider: React.FC<{ progress: number }> = ({ progress }) => (
  <div
    style={{
      position: "absolute",
      left: 0,
      top: 957,
      width: W,
      height: 6,
      background: COLORS.divider,
      transform: `scaleX(${progress})`,
      transformOrigin: "50% 50%",
    }}
  />
);
