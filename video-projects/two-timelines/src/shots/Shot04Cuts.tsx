import React from "react";
import { random, useCurrentFrame } from "remotion";
import { ChatCard } from "../components/ChatCard";
import { Chip } from "../components/Chip";
import { HardGrade } from "../components/HardGrade";
import { Note } from "../components/Note";
import { ShotHalf } from "../components/ShotHalf";
import { StepTag } from "../components/StepTag";
import { lerp, prog, smooth } from "../lib/anim";
import { COLORS, FONTS } from "../theme";
import { CUTS, SHOTS } from "../timing";
import { PROMPTS } from "../prompts";
import { ShotProps } from "./types";

const TL = { y: 420, w: 2400, trackH: 78, gap: 16, rulerH: 34 };
const TRACK_TONES = ["#8E8E8E", "#6F6F6F", "#A4A4A4"];

// Seeded clip layout for the fake 2-hour timeline.
const TRACKS = [0, 1, 2].map((t) => {
  const clips: { x: number; w: number }[] = [];
  let x = 20 + random(`t${t}-start`) * 40;
  let i = 0;
  while (x < TL.w) {
    const w = 60 + random(`t${t}-w${i}`) * 180;
    clips.push({ x, w });
    x += w + 6 + random(`t${t}-g${i}`) * 20;
    i++;
  }
  return clips;
});

const TRANSCRIPT = [
  ["00:02", "So today I'm showing you how I edit"],
  ["00:05", "um, so, uh, like, basically…"],
  ["00:09", "a whole reel in under an hour."],
  ["00:12", "wait, let me start that again —"],
  ["00:15", "First, the script. Then the cuts."],
  ["00:19", "Then captions and B-roll. Done."],
];

export const Shot04Cuts: React.FC<ShotProps> = ({ half, recordings }) => {
  const frame = useCurrentFrame() + SHOTS.cuts.from;
  const { from, to } = SHOTS.cuts;
  if (half === "top") {
    const pan = lerp(frame, [from, to], [0, -CUTS.pan]);
    // triangle-wave scrub, linear, back and forth
    const ph = ((frame - from) % CUTS.scrubPeriod) / CUTS.scrubPeriod;
    const tri = ph < 0.5 ? ph * 2 : 2 - ph * 2;
    const playX = 150 + tri * 760 + (random(`scrub-${frame}`) - 0.5) * 10;
    const tracksTop = TL.y + TL.rulerH + 8;
    const tlBottom = tracksTop + 3 * TL.trackH + 2 * TL.gap;
    return (
      <ShotHalf frame={frame} to={to} smart={false}>
        <StepTag frame={frame} start={from} side="top" text="Step 2 · Cuts" />
        <HardGrade>
          <div style={{ position: "absolute", left: 0, top: TL.y - 12, width: 1080, height: tlBottom - TL.y + 24, background: "#222222" }} />
          <div style={{ position: "absolute", left: pan, top: TL.y, width: TL.w, height: tlBottom - TL.y }}>
            {/* ruler */}
            {Array.from({ length: 80 }).map((_, i) => (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: i * 30,
                  top: i % 5 === 0 ? 0 : 16,
                  width: 2,
                  height: i % 5 === 0 ? TL.rulerH : TL.rulerH - 16,
                  background: "#6A6A6A",
                }}
              />
            ))}
            {TRACKS.map((clips, t) =>
              clips.map((c, i) => (
                <div
                  key={`${t}-${i}`}
                  style={{
                    position: "absolute",
                    left: c.x,
                    top: TL.rulerH + 8 + t * (TL.trackH + TL.gap),
                    width: c.w,
                    height: TL.trackH,
                    background: TRACK_TONES[t],
                    borderRadius: 6,
                    border: "2px solid #4A4A4A",
                  }}
                />
              )),
            )}
          </div>
        </HardGrade>
        {/* red playhead (kept out of the grade) */}
        <div style={{ position: "absolute", left: playX - 2, top: TL.y - 10, width: 4, height: tlBottom - TL.y + 20, background: COLORS.red }} />
        <div
          style={{
            position: "absolute",
            left: playX - 14,
            top: TL.y - 26,
            width: 0,
            height: 0,
            borderLeft: "14px solid transparent",
            borderRight: "14px solid transparent",
            borderTop: `18px solid ${COLORS.red}`,
          }}
        />
        <Note x={540} y={tlBottom + 48} align="center" opacity={frame >= from + 12 ? 1 : 0}>
          2 hrs of raw footage
        </Note>
      </ShotHalf>
    );
  }

  const tIn = smooth(frame, CUTS.transcriptIn, 10);
  return (
    <ShotHalf frame={frame} to={to} smart>
      <StepTag frame={frame} start={from} side="bottom" text="Step 2 · Cuts" />
      <ChatCard
        frame={frame}
        shotFrom={from}
        shotTo={to}
        x={60}
        y={1160}
        w={920}
        h={152}
        inAt={CUTS.cardIn}
        prompt={PROMPTS[1]}
        typing={CUTS.typing}
        fontSize={22}
        replyLabelAt={9999}
        recording={recordings?.[1]}
      />
      <div
        style={{
          position: "absolute",
          left: 60,
          top: 1326,
          width: 920,
          height: 190,
          borderRadius: 24,
          background: "#1C201C",
          border: "2px solid #2C322C",
          opacity: tIn,
          transform: `translateY(${(1 - tIn) * 24}px)`,
          padding: "16px 30px",
          boxSizing: "border-box",
          fontFamily: FONTS.inter,
        }}
      >
        {TRANSCRIPT.map(([ts, text], i) => {
          const k = CUTS.struckLines.indexOf(i);
          const strike = k >= 0 ? prog(frame, CUTS.strikeStart + k * CUTS.strikeStagger, CUTS.strikeStart + k * CUTS.strikeStagger + CUTS.strikeLen) : 0;
          const lineIn = smooth(frame, CUTS.transcriptIn + i * 2, 8);
          return (
            <div key={i} style={{ display: "flex", gap: 18, fontSize: 20, lineHeight: "26px", opacity: lineIn * (k >= 0 ? lerp(strike, [0, 1], [1, 0.55]) : 1) }}>
              <span style={{ color: COLORS.muted, fontWeight: 600, fontVariantNumeric: "tabular-nums" }}>{ts}</span>
              <span style={{ position: "relative", color: COLORS.white, fontWeight: 500 }}>
                {text}
                {k >= 0 ? (
                  <span
                    style={{
                      position: "absolute",
                      left: -4,
                      top: 12,
                      height: 3,
                      width: `calc(${strike * 100}% + ${strike * 8}px)`,
                      background: COLORS.red,
                      borderRadius: 2,
                    }}
                  />
                ) : null}
              </span>
            </div>
          );
        })}
      </div>
      <Chip frame={frame} start={CUTS.chip} x={712} y={1300} label="Cut list" />
    </ShotHalf>
  );
};
