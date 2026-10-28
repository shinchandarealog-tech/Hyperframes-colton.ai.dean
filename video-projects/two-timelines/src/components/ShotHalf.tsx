import React from "react";
import { AbsoluteFill } from "remotion";
import { lerp, prog } from "../lib/anim";
import { SMART_EASE } from "../timing";

/** Wraps one half of a shot and handles its exit (smart = eased, hard = abrupt). */
export const ShotHalf: React.FC<{
  frame: number;
  to: number;
  smart: boolean;
  exitLen?: number;
  children: React.ReactNode;
}> = ({ frame, to, smart, exitLen = 5, children }) => {
  const e = smart ? prog(frame, to - exitLen, to, SMART_EASE) : frame >= to - 2 ? 1 : 0;
  return (
    <AbsoluteFill
      style={{
        opacity: 1 - e,
        transform: smart ? `scale(${lerp(e, [0, 1], [1, 0.97])})` : undefined,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
