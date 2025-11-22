"use client";

import { motion, useReducedMotion } from "framer-motion";
import Link from "next/link";

export default function CTA() {
  const prefersReducedMotion = useReducedMotion();

  return (
    <div className="relative flex flex-col items-center justify-center py-24">
      
      {!prefersReducedMotion && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">

          <motion.div
            className="absolute w-64 h-64 rounded-full bg-red-400 opacity-30 blur-2xl z-10"
            initial={{ scale: 0.8, opacity: 0.4 }}
            animate={{ scale: 1.4, opacity: 0 }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              repeatType: "loop",
              ease: "easeOut",
            }}
          />

          <motion.div
            className="absolute w-48 h-48 rounded-full bg-red-500 opacity-40 blur-xl z-10"
            initial={{ scale: 0.8, opacity: 0.4 }}
            animate={{ scale: 1.6, opacity: 0 }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              repeatType: "loop",
              delay: 0.2,
              ease: "easeOut",
            }}
          />

        </div>
      )}

      <motion.h2
        className="relative text-center text-4xl md:text-5xl font-bold text-red-600 drop-shadow-lg z-10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        Sprawdź co Ci jest
      </motion.h2>

      <motion.div
        className="mt-8 z-10"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
      >
        <Link
          href="/symptoms"
          className="px-8 py-4 text-lg font-semibold bg-red-600 hover:bg-red-700 text-white rounded-xl shadow-lg hover:shadow-2xl transition-all"
        >
          Rozpocznij diagnozę
        </Link>
      </motion.div>
    </div>
  );
}
