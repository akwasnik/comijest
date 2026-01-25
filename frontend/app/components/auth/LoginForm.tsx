"use client";

import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { motion } from "framer-motion";
import { useMutation } from "@tanstack/react-query";
import { redirect, useRouter } from "next/navigation";

interface LoginPayload {
  email: string;
  password: string;
}

export default function LoginForm() {
  const router = useRouter();
  
  const loginMutation = useMutation({
    mutationFn: async (payload: LoginPayload) => {
      const res = await fetch("http://backend:5000/api/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error?.message || "Błąd logowania");
      }
      const response = await res.json()
      console.log(response);
      return response;
    },
    onSuccess: () => {
      router.push("/profile")
    },
  });

  

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-sm bg-white dark:bg-neutral-900 p-8 rounded-2xl shadow-lg border border-red-300"
    >
      <h1 className="text-2xl font-bold mb-6 text-center text-red-500">
        Zaloguj się
      </h1>

      <Formik
        initialValues={{ email: "", password: "" }}
        validationSchema={Yup.object({
          email: Yup.string()
            .email("Niepoprawny email")
            .required("Wymagane"),
          password: Yup.string()
                      .min(12, "Hasło musi mieć min. 12 znaków")
                      .test(
                        "has-uppercase",
                        "Hasło musi zawierać wielką literę",
                        (value) => !!value && [...value].some((c) => c >= "A" && c <= "Z")
                      )
                      .test(
                        "has-lowercase",
                        "Hasło musi zawierać małą literę",
                        (value) => !!value && [...value].some((c) => c >= "a" && c <= "z")
                      )
                      .test(
                        "has-digit",
                        "Hasło musi zawierać cyfrę",
                        (value) => !!value && [...value].some((c) => c >= "0" && c <= "9")
                      )
                      .test(
                        "has-special",
                        "Hasło musi zawierać znak specjalny",
                        (value) =>
                          !!value &&
                          [...value].some(
                            (c) => !/[a-zA-Z0-9]/.test(c)
                          )
                      )
                      .required("Wymagane"),
        })}
        onSubmit={(values, { setSubmitting }) => {
          loginMutation.mutate(values, {
            onSettled: () => {
              setSubmitting(false);
              if(loginMutation.isSuccess) redirect("/")
            },
          });
        }}
      >
        {({ isSubmitting }) => (
          <Form className="space-y-4">

            {/* Email */}
            <div>
              <Field
                name="email"
                type="email"
                placeholder="Adres e-mail"
                className="w-full p-3 rounded-xl border dark:border-neutral-700 border-gray-300 bg-white dark:bg-neutral-800 outline-none focus:ring-2 focus:ring-red-500"
              />
              <ErrorMessage
                name="email"
                component="div"
                className="text-red-600 text-sm mt-1"
              />
            </div>

            {/* Password */}
            <div>
              <Field
                name="password"
                type="password"
                placeholder="Hasło"
                className="w-full p-3 rounded-xl border dark:border-neutral-700 border-gray-300 bg-white dark:bg-neutral-800 outline-none focus:ring-2 focus:ring-red-500"
              />
              <ErrorMessage
                name="password"
                component="div"
                className="text-red-600 text-sm mt-1"
              />
            </div>

            {/* Backend error */}
            {loginMutation.isError && (
              <p className="text-sm text-red-600 text-center">
                {(loginMutation.error as Error).message}
              </p>
            )}

            {/* Submit */}
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              type="submit"
              disabled={isSubmitting || loginMutation.isPending}
              className="w-full p-3 bg-red-500 text-white rounded-xl font-semibold shadow-md hover:bg-red-600 transition disabled:opacity-60"
            >
              {loginMutation.isPending ? "Loguję..." : "Zaloguj"}
            </motion.button>
          </Form>
        )}
      </Formik>

      <p className="text-center mt-6 text-sm text-gray-700 dark:text-neutral-400">
        Nie masz konta?{" "}
        <a
          href="/register"
          className="text-red-500 font-semibold hover:text-red-700 transition"
        >
          Zarejestruj się
        </a>
      </p>
    </motion.div>
  );
}
