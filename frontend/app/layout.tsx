import type { Metadata } from "next";
import "./globals.css";
import Header from "./components/Header";
import Footer from "./components/Footer";


// LENIS SMOOTH SCROLL

import SmoothScrollProvider from "./providers/SmoothScrollProvider";


export const metadata: Metadata = {
  title: "Comijest",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pl">
      
        <body className="min-h-screen flex flex-col">
            <Header />
            <SmoothScrollProvider>{children}</SmoothScrollProvider>
            <Footer />
        </body>
    </html>
  );
}
