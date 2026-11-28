import type { Metadata } from "next";
import "./global.css";

export const metadata: Metadata = {
  title: "GitVerse — AI-Powered Developer Intelligence",
  description: "Explore GitHub profiles, analyze codebases with AI, and generate ATS-ready portfolios.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased selection:bg-indigo-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}