"use client";

import Image from "next/image";
import Link from "next/link";
import { User, LogOut } from "lucide-react";
import { AnimatedThemeToggler } from "./ui/animated-theme-toggler";
import { useUser } from "@/app/context/UserContext";

export default function Header() {
  const { isAuthenticated, isLoading, logout } = useUser();

  return (
    <header className="w-full bg-transparent shadow-sm shadow-red-300 py-5 px-6">
      <div className="mx-auto flex justify-between items-center">

        <Link href="/" className="flex flex-col items-start">
          <Image src="/logo.png" alt="Comijest logo" width={60} height={60} />
          <Image
            src="/logoText.png"
            alt="Comijest"
            width={60}
            height={60}
            className="absolute top-11 left-5.5"
          />
        </Link>

        <AnimatedThemeToggler />

        <div className="flex items-center gap-6 pr-2">
          <Link
            href="/onas"
            className="text-md font-bold text-red-400 hover:text-red-700"
          >
            O nas
          </Link>

          {!isLoading && (
            <>
              {isAuthenticated ? (
                <>
                  <Link
                    href="/profile"
                    className="text-red-400 hover:text-red-700"
                    title="Profil"
                  >
                    <User size={30} />
                  </Link>

                  <button
                    onClick={logout}
                    className="text-red-400 hover:text-red-700"
                    title="Wyloguj"
                  >
                    <LogOut size={26} />
                  </button>
                </>
              ) : (
                <Link
                  href="/login"
                  className="text-red-400 hover:text-red-700 font-bold"
                >
                  Zaloguj
                </Link>
              )}
            </>
          )}
        </div>
      </div>
    </header>
  );
}
