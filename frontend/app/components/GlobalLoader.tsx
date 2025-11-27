"use client";

import { useEffect, useState } from "react";
import Image from "next/image";

export default function GlobalLoader() {
  const [visible, setVisible] = useState(true);
  const [shouldRender, setShouldRender] = useState(true);

  useEffect(() => {
    const MIN_TIME = 600;

    const timer = setTimeout(() => {
      setVisible(false);
    }, MIN_TIME);

    return () => clearTimeout(timer);
  }, []);

// ODLACZANIE KOMPONENTU DLA OPTYMALNOSCI

  useEffect(() => {
    if (!visible) {
      const timeout = setTimeout(() => {
        setShouldRender(false);
      }, 700);

      return () => clearTimeout(timeout);
    }
  }, [visible]);

  if (!shouldRender) return null;

  return (
    <div
      className={`
        fixed inset-0 z-9999
        flex items-center justify-center
        bg-white dark:bg-neutral-950
        transition-opacity duration-500 
        ${visible ? "opacity-100" : "opacity-0 pointer-events-none"}
      `}
    >
      
      <div className="flex flex-col items-center gap-3">
        <Image
          src="/logo.png"
          width={70}
          height={70}
          alt="Comijest logo"
          className="animate-pulse"
        />
        <p className="text-red-500 font-semibold animate-pulse">
          Ładowanie...
        </p>
      </div>
    </div>
  );
}
