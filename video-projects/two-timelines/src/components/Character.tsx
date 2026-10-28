import React from "react";

const SKIN = "#E9B48A";
const HAIR = "#6E4A33";
const SHIRT = "#2FD06B";
const SHIRT_DARK = "#24A855";
const LAPTOP = "#D7DBD3";
const LAPTOP_EDGE = "#B9BEB4";
const DESK = "#5B6157";
const DESK_DARK = "#454A42";
const INK = "#1E1B19";

/**
 * Flat editor at a desk with a laptop (seen from behind the screen).
 * Same design for both halves; `pose` changes posture + face.
 */
export const Character: React.FC<{
  x: number; // centre x
  y: number; // centre y
  pose: "slumped" | "relaxed";
  scale?: number;
  headDrop?: number; // 0..1, slumped head sinking toward desk
  typing?: number; // frame-driven arm bob
  opacity?: number;
  blink?: boolean;
}> = ({ x, y, pose, scale = 1, headDrop = 0, typing = 0, opacity = 1, blink = false }) => {
  const W = 440;
  const H = 380;
  const slumped = pose === "slumped";
  const bodyY = slumped ? 16 : 0;
  const headY = (slumped ? 22 : 0) + headDrop * 62;
  const headRot = (slumped ? 9 : -3) + headDrop * 14;
  const armBob = Math.sin(typing * 1.3) * 3;
  return (
    <svg
      width={W}
      height={H}
      viewBox={`0 0 ${W} ${H}`}
      style={{
        position: "absolute",
        left: x - W / 2,
        top: y - H / 2,
        transform: `scale(${scale})`,
        transformOrigin: "50% 50%",
        opacity,
        overflow: "visible",
      }}
    >
      {/* torso */}
      <g transform={`translate(0 ${bodyY})`}>
        <path
          d={
            slumped
              ? "M122 290 C118 246 140 196 220 192 C300 196 322 246 318 290 Z"
              : "M128 306 C126 236 150 178 220 176 C290 178 314 236 312 306 Z"
          }
          fill={SHIRT}
        />
        {/* collar */}
        <path d={slumped ? "M196 196 Q220 214 244 196" : "M196 180 Q220 200 244 180"} stroke={SHIRT_DARK} strokeWidth={6} fill="none" strokeLinecap="round" />
        {/* arms reaching to keyboard */}
        <path
          d={`M150 ${slumped ? 236 : 222} Q120 280 168 ${300 + armBob}`}
          stroke={SHIRT_DARK}
          strokeWidth={30}
          fill="none"
          strokeLinecap="round"
        />
        <path
          d={`M290 ${slumped ? 236 : 222} Q320 280 272 ${300 - armBob}`}
          stroke={SHIRT_DARK}
          strokeWidth={30}
          fill="none"
          strokeLinecap="round"
        />
      </g>
      {/* head */}
      <g transform={`translate(0 ${headY}) rotate(${headRot} 220 176)`}>
        <rect x={204} y={150} width={32} height={34} rx={12} fill={SKIN} />
        <circle cx={160} cy={118} r={12} fill={SKIN} />
        <circle cx={280} cy={118} r={12} fill={SKIN} />
        <circle cx={220} cy={112} r={62} fill={SKIN} />
        <path d="M158 104 C156 52 196 38 222 40 C262 40 288 66 282 104 C270 82 248 74 220 74 C190 74 168 84 158 104 Z" fill={HAIR} />
        {slumped ? (
          <g>
            {/* tired, half-closed eyes */}
            <path d="M190 116 Q198 112 206 116" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
            <path d="M234 116 Q242 112 250 116" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
            <path d="M190 126 Q198 130 206 126" stroke="#B98463" strokeWidth={3} fill="none" strokeLinecap="round" />
            <path d="M234 126 Q242 130 250 126" stroke="#B98463" strokeWidth={3} fill="none" strokeLinecap="round" />
            <path d="M206 150 Q220 144 234 150" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
          </g>
        ) : (
          <g>
            {blink ? (
              <>
                <path d="M192 116 L204 116" stroke={INK} strokeWidth={5} strokeLinecap="round" />
                <path d="M236 116 L248 116" stroke={INK} strokeWidth={5} strokeLinecap="round" />
              </>
            ) : (
              <>
                <circle cx={198} cy={115} r={6.5} fill={INK} />
                <circle cx={242} cy={115} r={6.5} fill={INK} />
              </>
            )}
            <circle cx={186} cy={134} r={8} fill="#F09B86" opacity={0.45} />
            <circle cx={254} cy={134} r={8} fill="#F09B86" opacity={0.45} />
            <path d="M204 140 Q220 154 236 140" stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />
          </g>
        )}
      </g>
      {/* laptop (back of screen) */}
      <path d="M134 212 L306 212 Q314 212 313 220 L306 298 L134 298 L127 220 Q126 212 134 212 Z" fill={LAPTOP} />
      <path d="M134 212 L306 212 Q314 212 313 220 L312 228 L128 228 L127 220 Q126 212 134 212 Z" fill={LAPTOP_EDGE} opacity={0.6} />
      <rect x={112} y={296} width={216} height={10} rx={5} fill={LAPTOP_EDGE} />
      {/* desk */}
      <rect x={10} y={304} width={420} height={22} rx={8} fill={DESK} />
      <rect x={40} y={326} width={18} height={54} fill={DESK_DARK} />
      <rect x={382} y={326} width={18} height={54} fill={DESK_DARK} />
    </svg>
  );
};
