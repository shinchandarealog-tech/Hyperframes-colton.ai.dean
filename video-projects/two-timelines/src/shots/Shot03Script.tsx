import React from "react";
import { useCurrentFrame } from "remotion";
import { ChatCard } from "../components/ChatCard";
import { Check } from "../components/Check";
import { HardGrade } from "../components/HardGrade";
import { PaperBall } from "../components/PaperBall";
import { ShotHalf } from "../components/ShotHalf";
import { StepTag } from "../components/StepTag";
import { fallBounce, jerky, pop } from "../lib/anim";
import { COLORS } from "../theme";
import { SCRIPT, SHOTS } from "../timing";
import { PROMPTS } from "../prompts";
import { ShotProps } from "./types";

const DOC = { x: 300, y: 394, w: 480, h: 556 };
const BALLS = [
  { x: 200, y: 890, rot: 20, from: -120 },
  { x: 880, y: 892, rot: -35, from: -80 },
  { x: 214, y: 818, rot: 60, from: -140 },
];

export const Shot03Script: React.FC<ShotProps> = ({ half, recordings }) => {
  const frame = useCurrentFrame() + SHOTS.script.from;
  const { from, to } = SHOTS.script;
  if (half === "top") {
    const docIn = jerky(frame, from, 6, 2);
    const cursorOn = Math.floor((frame - from) / SCRIPT.cursorBlink) % 2 === 0;
    return (
      <ShotHalf frame={frame} to={to} smart={false}>
        <StepTag frame={frame} start={from} side="top" text="Step 1 · Script" />
        <HardGrade>
          <div
            style={{
              position: "absolute",
              left: DOC.x,
              top: DOC.y + (1 - docIn) * 20,
              width: DOC.w,
              height: DOC.h,
              background: "#F4F4F2",
              borderRadius: 10,
              boxShadow: "0 18px 50px rgba(0,0,0,0.45)",
              opacity: docIn > 0 ? 1 : 0,
            }}
          >
            <div style={{ position: "absolute", left: 0, top: 0, right: 0, height: 44, background: "#DADAD6", borderRadius: "10px 10px 0 0" }} />
            <div
              style={{
                position: "absolute",
                left: 48,
                top: 84,
                width: 4,
                height: 44,
                background: "#2A2A2A",
                opacity: cursorOn ? 1 : 0,
              }}
            />
          </div>
          {SCRIPT.paperBalls.map((start, i) => {
            if (frame < start) return null;
            const b = BALLS[i];
            const f = fallBounce(frame, start, SCRIPT.paperFall);
            const y = b.from + (b.y - b.from) * f.y;
            return <PaperBall key={i} x={b.x} y={y} rot={b.rot + f.y * 90} squash={f.squash} />;
          })}
        </HardGrade>
      </ShotHalf>
    );
  }
  const badge = pop(frame, SCRIPT.check);
  return (
    <ShotHalf frame={frame} to={to} smart>
      <StepTag frame={frame} start={from} side="bottom" text="Step 1 · Script" />
      <ChatCard
        frame={frame}
        shotFrom={from}
        shotTo={to}
        x={60}
        y={1160}
        w={920}
        h={420}
        inAt={SCRIPT.cardIn}
        prompt={PROMPTS[0]}
        typing={SCRIPT.typing}
        reply={[
          "Hook (0–2s): “Same video. Two editors.”",
          "2–25s: Script, cuts, captions, B-roll.",
          "25–28s: Export lands. One side wins.",
          "28–30s: “Work smarter, not longer.”",
        ]}
        replyFrom={SCRIPT.reply.from}
        replyTo={SCRIPT.reply.to - 6}
        recording={recordings?.[0]}
      />
      <div
        style={{
          position: "absolute",
          left: 980 - 34,
          top: 1160 - 34,
          width: 68,
          height: 68,
          borderRadius: 34,
          background: COLORS.green,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          transform: `scale(${badge.scale})`,
          opacity: badge.opacity,
          boxShadow: "0 10px 26px rgba(0,0,0,0.4)",
        }}
      >
        <Check size={40} color={COLORS.onGreen} stroke={3.6} />
      </div>
    </ShotHalf>
  );
};
