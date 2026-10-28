import React from "react";
import { COLORS, FONTS, TYPE } from "../theme";

/** Small handwritten side note (Caveat 700). */
export const Note: React.FC<{
  x: number;
  y: number;
  children: React.ReactNode;
  opacity?: number;
  rotate?: number;
  size?: number;
  align?: "left" | "center";
}> = ({ x, y, children, opacity = 1, rotate = -3, size = TYPE.note, align = "left" }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      transform: `translateX(${align === "center" ? "-50%" : "0"}) rotate(${rotate}deg)`,
      fontFamily: FONTS.caveat,
      fontWeight: 700,
      fontSize: size,
      lineHeight: 1,
      color: COLORS.white,
      opacity,
      whiteSpace: "nowrap",
    }}
  >
    {children}
  </div>
);
