import { LucideIcon } from 'lucide-react';
import { clsx } from 'clsx';

interface Props {
  label: string;
  value: number;
  unit: string;
  icon: LucideIcon;
  color: string;
  onClick?: () => void;
}

export default function MetricCard({ label, value, unit, icon: Icon, color, onClick }: Props) {
  return (
    <div 
      onClick={onClick}
      className={clsx(
        "glass-panel p-6 flex items-center justify-between transition-all duration-300",
        onClick && "cursor-pointer hover:scale-[1.02] hover:bg-slate-800/60 active:scale-95"
      )}
    >
      <div>
        <p className="text-slate-400 text-sm font-medium uppercase tracking-wider">{label}</p>
        <div className="flex items-baseline gap-1 mt-1">
          <span className="text-2xl font-light text-slate-100">{value}</span>
          <span className="text-slate-500 text-sm">{unit}</span>
        </div>
      </div>
      <div className={clsx("p-3 rounded-xl bg-opacity-10", color.replace('text-', 'bg-'))}>
        <Icon className={clsx("w-6 h-6", color)} />
      </div>
    </div>
  );
}
