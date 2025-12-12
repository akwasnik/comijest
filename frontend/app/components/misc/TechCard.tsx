import { LucideIcon } from "lucide-react";

interface TechCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function TechCard({ icon: Icon, title, description }: TechCardProps) {
  return (
    <div className="p-6 border rounded-xl space-y-4 flex flex-col items-center">
      <Icon className="text-primary" />
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}
