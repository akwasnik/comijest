import type { Metadata } from "next";
import "./globals.css";
import Header from "./components/Header";
import Footer from "./components/Footer";
import SmoothScrollProvider from "./providers/SmoothScrollProvider";
import CustomThemeProvider from "./providers/ThemeProvider";

export const metadata: Metadata = {
  title: "Comijest",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pl" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col">
        <CustomThemeProvider>
          <Header />
          <SmoothScrollProvider>{children}</SmoothScrollProvider>
          <Footer />
        </CustomThemeProvider>
      </body>
    </html>
  );
}
