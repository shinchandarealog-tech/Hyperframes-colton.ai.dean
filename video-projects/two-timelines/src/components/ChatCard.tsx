import React from "react";
import { OffthreadVideo, Sequence, staticFile } from "remotion";
import { COLORS, FONTS } from "../theme";
import { lerp, pop, smooth, typed } from "../lib/anim";
import { WhiteCard } from "./WhiteCard";

export type Recording = { file: string; durationSec: number } | null;

/**
 * White card with a Claude chat. If a screen recording exists it plays inside the
 * card (cropped to fill, sped up to fit). Otherwise: a typed user prompt and a
 * streamed reply under a plain "Claude" text label (no logo / brand mark).
 */
export const ChatCard: React.FC<{
  frame: number; // absolute frame
  shotFrom: number; // absolute start of the enclosing <Sequence>
  shotTo: number;
  x: number;
  y: number;
  w: number;
  h: number;
  inAt: number;
  prompt: string;
  typing: { from: number; to: number };
  reply?: string[];
  replyFrom?: number;
  replyTo?: number;
  fontSize?: number;
  recording?: Recording;
  children?: React.ReactNode; // custom reply body
  replyLabelAt?: number;
}> = ({
  frame,
  shotFrom,
  shotTo,
  x,
  y,
  w,
  h,
  inAt,
  prompt,
  typing,
  reply = [],
  replyFrom = typing.to + 4,
  replyTo = replyFrom + 30,
  fontSize = 24,
  recording,
  children,
  replyLabelAt,
}) => {
  const p = pop(frame, inAt);
  const shown = typed(prompt, frame, typing.from, typing.to);
  const isTyping = frame >= typing.from && frame < typing.to + 4;
  const caretOn = isTyping && Math.floor(frame / 4) % 2 === 0;
  const labelAt = replyLabelAt ?? replyFrom;
  const perLine = reply.length ? (replyTo - replyFrom) / reply.length : 0;

  if (recording) {
    const startLocal = typing.from - shotFrom;
    const windowFrames = shotTo - typing.from;
    const rate = Math.max(0.25, (recording.durationSec * 30) / windowFrames);
    return (
      <WhiteCard x={x} y={y} w={w} h={h} scale={p.scale} opacity={p.opacity}>
        <Sequence from={startLocal} layout="none">
          <OffthreadVideo
            src={staticFile(recording.file)}
            playbackRate={rate}
            muted
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </Sequence>
      </WhiteCard>
    );
  }

  return (
    <WhiteCard x={x} y={y} w={w} h={h} scale={p.scale} opacity={p.opacity}>
      <div style={{ padding: 34, display: "flex", flexDirection: "column", gap: 16, fontFamily: FONTS.inter }}>
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <div
            style={{
              maxWidth: "86%",
              background: COLORS.bubble,
              color: COLORS.cardText,
              fontWeight: 500,
              fontSize,
              lineHeight: 1.32,
              padding: "14px 20px",
              borderRadius: 22,
              borderBottomRightRadius: 6,
              minHeight: fontSize * 1.32,
              opacity: frame >= typing.from ? 1 : 0,
            }}
          >
            {shown}
            <span style={{ opacity: caretOn ? 1 : 0, marginLeft: 1 }}>|</span>
          </div>
        </div>
        <div style={{ opacity: lerp(frame, [labelAt, labelAt + 4], [0, 1]) }}>
          <div style={{ fontSize: 19, fontWeight: 600, color: COLORS.cardMuted, letterSpacing: 0.4, marginBottom: 8 }}>
            Claude
          </div>
          {children ??
            reply.map((line, i) => {
              const t = smooth(frame, replyFrom + i * perLine, 6);
              return (
                <div
                  key={i}
                  style={{
                    fontSize: fontSize - 1,
                    fontWeight: 500,
                    lineHeight: 1.36,
                    color: COLORS.cardText,
                    opacity: t,
                    transform: `translateY(${(1 - t) * 8}px)`,
                  }}
                >
                  {line}
                </div>
              );
            })}
        </div>
      </div>
    </WhiteCard>
  );
};
