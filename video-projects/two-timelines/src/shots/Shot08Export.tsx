import React from "react";
import { useCurrentFrame } from "remotion";
import { Character } from "../components/Character";
import { Check } from "../components/Check";
import { HardGrade } from "../components/HardGrade";
import { ProgressBar } from "../components/ProgressBar";
import { lerp, prog, smooth } from "../lib/anim";
import { COLORS, FONTS } from "../theme";
import { EXPORT, SHOTS } from "../timing";
import { ShotProps } from "./types";

const SPARKS = 12;

export const Shot08Export: React.FC<ShotProps> = ({ half }) => {
  const frame = useCurrentFrame() + SHOTS.exportShot.from;
  const { from } = SHOTS.exportShot;
  if (half === "top") {
    const crawl = Math.floor(prog(frame, from, EXPORT.topCrawlTo) * EXPORT.topPercent) / 100;
    const spin = Math.floor(frame / 2) * 45; // stepped spinner
    return (
      <>
        <HardGrade>
          <svg width={100} height={100} viewBox="-50 -50 100 100" style={{ position: "absolute", left: 490, top: 370 }}>
            {Array.from({ length: 8 }).map((_, i) => (
              <circle key={i} cx={0} cy={-34} r={8} fill="#DADADA" opacity={0.25 + (i / 8) * 0.75} transform={`rotate(${spin + i * 45})`} />
            ))}
          </svg>
          <div style={{ position: "absolute", left: 140, top: 498, fontFamily: FONTS.inter, fontWeight: 600, fontSize: 30, color: COLORS.white }}>
            Exporting final_v9_REAL.mp4
          </div>
          <ProgressBar x={140} y={548} w={800} h={40} progress={crawl} fill="#A0A0A0" />
          <Character x={540} y={800} pose="slumped" scale={0.5} headDrop={1} />
        </HardGrade>
        <div
          style={{
            position: "absolute",
            left: 140,
            top: 610,
            fontFamily: FONTS.inter,
            fontWeight: 700,
            fontSize: 40,
            color: COLORS.red,
            opacity: frame >= EXPORT.errorText ? 1 : 0,
          }}
        >
          {`${Math.round(crawl * 100)}%… still rendering`}
        </div>
      </>
    );
  }
  const fill = prog(frame, EXPORT.bottomFill.from, EXPORT.bottomFill.to, (t) => t);
  const slamT = prog(frame, EXPORT.slam, EXPORT.slam + EXPORT.slamLen);
  const slamScale = lerp(slamT, [0, 1], [1.4, 1]);
  const spark = prog(frame, EXPORT.slam, EXPORT.slam + EXPORT.sparkLen);
  const barIn = smooth(frame, from - 2, 6);
  return (
    <>
      <div style={{ position: "absolute", left: 140, top: 1134, fontFamily: FONTS.inter, fontWeight: 600, fontSize: 30, color: COLORS.white, opacity: barIn }}>
        Exporting final.mp4
      </div>
      <ProgressBar x={140} y={1184} w={800} h={40} progress={fill} fill={COLORS.green} />
      {frame >= EXPORT.slam ? (
        <div style={{ position: "absolute", left: 0, top: 1262, width: 1080, height: 150, display: "flex", justifyContent: "center", alignItems: "center" }}>
          {/* spark lines */}
          <svg width={900} height={420} viewBox="-450 -210 900 420" style={{ position: "absolute", left: 90, top: -135, opacity: 1 - spark }}>
            {Array.from({ length: SPARKS }).map((_, i) => {
              const a = (i / SPARKS) * Math.PI * 2 + 0.2;
              const r0 = 200 + spark * 120;
              const r1 = r0 + 50 * (1 - spark * 0.6);
              const sy = 0.55; // flatten to the word's shape
              return (
                <line
                  key={i}
                  x1={Math.cos(a) * r0}
                  y1={Math.sin(a) * r0 * sy}
                  x2={Math.cos(a) * r1}
                  y2={Math.sin(a) * r1 * sy}
                  stroke={COLORS.green}
                  strokeWidth={6}
                  strokeLinecap="round"
                />
              );
            })}
          </svg>
          <div
            style={{
              fontFamily: FONTS.inter,
              fontWeight: 900,
              fontSize: 110,
              lineHeight: 1,
              color: COLORS.green,
              transform: `scale(${slamScale})`,
              opacity: lerp(frame, [EXPORT.slam, EXPORT.slam + 2], [0, 1]),
              display: "flex",
              alignItems: "center",
              gap: 24,
              letterSpacing: -2,
            }}
          >
            EXPORT
            <Check size={96} color={COLORS.green} stroke={4} />
          </div>
        </div>
      ) : null}
    </>
  );
};
