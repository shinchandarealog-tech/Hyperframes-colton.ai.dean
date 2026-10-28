import React from "react";
import { Audio, Loop, Sequence, staticFile } from "remotion";
import { hasStatic } from "../lib/files";
import { SFX } from "../sfx";
import {
  DURATION,
  MUSIC_DROP_IN_TRACK_FRAMES,
  MUSIC_DROP_TARGET,
  MUSIC_OFFSET_FRAMES,
  MUSIC_VOLUME,
  SFX_VOLUME,
} from "../timing";

export const Soundtrack: React.FC<{ loopFrames: Record<string, number> }> = ({ loopFrames }) => {
  // >0: skip into the track; <0: delay the track.
  const shift = MUSIC_DROP_IN_TRACK_FRAMES - MUSIC_DROP_TARGET - MUSIC_OFFSET_FRAMES;
  return (
    <>
      {hasStatic("music.mp3") ? (
        <Sequence from={Math.max(0, -shift)} durationInFrames={DURATION} layout="none">
          <Audio src={staticFile("music.mp3")} startFrom={Math.max(0, shift)} volume={MUSIC_VOLUME} />
        </Sequence>
      ) : null}
      {SFX.filter((c) => hasStatic(`sfx/${c.file}`)).map((c, i) => {
        const src = staticFile(`sfx/${c.file}`);
        const volume = (c.volume ?? 1) * SFX_VOLUME;
        if (c.loopUntil) {
          const len = loopFrames[c.file] ?? 30;
          return (
            <Sequence key={i} from={c.frame} durationInFrames={c.loopUntil - c.frame} layout="none">
              <Loop durationInFrames={len} layout="none">
                <Audio src={src} volume={volume} />
              </Loop>
            </Sequence>
          );
        }
        return (
          <Sequence key={i} from={c.frame} durationInFrames={c.frames} layout="none">
            <Audio src={src} volume={volume} />
          </Sequence>
        );
      })}
    </>
  );
};
