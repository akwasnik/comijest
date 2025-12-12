"use client";

import { InfoCard } from "@/app/components/misc/InfoCard";
import { TeamCard } from "@/app/components/misc/TeamCard";
import { TechCard } from "@/app/components/misc/TechCard";
import { motion } from "framer-motion";
import {
  GraduationCap,
  Brain,
  Server,
  Laptop,
  Heart,
  Rocket,
  Users,
} from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0 },
};

export default function AboutPage() {
  return (
    <div className="flex flex-col gap-24 px-6 py-20 max-w-6xl mx-auto">

      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeUp}
        transition={{ duration: 0.6 }}
        className="text-center space-y-6"
      >
        <h1 className="text-4xl md:text-5xl font-bold">
          O projekcie <span className="text-primary">comijest</span>
        </h1>
        <p className="text-muted-foreground max-w-3xl mx-auto text-lg">
          Nowoczesna aplikacja tworzona przez studentów, łącząca
          sztuczną inteligencję, backend i frontend w jednym spójnym systemie.
        </p>
      </motion.section>

      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeUp}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="grid md:grid-cols-2 gap-12 items-center"
      >
        <div className="space-y-6">
          <h2 className="text-3xl font-semibold">Kim jesteśmy?</h2>
          <p className="text-muted-foreground leading-relaxed">
            Jesteśmy studentami, a <strong>ComiJest</strong> to projekt,
            który rozwijamy jako bazę pod naszą przyszłą
            <strong> pracę licencjacką</strong>.
            Tworzymy go z myślą o realnym zastosowaniu,
            wysokiej jakości kodu oraz nowoczesnej architekturze.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-6">
          <InfoCard icon={GraduationCap} title="Studenci" />
          <InfoCard icon={Rocket} title="Projekt licencjacki" />
          <InfoCard icon={Laptop} title="Frontend" />
          <InfoCard icon={Server} title="Backend" />
        </div>
      </motion.section>

      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeUp}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="text-center space-y-8"
      >
        <h2 className="text-3xl font-semibold">
          Ciągły rozwój i eksperymentowanie
        </h2>

        <p className="text-muted-foreground max-w-4xl mx-auto text-lg">
          Aplikacja jest stale rozwijana i służy jako
          <strong> praktyczny przykład połączenia:</strong>
        </p>

        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-8">
          <TechCard icon={Brain} title="Machine Learning" description="Modele AI, klasyfikacja, analiza danych" />
          <TechCard icon={Server} title="Backend" description="API, logika biznesowa, bazy danych" />
          <TechCard icon={Laptop} title="Frontend" description="Next.js, UX, wydajność" />
        </div>
      </motion.section>

      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeUp}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="bg-muted/50 rounded-2xl p-10 text-center space-y-6"
      >
        <Heart className="mx-auto text-primary" size={36} />
        <h2 className="text-3xl font-semibold">Ciekawostka</h2>
        <p className="text-muted-foreground max-w-3xl mx-auto text-lg">
          Uwielbiamy <strong>Uniwersytet Gdański</strong> – świetna atmosfera,
          wysoki poziom merytoryczny i fantastyczna współpraca sprawiają,
          że rozwijanie tego projektu to czysta przyjemność.
        </p>
      </motion.section>

      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeUp}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="space-y-12"
      >
        <h2 className="text-3xl font-semibold text-center">
          Zespół projektu
        </h2>

        <div className="grid md:grid-cols-3 gap-8">
          <TeamCard
            name="Maksymilian Janica"
            role="Backend"
            description="Architektura serwera, API, logika biznesowa"
          />
          <TeamCard
            name="Adrian Kwaśnik"
            role="Frontend/DevOps"
            description="Deployment, UI, Next.js"
          />
          <TeamCard
            name="Arkadiusz Lorek"
            role="AI"
            description="Modele ML, eksperymenty, analiza danych"
          />
        </div>

        <p className="text-center text-muted-foreground text-lg">
          <Users className="inline mr-2" />
          Świetnie się uzupełniamy i bardzo dobrze ze sobą współpracujemy
        </p>
      </motion.section>
    </div>
  );
}
