import React from "react";
import { CalculateMetadataFunction, Composition, staticFile } from "remotion";
import { parseMedia } from "@remotion/media-parser";
import { TwoTimelines, TwoTimelinesProps } from "./TwoTimelines";
import { Recording } from "./components/ChatCard";
import { hasStatic } from "./lib/files";
import { SFX } from "./sfx";
import { DURATION, FPS } from "./timing";
import { H, W } from "./theme";

const durationOf = async (file: string) => {
  const { slowDurationInSeconds } = await parseMedia({
    src: staticFile(file),
    fields: { slowDurationInSeconds: true },
    acknowledgeRemotionLicense: true,
  });
  return slowDurationInSeconds;
};

// Look for optional screen recordings + loop lengths before rendering.
const calculateMetadata: CalculateMetadataFunction<TwoTimelinesProps> = async ({ props }) => {
  const recordings: Recording[] = await Promise.all(
    [1, 2, 3, 4].map(async (n) => {
      const file = `recordings/prompt${n}.mp4`;
      if (!hasStatic(file)) return null;
      return { file, durationSec: await durationOf(file) };
    }),
  );
  const loopFrames: Record<string, number> = {};
  for (const cue of SFX.filter((c) => c.loopUntil)) {
    const file = `sfx/${cue.file}`;
    if (hasStatic(file)) loopFrames[cue.file] = Math.max(1, Math.round((await durationOf(file)) * FPS));
  }
  return { props: { ...props, recordings, loopFrames } };
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="TwoTimelines"
    component={TwoTimelines}
    width={W}
    height={H}
    fps={FPS}
    durationInFrames={DURATION}
    defaultProps={{ recordings: [null, null, null, null], loopFrames: {} }}
    calculateMetadata={calculateMetadata}
  />
);
