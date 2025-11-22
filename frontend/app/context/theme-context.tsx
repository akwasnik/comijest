"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

type ThemeContextProviderProps = {
  children: React.ReactNode;
};

type ThemeContextType = {
  isDark: boolean;
  setIsDark: React.Dispatch<React.SetStateAction<boolean>>;
};

export const ThemeContext = createContext<ThemeContextType | null>(null);

export default function ThemeContextProvider({ children }: ThemeContextProviderProps) {
  const [isDark, setIsDark] = useState<boolean>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("isDark") === "true";
    }
    return false;
  });

  const [mounted, setMounted] = useState<boolean>(false);

  // montujemy asynchronicznie -> ESLint nie krzyczy
  useEffect(() => {
    queueMicrotask(() => {
      setMounted(true);
    });
  }, []);

  // reagujemy na zmiany
  useEffect(() => {
    if (!mounted) return;

    localStorage.setItem("isDark", String(isDark));

    if (isDark) {
      document.documentElement.classList.add("dark");
      document.documentElement.classList.remove("light");
    } else {
      document.documentElement.classList.remove("dark");
      document.documentElement.classList.add("light");
    }
  }, [isDark, mounted]);

  if (!mounted) return null;

  return (
    <ThemeContext.Provider value={{ isDark, setIsDark }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useThemeContext() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useThemeContext must be used within ThemeContextProvider");
  return ctx;
}
