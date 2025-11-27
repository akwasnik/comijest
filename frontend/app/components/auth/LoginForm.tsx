"use client";

import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { motion } from "framer-motion";

export default function LoginForm() {
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
          email: Yup.string().email("Niepoprawny email").required("Wymagane"),
          password: Yup.string().min(6, "Minimum 6 znaków").required("Wymagane"),
        })}
        onSubmit={(values) => {
          console.log("Wysyłam:", values);
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
                className="w-full p-3 rounded-xl border dark:border-neutral-700 border-gray-300 bg-white dark:bg-neutral-800 outline-none focus:ring-2 focus:ring-red-500 transition"
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
                className="w-full p-3 rounded-xl border dark:border-neutral-700 border-gray-300 bg-white dark:bg-neutral-800 outline-none focus:ring-2 focus:ring-red-500 transition"
              />
              <ErrorMessage
                name="password"
                component="div"
                className="text-red-600 text-sm mt-1"
              />
            </div>

            {/* Submit */}
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              transition={{ type: "spring", stiffness: 200 }}
              type="submit"
              disabled={isSubmitting}
              className="w-full p-3 bg-red-500 text-white rounded-xl font-semibold shadow-md hover:bg-red-600 transition"
            >
              Zaloguj
            </motion.button>
          </Form>
        )}
      </Formik>

      {/* Link do rejestracji */}
      <p className="text-center mt-6 text-sm text-gray-700 dark:text-neutral-400">
        Nie masz konta?{" "}
        <a href="/register" className="text-red-500 font-semibold hover:text-red-700 transition">
          Zarejestruj się
        </a>
      </p>
    </motion.div>
  );
}
