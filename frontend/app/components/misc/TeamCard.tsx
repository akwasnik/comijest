interface TeamCardProps {
  name: string;
  role: string;
  description: string;
}

export function TeamCard({ name, role, description }: TeamCardProps) {
  return (
    <div className="p-8 border rounded-2xl text-center space-y-4">
      <h3 className="text-xl font-semibold">{name}</h3>
      <span className="text-primary font-medium">{role}</span>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}
