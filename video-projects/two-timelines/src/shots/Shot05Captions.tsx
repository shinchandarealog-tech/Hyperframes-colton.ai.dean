import React from "react";
import { useCurrentFrame } from "remotion";
import { ChatCard } from "../components/ChatCard";
import { Chip } from "../components/Chip";
import { HardGrade } from "../components/HardGrade";
import { Note } from "../components/Note";
import { ShotHalf } from "../components/ShotHalf";
import { StepTag } from "../components/StepTag";
import { jerky, lerp, overshoot, prog, smooth } from "../lib/anim";
import { COLORS, FONTS } from "../theme";
import { CAPTIONS, SHOTS } from "../timing";
import { PROMPTS } from "../prompts";
import { ShotProps } from "./types";

const FIRST = "Thsi is how i";
const FIXED = "This";
const REST_AFTER = " edit";

/** Hard-side caption text state at a frame. */
const captionState = (frame: number) => {
  const per = CAPTIONS.framesPerLetter;
  const n = Math.max(0, Math.floor((frame - CAPTIONS.typeStart) / per) + 1);
  if (frame < CAPTIONS.deleteFrom) return { word: FIRST.slice(0, Math.min(4, n)), tail: FIRST.slice(4, Math.min(FIRST.length, n)), wrong: true };
  const tail = FIRST.slice(4);
  if (frame < CAPTIONS.deleteTo) {
    const left = 4 - Math.floor(prog(frame, CAPTIONS.deleteFrom, CAPTIONS.deleteTo) * 4);
    return { word: FIRST.slice(0, left), tail, wrong: true };
  }
  const k = Math.floor((frame - CAPTIONS.deleteTo) / per) + 1;
  const word = FIXED.slice(0, Math.min(4, k));
  const extra = REST_AFTER.slice(0, Math.max(0, k - 6));
  return { word, tail: tail + extra, wrong: false };
};

const SRT = [
  ["00:00–00:01", "Same video."],
  ["00:01–00:02", "Same deadline."],
  ["00:02–00:03", "Two editors."],
];

const CARD = { x: 60, y: 1160, w: 580, h: 420 };
const PHONE = { x: 680, y: 1150, w: 260, h: 520 };

export const Shot05Captions: React.FC<ShotProps> = ({ half, recordings }) => {
  const frame = useCurrentFrame() + SHOTS.captions.from;
  const { from, to } = SHOTS.captions;
  if (half === "top") {
    const s = captionState(frame);
    const boxIn = jerky(frame, from, 6, 2);
    const caretOn = Math.floor(frame / 8) % 2 === 0;
    const squiggle = s.wrong && frame >= CAPTIONS.squiggle && s.word.length > 0;
    return (
      <ShotHalf frame={frame} to={to} smart={false}>
        <StepTag frame={frame} start={from} side="top" text="Step 3 · Captions" />
        <HardGrade>
          <div
            style={{
              position: "absolute",
              left: 130,
              top: 470,
              width: 820,
              height: 170,
              background: "#3A3A3A",
              border: "2px solid #505050",
              borderRadius: 14,
              opacity: boxIn > 0 ? 1 : 0,
            }}
          />
        </HardGrade>
        <div
          style={{
            position: "absolute",
            left: 180,
            top: 512,
            fontFamily: FONTS.inter,
            fontWeight: 700,
            fontSize: 64,
            lineHeight: "80px",
            color: COLORS.white,
            whiteSpace: "pre",
            opacity: boxIn > 0 ? 1 : 0,
          }}
        >
          <span style={{ position: "relative" }}>
            {s.word}
            {squiggle ? (
              <svg width={150} height={18} viewBox="0 0 150 18" style={{ position: "absolute", left: 0, top: 74 }}>
                <path d="M2 9 Q9.5 1 17 9 T32 9 T47 9 T62 9 T77 9 T92 9 T107 9 T122 9 T137 9 T148 9" stroke={COLORS.red} strokeWidth={4} fill="none" />
              </svg>
            ) : null}
          </span>
          {s.tail}
          <span style={{ opacity: caretOn ? 1 : 0, fontWeight: 500 }}>|</span>
        </div>
        <Note x={540} y={700} align="center" opacity={frame >= from + 20 ? 1 : 0}>
          typing every word…
        </Note>
      </ShotHalf>
    );
  }

  const phoneIn = smooth(frame, from + 4, 12);
  return (
    <ShotHalf frame={frame} to={to} smart>
      <StepTag frame={frame} start={from} side="bottom" text="Step 3 · Captions" />
      <ChatCard
        frame={frame}
        shotFrom={from}
        shotTo={to}
        {...CARD}
        inAt={CAPTIONS.cardIn}
        prompt={PROMPTS[2]}
        typing={CAPTIONS.typing}
        fontSize={22}
        replyFrom={CAPTIONS.srtIn}
        recording={recordings?.[2]}
      >
        {SRT.map(([ts, text], i) => {
          const t = smooth(frame, CAPTIONS.srtIn + i * 3, 6);
          const lifted = frame >= CAPTIONS.flyStart + i * CAPTIONS.flyStagger;
          return (
            <div key={i} style={{ display: "flex", gap: 14, alignItems: "baseline", opacity: t * (lifted ? 0.25 : 1), lineHeight: "32px" }}>
              <span style={{ fontSize: 17, fontWeight: 600, color: COLORS.cardMuted, fontVariantNumeric: "tabular-nums" }}>{ts}</span>
              <span style={{ fontSize: 22, fontWeight: 700, color: COLORS.cardText }}>{text}</span>
            </div>
          );
        })}
      </ChatCard>
      {/* phone */}
      <div
        style={{
          position: "absolute",
          left: PHONE.x,
          top: PHONE.y + (1 - phoneIn) * 40,
          width: PHONE.w,
          height: PHONE.h,
          borderRadius: 40,
          background: "#050605",
          border: "8px solid #2A2E2A",
          boxSizing: "border-box",
          opacity: phoneIn,
          boxShadow: "0 20px 60px rgba(0,0,0,0.45)",
          overflow: "hidden",
        }}
      >
        <div style={{ position: "absolute", left: "50%", top: 12, width: 70, height: 18, marginLeft: -35, borderRadius: 9, background: "#2A2E2A" }} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 0, bottom: 0, background: "radial-gradient(circle at 50% 35%, #1D241E 0%, #050605 70%)" }} />
      </div>
      {SRT.map(([, text], i) => {
        const start = CAPTIONS.flyStart + i * CAPTIONS.flyStagger;
        if (frame < start) return null;
        const t = prog(frame, start, start + CAPTIONS.flyLen, overshoot);
        const lin = prog(frame, start, start + CAPTIONS.flyLen);
        // from: its line in the card; to: stacked inside the phone
        const fromX = CARD.x + 34 + 150;
        const fromY = CARD.y + 34 + 150 + 30 + i * 32;
        const toX = PHONE.x + 24;
        const toY = PHONE.y + 140 + i * 56;
        const x = lerp(t, [0, 1], [fromX, toX]);
        const y = lerp(t, [0, 1], [fromY, toY]) - Math.sin(lin * Math.PI) * 40;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: PHONE.w - 48,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <span
              style={{
                fontFamily: FONTS.inter,
                fontWeight: 700,
                fontSize: 24,
                lineHeight: "30px",
                padding: "4px 12px",
                borderRadius: 8,
                color: COLORS.onGreen,
                background: COLORS.green,
                transform: `scale(${lerp(lin, [0, 1], [0.85, 1])})`,
                whiteSpace: "nowrap",
                boxShadow: "0 8px 20px rgba(0,0,0,0.35)",
              }}
            >
              {text}
            </span>
          </div>
        );
      })}
      <Chip frame={frame} start={CAPTIONS.chip} x={470} y={1128} label=".srt" />
    </ShotHalf>
  );
};
