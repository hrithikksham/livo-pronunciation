import type { Metadata } from "next";
import { Instrument_Sans, IBM_Plex_Mono } from "next/font/google";

import "./globals.css";
import { ConsentGate } from "./ConsentGate";

const instrumentSans = Instrument_Sans({
  variable: "--font-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const plexMono = IBM_Plex_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "LIVO — AI Pronunciation Scorer",
  description:
    "AI-powered English pronunciation analysis using Whisper and LLM feedback.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${instrumentSans.variable} ${plexMono.variable} antialiased bg-[#0F1113]`}
      >
        <ConsentGate>{children}</ConsentGate>
      </body>
    </html>
  );
}