import React from "react";
import { AbsoluteFill, Easing, Sequence, useCurrentFrame } from "remotion";
import { Divider, Panel } from "./components/Panel";
import { Glow } from "./components/Glow";
import { Grain } from "./components/Grain";
import { Label } from "./components/Label";
import { Timer } from "./components/Timer";
import { Soundtrack } from "./components/Soundtrack";
import { Recording } from "./components/ChatCard";
import { lerp, noise, prog, smooth } from "./lib/anim";
import { COLORS, COPY, H, LAYOUT, W } from "./theme";
import { EXPORT, MESSAGE, SHOTS, SPLIT, TIMERS_OUT, WIGGLE, ShotKey, dur } from "./timing";
import { Shot01Hook } from "./shots/Shot01Hook";
import { Shot02Split } from "./shots/Shot02Split";
import { Shot03Script } from "./shots/Shot03Script";
import { Shot04Cuts } from "./shots/Shot04Cuts";
import { Shot05Captions } from "./shots/Shot05Captions";
import { Shot06Broll } from "./shots/Shot06Broll";
import { Shot07Grind } from "./shots/Shot07Grind";
import { Shot08Export } from "./shots/Shot08Export";
import { Shot09Message } from "./shots/Shot09Message";
import { Shot10Cta } from "./shots/Shot10Cta";
import { Half, ShotProps } from "./shots/types";

export type TwoTimelinesProps = {
  recordings: Recording[];
  loopFrames: Record<string, number>;
};

const SPLIT_SHOTS: [ShotKey, React.FC<ShotProps>][] = [
  ["split", Shot02Split],
  ["script", Shot03Script],
  ["cuts", Shot04Cuts],
  ["captions", Shot05Captions],
  ["broll", Shot06Broll],
  ["grind", Shot07Grind],
  ["exportShot", Shot08Export],
];

const HalfShots: React.FC<{ half: Half; recordings: Recording[] }> = ({ half, recordings }) => (
  <>
    {SPLIT_SHOTS.map(([key, Shot]) => (
      <Sequence
        key={key}
        name={`${key} (${half})`}
        from={SHOTS[key].from}
        // the export shot stays up underneath the wipe
        durationInFrames={dur(key) + (key === "exportShot" ? MESSAGE.wipe.to - SHOTS.message.from : 0)}
      >
        <Shot half={half} recordings={recordings} />
      </Sequence>
    ))}
  </>
);

export const TwoTimelines: React.FC<TwoTimelinesProps> = ({ recordings, loopFrames }) => {
  const frame = useCurrentFrame();

  // Shot 2: panels slide in, divider draws from the centre.
  const slide = smooth(frame, SPLIT.panelsIn.from, SPLIT.panelsIn.to - SPLIT.panelsIn.from);
  const topOffset = -(1 - slide) * LAYOUT.topPanel.h;
  const bottomOffset = (1 - slide) * LAYOUT.bottomPanel.h;
  const divider = smooth(frame, SPLIT.divider.from, SPLIT.divider.to - SPLIT.divider.from);

  // Hard side camera wiggle (~6 per second), grows in shot 7.
  const amp = frame < WIGGLE.start ? 0 : lerp(frame, [SHOTS.grind.from, SHOTS.grind.from + 10], [WIGGLE.amp, WIGGLE.ampGrind]);
  const t = (frame * WIGGLE.perSecond) / 30;
  const wx = noise("wiggle-x", t) * amp;
  const wy = noise("wiggle-y", t) * amp;

  // Shot 8: 2-frame 8px shake on the bottom panel only.
  const shakeX = frame >= EXPORT.slam && frame < EXPORT.slam + EXPORT.shakeLen ? (frame === EXPORT.slam ? 8 : -8) : 0;

  // Shot 9: bottom panel wipes up over the whole frame.
  const wipe = prog(frame, MESSAGE.wipe.from, MESSAGE.wipe.to, Easing.inOut(Easing.cubic));
  const bottomTop = LAYOUT.bottomPanel.y * (1 - wipe);
  const bottomContent = 1 - prog(frame, MESSAGE.wipe.from, MESSAGE.wipe.from + 8);
  const timersOn = frame < TIMERS_OUT;

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.pageBg }}>
      <Glow />

      <Sequence name="1 · Hook" from={0} durationInFrames={SPLIT.hookOut.to}>
        <Shot01Hook />
      </Sequence>

      {frame >= SPLIT.panelsIn.from ? (
        <>
          {/* TOP: the hard way */}
          {frame < MESSAGE.wipe.to ? (
            <Panel top={0} bottom={LAYOUT.topPanel.h} bg={COLORS.topPanel} offsetY={topOffset}>
              <AbsoluteFill style={{ transform: `translate(${wx}px, ${wy}px)` }}>
                <HalfShots half="top" recordings={recordings} />
              </AbsoluteFill>
              {frame >= SPLIT.textureStart ? <Grain width={W} height={LAYOUT.topPanel.h} /> : null}
              <Label frame={frame} side="top" text={COPY.topLabel} />
              {timersOn ? <Timer frame={frame} side="top" /> : null}
            </Panel>
          ) : null}

          <Divider progress={divider} />

          {/* BOTTOM: the smart way */}
          <Panel
            top={bottomTop}
            bottom={H}
            bg={COLORS.bottomPanel}
            offsetY={bottomOffset}
            background={<Glow opacity={wipe} />}
          >
            <AbsoluteFill style={{ transform: `translateX(${shakeX}px)`, opacity: bottomContent }}>
              <HalfShots half="bottom" recordings={recordings} />
              <Label frame={frame} side="bottom" text={COPY.bottomLabel} />
              {timersOn ? <Timer frame={frame} side="bottom" /> : null}
            </AbsoluteFill>
          </Panel>
        </>
      ) : null}

      <Sequence name="9 · Message" from={SHOTS.message.from} durationInFrames={dur("message")}>
        <Shot09Message />
      </Sequence>
      <Sequence name="10 · CTA" from={SHOTS.cta.from} durationInFrames={dur("cta")}>
        <Shot10Cta />
      </Sequence>

      <Soundtrack loopFrames={loopFrames} />
    </AbsoluteFill>
  );
};
