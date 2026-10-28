import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COLORS, COPY, FONTS } from "../theme";
import { CTA, SHOTS } from "../timing";
import { pop } from "../lib/anim";

export const Shot10Cta: React.FC = () => {
  const frame = useCurrentFrame() + SHOTS.cta.from;
  const pulse =
    frame >= CTA.pulseFrom ? 1 + 0.04 * Math.sin((((frame - CTA.pulseFrom) % CTA.pulsePeriod) / CTA.pulsePeriod) * Math.PI) : 1;
  const lines: { y: number; node: React.ReactNode }[] = [
    {
      y: 720,
      node: <span style={{ fontWeight: 600, fontSize: 64, color: COLORS.white }}>{COPY.cta.comment}</span>,
    },
    {
      y: 860,
      node: (
        <span
          style={{
            display: "inline-block",
            fontWeight: 900,
            fontSize: 130,
            lineHeight: 1,
            color: COLORS.onGreen,
            background: COLORS.green,
            padding: "14px 40px 18px",
            borderRadius: 18,
            transform: `scale(${pulse})`,
            letterSpacing: -2,
          }}
        >
          {COPY.cta.keyword}
        </span>
      ),
    },
    { y: 990, node: <span style={{ fontWeight: 500, fontSize: 52, color: COLORS.white }}>{COPY.cta.line}</span> },
    { y: 1120, node: <span style={{ fontWeight: 500, fontSize: 40, color: COLORS.muted }}>{COPY.cta.handle}</span> },
  ];
  return (
    <AbsoluteFill style={{ fontFamily: FONTS.inter }}>
      {lines.map((l, i) => {
        const p = pop(frame, CTA.lineStarts[i]);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: 0,
              width: "100%",
              top: l.y,
              display: "flex",
              justifyContent: "center",
              transform: `translateY(-50%) scale(${p.scale})`,
              opacity: p.opacity,
              whiteSpace: "nowrap",
            }}
          >
            {l.node}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
