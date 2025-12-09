"use client";

import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { clsx } from 'clsx';

interface Props {
  score: number;
  status: string;
}

const getColor = (score: number) => {
  if (score >= 90) return '#34d399'; // Emerald-400
  if (score >= 75) return '#4ade80'; // Green-400
  if (score >= 60) return '#facc15'; // Yellow-400
  if (score >= 40) return '#fb923c'; // Orange-400
  return '#ef4444'; // Red-500
};

export default function AirQualityGauge({ score, status }: Props) {
  const color = getColor(score);
  
  return (
    <div className="glass-panel p-8 flex flex-col items-center justify-center relative w-full h-full min-h-[350px]">
      <div className="absolute top-6 left-6">
        <h2 className="text-slate-400 text-sm font-medium uppercase tracking-wider">Air Quality Index</h2>
      </div>
      
      <div className="w-64 h-64 relative">
        {/* Glow effect behind the gauge */}
        <div 
          className="absolute inset-0 rounded-full blur-3xl opacity-20 transition-colors duration-1000"
          style={{ backgroundColor: color }}
        />
        
        <CircularProgressbar
          value={score}
          text={`${Math.round(score)}%`}
          styles={buildStyles({
            pathColor: color,
            textColor: '#f8fafc',
            trailColor: 'rgba(255,255,255,0.05)',
            textSize: '18px',
            pathTransitionDuration: 1.5,
          })}
          strokeWidth={6}
        />
        
        {/* Status Text Centered Below Number (Visual Hack: Use absolute positioning over the component if needed, but text prop handles number) */}
      </div>

      <div className="mt-8 text-center">
        <h1 className={clsx(
          "text-4xl font-light tracking-tight transition-colors duration-500",
        )} style={{ color }}>
          {status}
        </h1>
        <p className="text-slate-500 mt-2 text-sm font-light">
          Real-time analysis based on VOCs & Humidity
        </p>
      </div>
    </div>
  );
}
