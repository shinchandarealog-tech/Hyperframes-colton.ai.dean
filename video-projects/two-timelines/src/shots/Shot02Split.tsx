import React from "react";
import { useCurrentFrame } from "remotion";
import { Character } from "../components/Character";
import { HardGrade } from "../components/HardGrade";
import { ShotHalf } from "../components/ShotHalf";
import { jerky, lerp, pop } from "../lib/anim";
import { SHOTS } from "../timing";
import { ShotProps } from "./types";

const APPEAR = 76;

export const Shot02Split: React.FC<ShotProps> = ({ half }) => {
  const frame = useCurrentFrame() + SHOTS.split.from;
  if (half === "top") {
    const j = jerky(frame, APPEAR, 8, 3);
    const sigh = Math.floor(frame / 6) % 2; // jerky breathing
    return (
      <ShotHalf frame={frame} to={SHOTS.split.to} smart={false}>
        <HardGrade>
          <Character x={540} y={640 + (1 - j) * 30 + sigh} pose="slumped" opacity={j > 0 ? 1 : 0} />
        </HardGrade>
      </ShotHalf>
    );
  }
  const p = pop(frame, APPEAR);
  const bob = lerp(Math.sin((frame - APPEAR) / 9), [-1, 1], [-3, 3]);
  return (
    <ShotHalf frame={frame} to={SHOTS.split.to} smart>
      <Character
        x={540}
        y={1310 + bob}
        pose="relaxed"
        scale={p.scale * 0.92}
        opacity={p.opacity}
        typing={frame / 2}
        blink={frame % 48 < 3}
      />
    </ShotHalf>
  );
};
