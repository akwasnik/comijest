"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useMutation } from "@tanstack/react-query";
import { X } from "lucide-react";
import { useUser } from "@/app/context/UserContext";

/* =======================
   TYPES
======================= */

type Props = {
  isOpen: boolean;
  onClose: () => void;
};

type UpdateUserPayload = {
  username: string;
  email: string;
  password?: string;
};

/* =======================
   VALIDATION
======================= */

const passwordSchema = Yup.string()
  .min(12, "Hasło musi mieć min. 12 znaków")
  .test(
    "has-uppercase",
    "Hasło musi zawierać wielką literę",
    (value) => !!value && /[A-Z]/.test(value)
  )
  .test(
    "has-lowercase",
    "Hasło musi zawierać małą literę",
    (value) => !!value && /[a-z]/.test(value)
  )
  .test(
    "has-digit",
    "Hasło musi zawierać cyfrę",
    (value) => !!value && /[0-9]/.test(value)
  )
  .test(
    "has-special",
    "Hasło musi zawierać znak specjalny",
    (value) => !!value && /[^a-zA-Z0-9]/.test(value)
  );

const validationSchema = Yup.object({
  username: Yup.string()
    .min(3, "Min. 3 znaki")
    .required("Username jest wymagany"),

  email: Yup.string()
    .email("Niepoprawny email")
    .required("Email jest wymagany"),

  password: Yup.string()
    .notRequired()
    .test(
      "password-strength",
      "Hasło musi mieć min. 12 znaków, wielką i małą literę, cyfrę oraz znak specjalny",
      (value) => {
        if (!value || value.length === 0) {
          return true; // 👈 puste = OK
        }

        const hasUppercase = /[A-Z]/.test(value);
        const hasLowercase = /[a-z]/.test(value);
        const hasDigit = /[0-9]/.test(value);
        const hasSpecial = /[^a-zA-Z0-9]/.test(value);
        const hasMinLength = value.length >= 12;

        return (
          hasUppercase &&
          hasLowercase &&
          hasDigit &&
          hasSpecial &&
          hasMinLength
        );
      }
    ),

  confirm: Yup.string().when("password", {
    is: (val: string) => !!val && val.length > 0,
    then: (schema) =>
      schema
        .required("Potwierdzenie hasła jest wymagane")
        .oneOf([Yup.ref("password")], "Hasła muszą być takie same"),
    otherwise: (schema) => schema.notRequired(),
  }),
});


export default function EditProfileModal({ isOpen, onClose }: Props) {
  const { user, refetchUser } = useUser();

  const updateMutation = useMutation({
    mutationFn: async (values: UpdateUserPayload) => {
      const res = await fetch(
        "http://backend:5000/api/users/me",
        {
          method: "PUT",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        }
      );

      if (!res.ok) {
        const data = await res.json();
        throw new Error(
          data.error || data.msg || "Błąd aktualizacji"
        );
      }

      return res.json();
    },
    onSuccess: async () => {
      await refetchUser();
      onClose();
    },
  });

  if (!user) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* OVERLAY */}
          <motion.div
            className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* MODAL */}
          <motion.div
            className="
              fixed z-50 top-1/2 left-1/2
              w-full max-w-lg
              -translate-x-1/2 -translate-y-1/2
              rounded-2xl border
              bg-background p-6 shadow-xl
            "
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ ease: 'easeOut', duration: 0.2 }}
          >
            {/* HEADER */}
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-bold">
                Edytuj dane profilu
              </h2>
              <button onClick={onClose}>
                <X className="hover:text-red-500" />
              </button>
            </div>

            <Formik
              initialValues={{
                username: user.username,
                email: user.email,
                password: "",
                confirm: "",
              }}
              validationSchema={validationSchema}
              onSubmit={(values, { setSubmitting }) => {
                const payload: UpdateUserPayload = {
                  username: values.username,
                  email: values.email,
                  ...(values.password
                    ? { password: values.password }
                    : {}),
                };

                updateMutation.mutate(payload);
                setSubmitting(false);
              }}
            >
              {({ isSubmitting, values }) => (
                <Form className="space-y-4">
                  <FieldBlock
                    name="username"
                    placeholder="Nazwa użytkownika"
                  />

                  <FieldBlock
                    name="email"
                    type="email"
                    placeholder="Adres e-mail"
                  />

                  <FieldBlock
                    name="password"
                    type="password"
                    placeholder="Nowe hasło"
                  />

                  {values.password && (
                    <FieldBlock
                      name="confirm"
                      type="password"
                      placeholder="Powtórz hasło"
                    />
                  )}

                  <motion.button
                    whileHover={{ scale: 1.03 }}
                    whileTap={{ scale: 0.97 }}
                    type="submit"
                    disabled={
                      isSubmitting || updateMutation.isPending
                    }
                    className="
                      w-full p-3 bg-red-500 text-white
                      rounded-xl font-semibold
                      hover:bg-red-600 transition
                      disabled:opacity-60
                    "
                  >
                    {updateMutation.isPending
                      ? "Zapisuję..."
                      : "Zapisz zmiany"}
                  </motion.button>

                  {updateMutation.isError && (
                    <p className="text-sm text-red-600 text-center">
                      {updateMutation.error.message}
                    </p>
                  )}
                </Form>
              )}
            </Formik>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

/* =======================
   FIELD COMPONENT
======================= */

function FieldBlock({
  name,
  type = "text",
  placeholder,
}: {
  name: string;
  type?: string;
  placeholder: string;
}) {
  return (
    <div>
      <Field
        name={name}
        type={type}
        placeholder={placeholder}
        className="
          w-full p-3 rounded-xl border
          bg-white dark:bg-neutral-800
          border-gray-300 dark:border-neutral-700
          outline-none focus:ring-2 focus:ring-red-500
        "
      />
      <ErrorMessage
        name={name}
        component="div"
        className="text-red-600 text-sm mt-1"
      />
    </div>
  );
}
