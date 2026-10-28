import { Recording } from "../components/ChatCard";

export type Half = "top" | "bottom";
export type ShotProps = { half: Half; recordings?: Recording[] };
