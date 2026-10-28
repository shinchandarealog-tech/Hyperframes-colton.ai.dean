import { getStaticFiles } from "@remotion/studio";

/** True when a file exists in /public (checked at bundle time). */
export const hasStatic = (name: string): boolean => {
  try {
    return getStaticFiles().some((f) => f.name === name);
  } catch {
    return false;
  }
};
