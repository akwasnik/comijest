import type { Metadata } from "next";
import "./globals.css";
import Header from "./components/Header";
import Footer from "./components/Footer";


// LENIS SMOOTH SCROLL

import { ReactLenis } from './utils/lenis';


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
      <ReactLenis root>
        <body className="min-h-screen flex flex-col">
          <Header />
          
          <main className="grow container mx-auto px-4 py-6">
            {children}
          </main>

          <Footer />
        </body>
      </ReactLenis>
    </html>
  );
}
