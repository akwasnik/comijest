import LoginForm from "@/app/components/auth/LoginForm";
import QueryProvider from "@/app/providers/QueryProvider";

export default function LoginPage() {
  return (
    <QueryProvider>
      <div className="p-20 flex items-center justify-center bg-white dark:bg-neutral-950">
        <LoginForm />
      </div>
    </QueryProvider>
  );
}
