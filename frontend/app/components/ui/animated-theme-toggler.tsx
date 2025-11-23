"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Moon, Sun } from "lucide-react";
import { flushSync } from "react-dom";
import { cn } from "@/app/lib/utils";
import { Spinner } from "./spinner";
import { useTheme } from "next-themes";

interface AnimatedThemeTogglerProps
  extends React.ComponentPropsWithoutRef<"button"> {
  duration?: number;
}

export const AnimatedThemeToggler = ({
  className,
  duration = 400,
  ...props
}: AnimatedThemeTogglerProps) => {
  const [mounted, setMounted] = useState(false)
  const {setTheme, resolvedTheme} =  useTheme();
  const buttonRef = useRef<HTMLButtonElement>(null);

    const toggleTheme = useCallback(async () => {
    if (!buttonRef.current) return;
    const newTheme = resolvedTheme === "dark" ? false : true;

    await document.startViewTransition(() => {
      flushSync(() => {
        setTheme(newTheme ? "dark" : "light");
      });
    }).ready;
    
    const { top, left, width, height } =
    buttonRef.current.getBoundingClientRect();
    const x = left + width / 2;
    const y = top + height / 2;
    const maxRadius = Math.hypot(
      Math.max(left, window.innerWidth - left),
      Math.max(top, window.innerHeight - top)
    );

    document.documentElement.animate(
      {
        clipPath: [
          `circle(0px at ${x}px ${y}px)`,
          `circle(${maxRadius}px at ${x}px ${y}px)`
        ],
      },
      {
        duration,
        easing: "ease-in-out",
        pseudoElement: "::view-transition-new(root)",
      }
    );
    
  }, [duration, resolvedTheme, setTheme]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setMounted(true);
  }, []);

  if (!mounted) return (
      <Spinner className="text-red-500"/>
  );

  return (
    <button
      ref={buttonRef}
      onClick={toggleTheme}
      className={cn(className, "text-red-500")}
      {...props}
    >
      {resolvedTheme === "dark" ? <Sun /> : <Moon />}
      <span className="sr-only">Toggle theme</span>
    </button>
  );
};
