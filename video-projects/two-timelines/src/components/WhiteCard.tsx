import React from "react";
import { CARD_RADIUS, CARD_SHADOW, COLORS } from "../theme";

export const WhiteCard: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  scale?: number;
  opacity?: number;
  radius?: number;
  origin?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}> = ({ x, y, w, h, scale = 1, opacity = 1, radius = CARD_RADIUS, origin = "50% 50%", style, children }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      height: h,
      borderRadius: radius,
      background: COLORS.card,
      boxShadow: CARD_SHADOW,
      transform: `scale(${scale})`,
      transformOrigin: origin,
      opacity,
      overflow: "hidden",
      ...style,
    }}
  >
    {children}
  </div>
);
