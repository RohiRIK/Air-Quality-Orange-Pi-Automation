"use client";

import { useEffect, useState } from 'react';

export default function LiveClock() {
  const [time, setTime] = useState<Date | null>(null);

  useEffect(() => {
    setTime(new Date());
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  if (!time) return <div className="h-8 w-32 bg-slate-800/50 rounded animate-pulse" />;

  return (
    <div className="text-right">
      <div className="text-3xl font-light text-slate-100 tabular-nums">
        {time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
      <div className="text-sm text-slate-400 font-medium uppercase tracking-widest">
        {time.toLocaleDateString([], { weekday: 'long', month: 'short', day: 'numeric' })}
      </div>
    </div>
  );
}
