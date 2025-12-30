"use client";

import { motion, useReducedMotion } from "framer-motion";
import Link from "next/link";
import { useMounted } from "@/app/hooks/useMounted"

export default function CallToAction() {
  const mounted = useMounted();
  const reduceMotion = useReducedMotion();

  return (
    <section className="relative overflow-hidden py-16 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="relative bg-red-50/70 dark:bg-red-400/10 border border-red-100 dark:border-none rounded-3xl px-6 py-12 md:px-12 md:py-16 text-center shadow-[0_18px_40px_rgba(220,38,38,0.18)]">

          {mounted && !reduceMotion && (
            <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
              <div className="heartbeat-wrapper">
                <div className="heartbeat-ring heartbeat-ring-1" />
                <div className="heartbeat-ring heartbeat-ring-2" />
              </div>
            </div>
          )}

          <motion.h2 initial={false} animate={{ opacity: 1, y: 0 }}>
            Sprawdź co Ci jest
          </motion.h2>
        </div>
      </div>
    </section>
  );
}
