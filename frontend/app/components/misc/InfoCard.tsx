import { LucideIcon } from "lucide-react";

interface InfoCardProps {
  icon: LucideIcon;
  title: string;
}

export function InfoCard({ icon: Icon, title }: InfoCardProps) {
  return (
    <div className="flex items-center gap-4 p-5 border rounded-xl">
      <Icon className="text-primary" />
      <span className="font-medium">{title}</span>
    </div>
  );
}
