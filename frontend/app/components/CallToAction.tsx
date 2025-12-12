"use client";

import { motion, useReducedMotion } from "framer-motion";
import Link from "next/link";

export default function CallToAction() {
  const reduceMotion = useReducedMotion();

  return (
    <section className="relative overflow-hidden py-16 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="relative bg-red-50/70 dark:bg-red-400/10 border border-red-100 dark:border-none rounded-3xl px-6 py-12 md:px-12 md:py-16 text-center shadow-[0_18px_40px_rgba(220,38,38,0.18)]">

          {/* dekoracyjne animowane kółka */}
          {!reduceMotion && (
            <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
              <div className="heartbeat-wrapper">
                <div className="heartbeat-ring heartbeat-ring-1" />
                <div className="heartbeat-ring heartbeat-ring-2" />
              </div>
            </div>
          )}

          <motion.h2
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
            className="relative text-3xl md:text-4xl font-semibold text-red-700 mb-4"
          >
            Sprawdź co Ci jest
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.4 }}
            className="relative text-sm md:text-base text-red-900/80 dark:text-white max-w-xl mx-auto mb-8"
          >
            Zaznacz swoje objawy, a model AI zwróci Ci możliwą diagnozę.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.3 }}
            className="relative"
          >
            <Link
              href="/symptoms"
              className="inline-flex items-center justify-center px-8 py-3 rounded-full bg-red-600 text-white font-medium text-base md:text-lg shadow-lg hover:bg-red-700 transition hover:shadow-[0_0_25px_rgba(248,113,113,0.9)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 focus-visible:ring-offset-red-50"
            >
              Rozpocznij diagnozę
            </Link>
          </motion.div>

        </div>
      </div>
    </section>
  );
}
