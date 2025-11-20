import Image from "next/image";
import { User } from "lucide-react";

export default function Header() {
  return (
    <header className="w-full bg-white shadow-sm shadow-red-300 py-5 px-6">
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

        <div className="flex items-center gap-6">
          <a href="/about" className="text-sm font-medium text-red-400 hover:text-red-700">
            O nas
          </a>

          <a href="/account" className="text-red-400 hover:text-red-700">
            <User size={26} />
          </a>
        </div>
      </div>
    </header>
  );
}
