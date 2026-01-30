"use client";

import { SVGProps, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useMutation } from "@tanstack/react-query";
import {
  Activity,
  Thermometer,
  Waves,
  Wind,
  HeartPulse,
  Stethoscope,
  Droplets,
  Brain,
  Eye,
  Ear,
  Skull,
  Hand,
  Footprints,
  Pill,
  Soup,
  Zap,
  Flame,
  AlertTriangle,
  BadgeHelp,
  Moon,
  Sun,
  ShieldAlert,
  Sparkles,
  Utensils,
  MoveDown,
  MoveUp,
  MessageSquare,
} from "lucide-react";

type DiagnosePayload = {
  symptoms: string[];
  userinput: string;
};

type DiagnoseApiResponse = {
  top5: {
    label_pl: string;
    prob: number;
  }[];
};


type SymptomOption = {
  key: string;
  label: string;
  icon: React.ComponentType<SVGProps<SVGSVGElement>>;
};

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.04, delayChildren: 0.05 },
  },
};

const item = {
  hidden: { opacity: 0, y: 10, scale: 0.98 },
  show: { opacity: 1, y: 0, scale: 1 },
};

export default function DiagnosePage() {
  const options: SymptomOption[] = useMemo(
    () => [
      { key: "fever", label: "Gorączka", icon: Thermometer },
      { key: "chills", label: "Dreszcze", icon: Snowish },
      { key: "cough", label: "Kaszel", icon: Wind },
      { key: "sore_throat", label: "Ból gardła", icon: Skull },
      { key: "runny_nose", label: "Katar", icon: Droplets },
      { key: "shortness_of_breath", label: "Duszność", icon: Waves },
      { key: "chest_pain", label: "Ból w klatce", icon: HeartPulse },
      { key: "palpitations", label: "Kołatanie serca", icon: Activity },
      { key: "headache", label: "Ból głowy", icon: Brain },
      { key: "dizziness", label: "Zawroty głowy", icon: MoveUp },
      { key: "fainting", label: "Omdlenie", icon: MoveDown },
      { key: "nausea", label: "Nudności", icon: Soup },
      { key: "vomiting", label: "Wymioty", icon: Utensils },
      { key: "diarrhea", label: "Biegunka", icon: Waves },
      { key: "abdominal_pain", label: "Ból brzucha", icon: Pill },
      { key: "heartburn", label: "Zgaga", icon: Flame },
      { key: "fatigue", label: "Zmęczenie", icon: Moon },
      { key: "insomnia", label: "Bezsenność", icon: Sun },
      { key: "muscle_pain", label: "Ból mięśni", icon: Hand },
      { key: "joint_pain", label: "Ból stawów", icon: Footprints },
      { key: "back_pain", label: "Ból pleców", icon: Stethoscope },
      { key: "neck_pain", label: "Ból szyi", icon: Stethoscope },
      { key: "rash", label: "Wysypka", icon: Sparkles },
      { key: "itching", label: "Swędzenie", icon: Sparkles },
      { key: "swelling", label: "Obrzęk", icon: Droplets },
      { key: "eye_pain", label: "Ból oka", icon: Eye },
      { key: "blurred_vision", label: "Zamglone widzenie", icon: Eye },
      { key: "ear_pain", label: "Ból ucha", icon: Ear },
      { key: "tinnitus", label: "Szum w uszach", icon: Ear },
      { key: "toothache", label: "Ból zęba", icon: Zap },
      { key: "anxiety", label: "Lęk / niepokój", icon: BadgeHelp },
      { key: "confusion", label: "Splątanie", icon: AlertTriangle },
      { key: "severe_pain", label: "Silny ból", icon: ShieldAlert },
    ],
    []
  );

  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [userinput, setUserinput] = useState("");
  const [result, setResult] = useState<DiagnoseApiResponse | null>(null);


  const selectedLabels = useMemo(
    () =>
      options
        .filter((o) => selected.has(o.key))
        .map((o) => o.label),
    [options, selected]
  );
  
  const mutation = useMutation<DiagnoseApiResponse, Error, DiagnosePayload>({
    mutationFn: async (payload) => {
      const res = await fetch("/api/diagnose/diagnose", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      let data: unknown = null;

      try {
        data = await res.json();
      } catch {
        // response body empty or invalid JSON
      }

      if (!res.ok) {
        const errorMessage =
          typeof data === "object" && data !== null && "error" in data
            ? (data as { error?: string }).error
            : typeof data === "object" && data !== null && "msg" in data
            ? (data as { msg?: string }).msg
            : "Nie udało się wykonać diagnozy";

        throw new Error(errorMessage);
      }

      return data as DiagnoseApiResponse;
    },
    onSuccess: (data) => {
      setResult(data);
    },
  });
  
    const toggle = (key: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  const canSubmit = selected.size > 0 || userinput.trim().length > 0;

  const submit = () => {
    const payload: DiagnosePayload = {
      symptoms: selectedLabels,
      userinput: userinput.trim(),
    };
    setResult(null);
    mutation.mutate(payload);
  };

  return (
    <main className="mx-auto w-full max-w-6xl px-4 pb-16 pt-24">
      {/* Hero */}
      <motion.section
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease: "easeOut" }}
        className="
          relative overflow-hidden rounded-3xl border
          bg-background/70 p-6 shadow-xl backdrop-blur
        "
      >
        <div className="absolute inset-0 opacity-30 [mask-image:radial-gradient(ellipse_at_top,white,transparent_70%)]">
          <div className="h-full w-full bg-[linear-gradient(to_right,rgba(239,68,68,0.2),rgba(244,63,94,0.15),rgba(248,113,113,0.1))]" />
        </div>

        <div className="relative">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
                Diagnostyka objawów
              </h1>
              <p className="mt-2 max-w-2xl text-sm text-muted-foreground sm:text-base">
                Wybierz objawy z listy (minimum 1) lub opisz je własnymi słowami.
                Następnie kliknij <span className="font-semibold">Zbadaj</span>.
              </p>
            </div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1, duration: 0.3 }}
              className="hidden shrink-0 items-center gap-2 rounded-2xl border bg-background/60 px-4 py-3 text-sm shadow-sm md:flex"
            >
              <Stethoscope className="opacity-70" />
              <span className="text-muted-foreground">
                Doktor: <span className="font-medium">AI</span>
              </span>
            </motion.div>
          </div>

          {/* Selected chips */}
          <AnimatePresence>
            {(selected.size > 0 || userinput.trim()) && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 8 }}
                className="mt-5 flex flex-wrap items-center gap-2"
              >
                {selectedLabels.slice(0, 8).map((lbl) => (
                  <span
                    key={lbl}
                    className="rounded-full border bg-background/60 px-3 py-1 text-xs text-muted-foreground"
                  >
                    {lbl}
                  </span>
                ))}
                {selectedLabels.length > 8 && (
                  <span className="rounded-full border bg-background/60 px-3 py-1 text-xs text-muted-foreground">
                    +{selectedLabels.length - 8} więcej
                  </span>
                )}
                {userinput.trim() && (
                  <span className="rounded-full border bg-background/60 px-3 py-1 text-xs text-muted-foreground">
                    opis: “{truncate(userinput.trim(), 28)}”
                  </span>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.section>

      {/* Grid of symptoms */}
      <motion.section
        variants={container}
        initial="hidden"
        animate="show"
        className="mt-8"
      >
        <div className="mb-3 flex items-end justify-between gap-3">
          <h2 className="text-lg font-semibold sm:text-xl">
            Wybierz objawy
          </h2>
          <p className="text-xs text-muted-foreground sm:text-sm">
            Kliknij kafelek, aby dodać / usunąć.
          </p>
        </div>

        <motion.div
          variants={container}
          className="
            grid grid-cols-2 gap-3
            sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6
          "
        >
          {options.map((o) => {
            const active = selected.has(o.key);
            const Icon = o.icon;

            return (
              <motion.button
                key={o.key}
                variants={item}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => toggle(o.key)}
                className={[
                  "group relative overflow-hidden rounded-2xl border p-4 text-left shadow-sm transition",
                  "bg-background/70 backdrop-blur",
                  active
                    ? "border-red-500/70 ring-2 ring-red-500/30"
                    : "hover:border-red-500/30",
                ].join(" ")}
              >
                <div className="absolute inset-0 opacity-0 transition group-hover:opacity-100">
                  <div className="h-full w-full bg-[radial-gradient(circle_at_top,rgba(239,68,68,0.18),transparent_55%)]" />
                </div>

                <div className="relative flex items-start justify-between gap-2">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl border bg-background/60">
                    <Icon className={active ? "opacity-90" : "opacity-70"} />
                  </div>

                  <motion.div
                    initial={false}
                    animate={{ opacity: active ? 1 : 0, scale: active ? 1 : 0.9 }}
                    className="rounded-full border bg-background/60 px-2 py-1 text-[10px] text-muted-foreground"
                  >
                    wybrane
                  </motion.div>
                </div>

                <div className="relative mt-3">
                  <p className="text-sm font-semibold leading-tight">
                    {o.label}
                  </p>
                  <p className="mt-1 text-[11px] text-muted-foreground">
                    {active ? "Dodane do listy" : "Kliknij, aby dodać"}
                  </p>
                </div>
              </motion.button>
            );
          })}
        </motion.div>
      </motion.section>
      <AnimatePresence>
        {!!result && (
          <motion.section
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 40 }}
            transition={{ duration: 0.6 }}
            className="
              mt-14 rounded-[2.5rem] border
              bg-background/80 p-8 shadow-2xl backdrop-blur
            "
          >
            <h2 className="text-2xl font-bold tracking-tight">
              Najbardziej prawdopodobne diagnozy
            </h2>

            <p className="mt-2 text-sm text-muted-foreground">
              Wyniki uszeregowane według prawdopodobieństwa
            </p>

            <div className="mt-8 space-y-4">
              {result.top5
                .sort((a, b) => b.prob - a.prob)
                .map((d, idx) => {
                  const percent = Math.round(d.prob * 100);

                  return (
                    <motion.div
                      key={d.label_pl}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.08 }}
                      className={[
                        "rounded-2xl border p-5 shadow-sm",
                        "bg-background/70",
                        idx === 0
                          ? "border-red-500/60 ring-2 ring-red-500/30"
                          : "",
                      ].join(" ")}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-muted-foreground">
                            #{idx + 1}
                          </p>
                          <p className="text-lg font-semibold">
                            {d.label_pl}
                          </p>
                        </div>

                        <div className="text-right">
                          <p className="text-2xl font-bold text-red-500">
                            {percent}%
                          </p>
                        </div>
                      </div>

                      {/* progress bar */}
                      <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-muted">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${percent}%` }}
                          transition={{ duration: 0.6, ease: "easeOut" }}
                          className="h-full bg-red-500"
                        />
                      </div>
                    </motion.div>
                  );
                })}
            </div>

            <p className="mt-6 text-xs text-muted-foreground">
              ⚠️ Wynik ma charakter informacyjny i nie zastępuje konsultacji lekarskiej.
            </p>
          </motion.section>
        )}
      </AnimatePresence>
      <motion.section
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05, duration: 0.4, ease: "easeOut" }}
        className="mt-10 grid gap-4 lg:grid-cols-3"
      >
        {/* textarea */}
        <div className="lg:col-span-2">
          <div className="rounded-3xl border bg-background/70 p-5 shadow-sm backdrop-blur">
            <h3 className="text-base font-semibold">
              Dodatkowy opis (opcjonalnie)
            </h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Np. „wieczorami boli mnie szyja z lewej strony”.
            </p>

            <textarea
              value={userinput}
              onChange={(e) => setUserinput(e.target.value)}
              rows={5}
              className="
                mt-4 w-full resize-none rounded-2xl border
                bg-white p-4 text-sm outline-none
                focus:ring-2 focus:ring-red-500
                dark:bg-neutral-800 dark:border-neutral-700
              "
              placeholder="Opisz, co dokładnie czujesz, kiedy, od kiedy, co pomaga..."
            />

            <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
              <span>{userinput.trim().length}/600</span>
              <span className="hidden sm:inline">
                Tip: uwzględnij czas trwania, stronę ciała, nasilenie
              </span>
            </div>
          </div>
        </div>

        {/* submit card */}
        <div className="lg:col-span-1">
          <div className="rounded-3xl border bg-background/70 p-5 shadow-sm backdrop-blur">
            <h3 className="text-base font-semibold">Gotowe?</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Wybrane objawy:{" "}
              <span className="font-semibold">{selected.size}</span>
            </p>

            <div className="mt-5 space-y-3">
              <motion.button
                whileHover={{ scale: canSubmit ? 1.02 : 1 }}
                whileTap={{ scale: canSubmit ? 0.98 : 1 }}
                onClick={submit}
                disabled={!canSubmit || mutation.isPending}
                className="
                  w-full rounded-2xl bg-red-500 px-4 py-3
                  font-semibold text-white shadow-md
                  transition hover:bg-red-600
                  disabled:opacity-60
                "
              >
                {mutation.isPending ? "Badam..." : "Zbadaj"}
              </motion.button>

              <button
                onClick={() => {
                  setSelected(new Set());
                  setUserinput("");
                  setResult(null);
                }}
                className="
                  w-full rounded-2xl border bg-background/60 px-4 py-3
                  text-sm font-semibold text-muted-foreground
                  transition hover:bg-muted
                "
              >
                Wyczyść
              </button>
            </div>
          </div>
        </div>
      </motion.section>
      <AnimatePresence>
            {mutation.isPending && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="
                    fixed inset-0 z-50 flex items-center justify-center
                    bg-background/80 backdrop-blur-xl
                  "
                >
                  <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="
                      flex flex-col items-center gap-6
                      rounded-3xl border bg-background/70
                      px-10 py-12 shadow-2xl
                    "
                  >
                    
                    <motion.div
                      animate={{ scale: [1, 1.15, 1] }}
                      transition={{ repeat: Infinity, duration: 1.8 }}
                      className="
                        flex h-20 w-20 items-center justify-center
                        rounded-3xl border bg-background
                      "
                    >
                      <Stethoscope className="h-10 w-10 text-red-500" />
                    </motion.div>

                    <h3 className="text-xl font-bold tracking-tight">
                      Analizuję objawy…
                    </h3>

                    <p className="max-w-xs text-center text-sm text-muted-foreground">
                      Łączę symptomy z bazą chorób i modelami predykcyjnymi
                    </p>

                    <div className="w-64 overflow-hidden rounded-full border">
                      <motion.div
                        initial={{ x: "-100%" }}
                        animate={{ x: "100%" }}
                        transition={{
                          repeat: Infinity,
                          duration: 1.2,
                          ease: "linear",
                        }}
                        className="h-2 bg-red-500/70"
                      />
                    </div>
                  </motion.div>
                </motion.div>
              )}
      </AnimatePresence>
    </main>
  );
}

function Snowish(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      viewBox="0 0 24 24"
      width="24"
      height="24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="M12 2v20" />
      <path d="M5 7l14 10" />
      <path d="M19 7L5 17" />
    </svg>
  );
}

function truncate(s: string, n: number) {
  if (s.length <= n) return s;
  return s.slice(0, n - 1) + "…";
}
