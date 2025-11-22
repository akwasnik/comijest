// lenis-provider.tsx
"use client";
import { ReactLenis, LenisRef } from "lenis/react";
import { useRef } from "react";

type LenisScrollProviderProps = {
  children: React.ReactNode;
};

export default function SmoothScrollProvider({ children }: LenisScrollProviderProps) {
  const lenisRef = useRef< LenisRef | null >(null);

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