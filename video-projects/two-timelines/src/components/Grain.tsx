import React from "react";
import { useCurrentFrame } from "remotion";
import { GRAIN_OPACITY } from "../theme";

/** Animated film grain (seed changes every frame). */
export const Grain: React.FC<{ width: number; height: number; opacity?: number }> = ({
  width,
  height,
  opacity = GRAIN_OPACITY,
}) => {
  const frame = useCurrentFrame();
  const id = "grain-filter";
  return (
    <svg
      width={width}
      height={height}
      style={{ position: "absolute", left: 0, top: 0, opacity, mixBlendMode: "overlay", pointerEvents: "none" }}
    >
      <filter id={id}>
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={frame % 97} stitchTiles="stitch" />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter={`url(#${id})`} />
    </svg>
  );
};
