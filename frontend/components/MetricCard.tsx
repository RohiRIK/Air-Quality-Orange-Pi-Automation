import { LucideIcon } from 'lucide-react';

interface Props {
  label: string;
  value: string | number;
  unit: string;
  icon: LucideIcon;
  trend?: 'up' | 'down' | 'flat';
  color?: string;
}

export default function MetricCard({ label, value, unit, icon: Icon, color = "text-blue-400" }: Props) {
  return (
    <div className="glass-card p-6 flex flex-col justify-between h-32 relative overflow-hidden group">
      <div className="flex justify-between items-start z-10">
        <span className="text-slate-400 text-sm font-medium">{label}</span>
        <Icon className={`w-5 h-5 ${color} opacity-80`} />
      </div>
      
      <div className="z-10 mt-auto">
        <span className="text-3xl font-light text-slate-100">{value}</span>
        <span className="text-slate-500 text-sm ml-1">{unit}</span>
      </div>

      {/* Decorative background element */}
      <div className={`absolute -bottom-4 -right-4 w-24 h-24 ${color} rounded-full blur-3xl opacity-5 group-hover:opacity-10 transition-opacity duration-500`} />
    </div>
  );
}
