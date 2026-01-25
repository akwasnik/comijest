"use client";

import EditProfileModal from "@/app/components/misc/EditProfileModal";
import { useUser } from "@/app/context/UserContext";
import { motion } from "framer-motion";
import { useLayoutEffect, useState } from "react";

function ProfileContent() {

  const { user, isLoading, refetchUser } = useUser();

  const [open, setOpen] = useState(false);


  useLayoutEffect(() => {
    refetchUser()
  },[])

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <span className="text-muted-foreground animate-pulse">
          Ładowanie profilu…
        </span>
      </div>
    );
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="
        mx-auto mt-24 max-w-xl mb-24
        rounded-2xl border
        bg-background/80
        p-8 shadow-xl backdrop-blur
      "
    >
      <h1 className="mb-6 text-center text-3xl font-bold">
        Twój profil
      </h1>

      {user && (<div className="space-y-4">
        <ProfileRow label="Username" value={user.username} />
        <ProfileRow label="Email" value={user.email} />
        <ProfileRow label="Hasło" value="••••••••••" />
      </div>)}

      <button
        onClick={() => setOpen(true)}
        className="
          w-full rounded-xl border
          px-4 py-2 font-semibold
          hover:bg-muted transition
        "
      >
        Edytuj dane
      </button>

      <EditProfileModal
        isOpen={open}
        onClose={() => setOpen(false)}
      />

    </motion.section>
  );
}

function ProfileRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between rounded-xl border p-4">
      <span className="text-muted-foreground">{label}</span>
      <span className="font-medium">{value}</span>
    </div>
  );
}

export default function ProfilePage() {
  return (
      <ProfileContent />
  );
}
