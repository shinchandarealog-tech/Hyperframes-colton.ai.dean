import React from "react";
import { AbsoluteFill } from "remotion";
import { HARD_FILTER } from "../theme";

/** Desaturated "hard way" grade. Red accents are placed outside of it on purpose. */
export const HardGrade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ filter: HARD_FILTER }}>{children}</AbsoluteFill>
);
