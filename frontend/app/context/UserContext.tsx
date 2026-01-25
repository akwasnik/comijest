"use client";

import {
  createContext,
  useContext,
  ReactNode,
} from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

export type User = {
  username: string;
  email: string;
};

type UserContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  logout: () => void;
  refetchUser: () => void;
};

const UserContext = createContext<UserContextType | null>(null);

export function UserProvider({ children }: { children: ReactNode }) {
  const router = useRouter();

  const {
    data,
    isLoading,
    refetch,
  } = useQuery<User | null>({
    queryKey: ["currentUser"],
    queryFn: async () => {
      const res = await fetch(
        "https://backend:5000/api/users/me",
        {
          credentials: "include",
        }
      );

      if (res.status === 401) {
        return null;
      }

      if (!res.ok) {
        throw new Error("Failed to fetch user");
      }

      return res.json();
    },
    retry: false,
  });

  const logoutMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(
        "https://backend:5000/api/users/logout",
        {
          method: "POST",
          credentials: "include",
        }
      );

      if (!res.ok) {
        throw new Error("Logout failed");
      }
    },
    onSuccess: async () => {
      await refetch();
      router.push("/login");
    },
  });

  const value: UserContextType = {
    user: data ?? null,
    isAuthenticated: !!data,
    isLoading,
    logout: () => logoutMutation.mutate(),
    refetchUser: () => refetch(),
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const ctx = useContext(UserContext);
  if (!ctx) {
    throw new Error("useUser must be used inside UserProvider");
  }
  return ctx;
}
