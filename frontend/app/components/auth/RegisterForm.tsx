"use client";

import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { motion } from "framer-motion";
import { useMutation } from "@tanstack/react-query";
import { redirect, useRouter } from "next/navigation";

interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

export default function RegisterForm() {
  const router = useRouter()
  const registerMutation = useMutation({
    mutationFn: async (payload: RegisterPayload) => {
      const res = await fetch("https://backend:5000/api/users/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errormsg = await res.json()
        throw new Error(errormsg.message);
      }

      return res.json();
    },
    onSuccess: () => router.push("/login")
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-sm bg-white dark:bg-neutral-900 p-8 rounded-2xl shadow-lg border border-red-300"
    >
      <h1 className="text-2xl font-bold mb-6 text-center text-red-500">
        Utwórz konto
      </h1>

      <Formik
        initialValues={{
          username: "",
          email: "",
          password: "",
          confirm: "",
        }}
        validationSchema={Yup.object({
          username: Yup.string()
            .min(3, "Min. 3 znaki")
            .required("Wymagane"),

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

          confirm: Yup.string()
            .oneOf([Yup.ref("password")], "Hasła się nie zgadzają")
            .required("Wymagane"),
        })}
        onSubmit={(values, { setSubmitting }) => {
          registerMutation.mutate(
            {
              username: values.username,
              email: values.email,
              password: values.password,
            },
            {
              onSettled: () => setSubmitting(false),
            }
          );
          
        }}
      >
        {({ isSubmitting }) => (
          <Form className="space-y-4">

            {/* Username */}
            <div>
              <Field
                name="username"
                placeholder="Nazwa użytkownika"
                className="w-full p-3 rounded-xl border dark:border-neutral-700 bg-white dark:bg-neutral-800 border-gray-300 outline-none focus:ring-2 focus:ring-red-500"
              />
              <ErrorMessage name="username" component="div" className="text-red-600 text-sm mt-1" />
            </div>

            {/* Email */}
            <div>
              <Field
                name="email"
                type="email"
                placeholder="Adres e-mail"
                className="w-full p-3 rounded-xl border dark:border-neutral-700 bg-white dark:bg-neutral-800 border-gray-300 outline-none focus:ring-2 focus:ring-red-500"
              />
              <ErrorMessage name="email" component="div" className="text-red-600 text-sm mt-1" />
            </div>

            {/* Password */}
            <div>
              <Field
                name="password"
                type="password"
                placeholder="Hasło"
                className="w-full p-3 rounded-xl border dark:border-neutral-700 bg-white dark:bg-neutral-800 border-gray-300 outline-none focus:ring-2 focus:ring-red-500"
              />
              <ErrorMessage name="password" component="div" className="text-red-600 text-sm mt-1" />
            </div>

            {/* Confirm */}
            <div>
              <Field
                name="confirm"
                type="password"
                placeholder="Powtórz hasło"
                className="w-full p-3 rounded-xl border dark:border-neutral-700 bg-white dark:bg-neutral-800 border-gray-300 outline-none focus:ring-2 focus:ring-red-500"
              />
              <ErrorMessage name="confirm" component="div" className="text-red-600 text-sm mt-1" />
            </div>

            {/* Submit */}
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              type="submit"
              disabled={isSubmitting || registerMutation.isPending}
              className="w-full p-3 bg-red-500 text-white rounded-xl font-semibold shadow-md hover:bg-red-600 transition disabled:opacity-60"
            >
              {registerMutation.isPending ? "Rejestruję..." : "Zarejestruj"}
            </motion.button>
             {registerMutation.isError && (
              <p className="text-sm text-red-600 text-center">
                {(registerMutation.error).message}
              </p>
             )}
             
          </Form>
        )}
      </Formik>

      <p className="text-center mt-6 text-sm text-gray-700 dark:text-neutral-400">
        Masz konto?{" "}
        <a href="/login" className="text-red-500 font-semibold hover:text-red-700">
          Zaloguj się
        </a>
      </p>
    </motion.div>
  );
}
