import React from "react";
import { AbsoluteFill, Easing, useCurrentFrame } from "remotion";
import { COLORS, COPY, FONTS, TYPE } from "../theme";
import { HOOK, SHOTS, SPLIT } from "../timing";
import { lerp, prog } from "../lib/anim";

const YS = [820, 920, 1060];

export const Shot01Hook: React.FC = () => {
  const frame = useCurrentFrame() + SHOTS.hook.from;
  const out = 1 - prog(frame, SPLIT.hookOut.from, SPLIT.hookOut.to);
  const line = prog(frame, HOOK.underline.from, HOOK.underline.to, Easing.out(Easing.cubic));
  return (
    <AbsoluteFill style={{ opacity: out }}>
      {COPY.hook.map((text, i) => {
        const s = HOOK.lineStarts[i];
        const t = prog(frame, s, s + HOOK.lineIn, Easing.out(Easing.cubic));
        return (
          <div
            key={text}
            style={{
              position: "absolute",
              left: 0,
              width: "100%",
              top: YS[i],
              display: "flex",
              justifyContent: "center",
              transform: "translateY(-50%)",
            }}
          >
            <div
              style={{
                position: "relative",
                fontFamily: FONTS.inter,
                fontWeight: 700,
                fontSize: TYPE.hook,
                lineHeight: 1.1,
                color: COLORS.white,
                opacity: t,
                transform: `scale(${lerp(t, [0, 1], [0.9, 1])})`,
                letterSpacing: -1,
              }}
            >
              {text}
              {i === 2 ? (
                <div
                  style={{
                    position: "absolute",
                    left: 0,
                    bottom: -14,
                    height: 4,
                    width: `${line * 100}%`,
                    background: COLORS.green,
                    borderRadius: 2,
                  }}
                />
              ) : null}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
