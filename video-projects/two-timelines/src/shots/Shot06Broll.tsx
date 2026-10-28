import React from "react";
import { useCurrentFrame } from "remotion";
import { ChatCard } from "../components/ChatCard";
import { HardGrade } from "../components/HardGrade";
import { Note } from "../components/Note";
import { ShotHalf } from "../components/ShotHalf";
import { StepTag } from "../components/StepTag";
import { jerky, lerp, smooth } from "../lib/anim";
import { COLORS, FONTS } from "../theme";
import { BROLL, SHOTS } from "../timing";
import { PROMPTS } from "../prompts";
import { ShotProps } from "./types";

const WIN = { x: 110, y: 400, w: 820, h: 430 };
const IDEAS = ["Drone over the city", "Hands on keyboard", "Slow push-in on face"];

export const Shot06Broll: React.FC<ShotProps> = ({ half, recordings }) => {
  const frame = useCurrentFrame() + SHOTS.broll.from;
  const { from, to } = SHOTS.broll;
  if (half === "top") {
    const tabs = Math.min(BROLL.tabsEnd, BROLL.tabsStart + Math.max(0, Math.floor((frame - from) / BROLL.tabEvery)));
    const tabsW = WIN.w - 120;
    const tabW = tabsW / tabs;
    const winIn = jerky(frame, from, 4, 2);
    return (
      <ShotHalf frame={frame} to={to} smart={false}>
        <StepTag frame={frame} start={from} side="top" text="Step 4 · B-roll" />
        <HardGrade>
          <div
            style={{
              position: "absolute",
              left: WIN.x,
              top: WIN.y,
              width: WIN.w,
              height: WIN.h,
              borderRadius: 16,
              background: "#ECECEC",
              overflow: "hidden",
              boxShadow: "0 18px 50px rgba(0,0,0,0.45)",
              opacity: winIn > 0 ? 1 : 0,
              fontFamily: FONTS.inter,
            }}
          >
            {/* tab strip */}
            <div style={{ position: "absolute", left: 0, top: 0, right: 0, height: 54, background: "#BDBDBD" }} />
            {Array.from({ length: tabs }).map((_, i) => (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: 14 + i * tabW,
                  top: 10,
                  width: Math.max(2, tabW - 3),
                  height: 44,
                  borderRadius: "8px 8px 0 0",
                  background: i === tabs - 1 ? "#ECECEC" : "#D6D6D6",
                  overflow: "hidden",
                  whiteSpace: "nowrap",
                  fontSize: 18,
                  fontWeight: 500,
                  color: "#444",
                  lineHeight: "44px",
                  paddingLeft: 8,
                  boxSizing: "border-box",
                }}
              >
                b-roll ideas - Search
              </div>
            ))}
            {/* tab counter */}
            <div
              style={{
                position: "absolute",
                right: 18,
                top: 9,
                width: 72,
                height: 38,
                borderRadius: 9,
                border: "3px solid #3A3A3A",
                fontWeight: 700,
                fontSize: 22,
                lineHeight: "32px",
                textAlign: "center",
                color: "#2A2A2A",
                background: "#ECECEC",
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {tabs}
            </div>
            {/* search bar */}
            <div
              style={{
                position: "absolute",
                left: 30,
                right: 30,
                top: 76,
                height: 62,
                borderRadius: 31,
                background: "#FFFFFF",
                border: "2px solid #C8C8C8",
                fontSize: 30,
                fontWeight: 500,
                color: "#2A2A2A",
                lineHeight: "58px",
                paddingLeft: 28,
              }}
            >
              b-roll ideas???
            </div>
            {/* results */}
            {Array.from({ length: 8 }).map((_, i) => (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: 30 + (i % 4) * 192,
                  top: 162 + Math.floor(i / 4) * 128,
                  width: 176,
                  height: 112,
                  borderRadius: 10,
                  background: i % 3 === 0 ? "#B5B5B5" : "#CFCFCF",
                }}
              />
            ))}
          </div>
        </HardGrade>
        <Note x={540} y={862} align="center" opacity={tabs >= BROLL.tabsEnd ? 1 : 0}>
          47 tabs open
        </Note>
      </ShotHalf>
    );
  }

  return (
    <ShotHalf frame={frame} to={to} smart>
      <StepTag frame={frame} start={from} side="bottom" text="Step 4 · B-roll" />
      <ChatCard
        frame={frame}
        shotFrom={from}
        shotTo={to}
        x={60}
        y={1160}
        w={920}
        h={152}
        inAt={BROLL.cardIn}
        prompt={PROMPTS[3]}
        typing={BROLL.typing}
        fontSize={22}
        replyLabelAt={9999}
        recording={recordings?.[3]}
      />
      <div
        style={{
          position: "absolute",
          left: 84,
          top: 1330,
          fontFamily: FONTS.inter,
          fontWeight: 600,
          fontSize: 20,
          color: COLORS.muted,
          letterSpacing: 0.4,
          opacity: lerp(frame, [BROLL.ideaStarts[0] - 2, BROLL.ideaStarts[0] + 2], [0, 1]),
        }}
      >
        Claude
      </div>
      {IDEAS.map((text, i) => {
        const t = smooth(frame, BROLL.ideaStarts[i], BROLL.ideaLen);
        return (
          <div
            key={text}
            style={{
              position: "absolute",
              left: 84 + i * 100 + (1 - t) * BROLL.ideaTravel,
              top: 1356 + i * 44,
              width: 520,
              height: 56,
              borderRadius: 16,
              background: COLORS.card,
              boxShadow: "0 12px 30px rgba(0,0,0,0.45)",
              opacity: t,
              display: "flex",
              alignItems: "center",
              gap: 14,
              paddingLeft: 12,
              boxSizing: "border-box",
              fontFamily: FONTS.inter,
            }}
          >
            <span
              style={{
                width: 34,
                height: 34,
                borderRadius: 10,
                background: COLORS.green,
                color: COLORS.onGreen,
                fontWeight: 800,
                fontSize: 20,
                lineHeight: "34px",
                textAlign: "center",
              }}
            >
              {i + 1}
            </span>
            <span style={{ fontWeight: 600, fontSize: 24, color: COLORS.cardText }}>{text}</span>
          </div>
        );
      })}
    </ShotHalf>
  );
};
