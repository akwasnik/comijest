"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { useEffect } from "react";

export default function ErrorPage({ error, reset }: { error: Error; reset: () => void }) {

  useEffect(() => {
    console.error("ERROR:", error);
  }, [error]);

  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center px-6">
      
      <motion.img
        src="/bandage.png"
        alt="error icon"
        className="w-28 mb-6"
        initial={{ scale: 0, rotate: -20 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ duration: 0.6, type: "spring" }}
       />

      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="text-2xl md:text-3xl font-semibold mb-3"
      >
        Wystąpił błąd!
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="text-gray-600 max-w-md mb-8"
      >
        Coś poszło nie tak podczas ładowania strony.  
        Spróbuj ponownie lub wróć na stronę główną.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.4 }}
      >
        <Link
          href="/"
          className="px-6 py-3 rounded-xl bg-blue-600 text-white text-lg font-medium shadow-lg hover:bg-blue-700 transition-all hover:shadow-xl"
        >
          Strona główna
        </Link>
      </motion.div>
    </div>
  );
}
