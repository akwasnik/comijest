import RegisterForm from "@/app/components/auth/RegisterForm";
import QueryProvider from "@/app/providers/QueryProvider";

export default function RegisterPage() {
  return (
    <QueryProvider>
      <div className="p-20 flex items-center justify-center bg-white dark:bg-neutral-950">
        <RegisterForm />
      </div>
    </QueryProvider>
  );
}
