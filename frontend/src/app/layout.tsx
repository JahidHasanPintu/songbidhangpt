import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SongbidhanGPT — বাংলাদেশ সংবিধান AI",
  description: "Ask anything about the Constitution of Bangladesh in Bangla or English",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="bn">
      <body>{children}</body>
    </html>
  );
}