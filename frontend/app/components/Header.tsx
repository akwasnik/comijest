import Image from "next/image";
import { User } from "lucide-react";
import { AnimatedThemeToggler } from "./ui/animated-theme-toggler";

export default function Header() {
  return (
    <header className="w-full bg-transparent shadow-sm shadow-red-300 py-5 px-6">
      <div className="mx-auto flex justify-between items-center">
        
        <a href="/" className="flex flex-col items-start">
          <Image 
            src="/logo.png"
            alt="Comijest logo"
            width={60}
            height={60}
            className="mb-1"
          />

          <Image 
            src="/logoText.png"
            alt="Comijest"
            width={60}
            height={60}
            className="absolute top-11 left-5.5"
          />
        </a>
        <AnimatedThemeToggler />
        <div className="flex items-center gap-6 pr-2">
          <a href="/about" className="text-md font-bold text-red-400 hover:text-red-700">
            O nas
          </a>

          <a href="/account" className="text-red-400 hover:text-red-700">
            <User size={30} />
          </a>
        </div>
      </div>
    </header>
  );
}
