// lenis-provider.tsx
"use client";
import { ReactLenis } from "lenis/react";
import { FC, useRef } from "react";

type LenisScrollProviderProps = {
  children: React.ReactNode;
};

export default function SmoothScrollProvider({ children }: LenisScrollProviderProps) {
  const lenisRef = useRef<any>(null);

  return (
    <ReactLenis 
      ref={lenisRef}
      root
      options={{
        lerp: 0.1,
        duration: 1.5,
        smoothWheel: true
      }}
    >
      {children}
    </ReactLenis>
  );
}