import React from "react";
import { useCurrentFrame } from "remotion";
import { Character } from "../components/Character";
import { HardGrade } from "../components/HardGrade";
import { Note } from "../components/Note";
import { ShotHalf } from "../components/ShotHalf";
import { lerp, prog, smooth } from "../lib/anim";
import { COLORS } from "../theme";
import { GRIND, SHOTS } from "../timing";
import { ShotProps } from "./types";

const CLOCK = { x: 240, y: 520, r: 112 };
const CUP = { x: 800, w: 96, h: 70, floor: 650 };
const TRACK = { x: 100, y: 1404, w: 820, h: 84 };
const CLIP_W = (TRACK.w - 20 - 3 * 10) / 4;

const Cup: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <svg width={CUP.w + 28} height={CUP.h} viewBox="0 0 124 70" style={{ position: "absolute", left: x, top: y }}>
    <path d="M6 4 L90 4 L82 66 L14 66 Z" fill="#E4E4E4" stroke="#8C8C8C" strokeWidth={3} />
    <rect x={10} y={22} width={76} height={14} fill="#9C9C9C" />
    <path d="M88 18 Q112 20 108 38 Q104 52 84 50" stroke="#8C8C8C" strokeWidth={6} fill="none" />
  </svg>
);

export const Shot07Grind: React.FC<ShotProps> = ({ half }) => {
  const frame = useCurrentFrame() + SHOTS.grind.from;
  const { from, to } = SHOTS.grind;
  if (half === "top") {
    const minuteA = (frame - from) * 26;
    const hourA = (frame - from) * 2.2 + 40;
    const headDrop = prog(frame, from, to);
    return (
      <ShotHalf frame={frame} to={to} smart={false}>
        <HardGrade>
          {/* wall clock */}
          <svg width={CLOCK.r * 2 + 20} height={CLOCK.r * 2 + 20} style={{ position: "absolute", left: CLOCK.x - CLOCK.r - 10, top: CLOCK.y - CLOCK.r - 10 }}>
            <g transform={`translate(${CLOCK.r + 10} ${CLOCK.r + 10})`}>
              <circle r={CLOCK.r} fill="#EDEDED" stroke="#5A5A5A" strokeWidth={10} />
              {Array.from({ length: 12 }).map((_, i) => (
                <rect key={i} x={-3} y={-CLOCK.r + 12} width={6} height={i % 3 === 0 ? 20 : 12} fill="#4A4A4A" transform={`rotate(${i * 30})`} />
              ))}
              <rect x={-5} y={-58} width={10} height={64} rx={5} fill="#2E2E2E" transform={`rotate(${hourA})`} />
              <rect x={-3.5} y={-88} width={7} height={96} rx={3.5} fill="#2E2E2E" transform={`rotate(${minuteA})`} />
              <circle r={9} fill="#2E2E2E" />
            </g>
          </svg>
          {/* stacked coffee cups */}
          {GRIND.cups.map((start, i) => {
            if (frame < start) return null;
            const landY = CUP.floor - (i + 1) * (CUP.h - 4);
            const fall = Math.floor(prog(frame, start, start + 6) * 3) / 3; // jerky
            return <Cup key={i} x={CUP.x + (i % 2 ? 6 : -4)} y={landY - (1 - fall) * 120} />;
          })}
          <Character x={560} y={760} pose="slumped" scale={0.64} headDrop={headDrop} />
        </HardGrade>
        <Note x={600} y={392} opacity={frame >= GRIND.cups[3] ? 1 : 0} rotate={-6}>
          coffee #4
        </Note>
      </ShotHalf>
    );
  }

  const enter = smooth(frame, from, 10);
  const playX = lerp(frame, [from + 6, to], [TRACK.x + 10, TRACK.x + TRACK.w - 10]);
  return (
    <ShotHalf frame={frame} to={to} smart>
      <div style={{ opacity: enter, transform: `translateY(${(1 - enter) * 20}px)` }}>
        <Character x={300} y={1250} pose="relaxed" scale={0.6} typing={frame / 2} blink={frame % 50 < 3} />
        <Note x={560} y={1190} rotate={-4}>
          actually editing
        </Note>
        {/* timeline track */}
        <div
          style={{
            position: "absolute",
            left: TRACK.x,
            top: TRACK.y,
            width: TRACK.w,
            height: TRACK.h,
            borderRadius: 16,
            background: "#1A1E1A",
            border: "2px solid #2C322C",
          }}
        />
        {GRIND.clipSnaps.map((start, i) => {
          const x = TRACK.x + 10 + i * (CLIP_W + 10);
          const y = TRACK.y + 10;
          const h = TRACK.h - 20;
          const land = start + GRIND.clipLen;
          const t = prog(frame, start, land);
          const squash = frame >= land && frame < land + GRIND.squash ? 1 : 0;
          const placed = frame >= land;
          return (
            <React.Fragment key={i}>
              <div
                style={{
                  position: "absolute",
                  left: x,
                  top: y,
                  width: CLIP_W,
                  height: h,
                  borderRadius: 10,
                  border: "2px dashed #3E463E",
                  boxSizing: "border-box",
                }}
              />
              {frame >= start ? (
                <div
                  style={{
                    position: "absolute",
                    left: x,
                    top: y - (1 - t) * 70,
                    width: CLIP_W,
                    height: h,
                    borderRadius: 10,
                    background: placed ? COLORS.green : "#4B544B",
                    transform: `scale(${squash ? 1.06 : 1}, ${squash ? 0.86 : 1})`,
                    transformOrigin: "50% 100%",
                    opacity: lerp(t, [0, 0.4], [0, 1]),
                  }}
                />
              ) : null}
            </React.Fragment>
          );
        })}
        <div style={{ position: "absolute", left: playX - 2, top: TRACK.y - 12, width: 4, height: TRACK.h + 24, background: COLORS.white, borderRadius: 2 }} />
      </div>
    </ShotHalf>
  );
};
