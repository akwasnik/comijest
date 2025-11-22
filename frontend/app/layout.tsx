import type { Metadata } from "next";
import "./globals.css";
import Header from "./components/Header";
import Footer from "./components/Footer";


// LENIS SMOOTH SCROLL

import SmoothScrollProvider from "./providers/SmoothScrollProvider";
import ThemeContextProvider from "./context/theme-context";


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
          <ThemeContextProvider>
            <Header />
            <SmoothScrollProvider>{children}</SmoothScrollProvider>
            <Footer />
          </ThemeContextProvider>
        </body>
    </html>
  );
}
