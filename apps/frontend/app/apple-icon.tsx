import { signMark } from "./icon";

export const size = { width: 180, height: 180 };
export const contentType = "image/png";

// iOS ignores transparency on home-screen icons: give it the sign's yellow field.
export default function AppleIcon() {
  return signMark(180, 0.12, "#ffce00");
}
