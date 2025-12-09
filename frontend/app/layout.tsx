import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Air Quality Monitor",
  description: "Real-time indoor air quality dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0f172a] text-slate-100 antialiased min-h-screen selection:bg-emerald-500/30">
        {children}
      </body>
    </html>
  );
}
