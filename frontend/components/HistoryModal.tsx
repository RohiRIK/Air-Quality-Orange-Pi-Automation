"use client";

import { X } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { SensorData } from '@/types/sensor';
import { useEffect, useState } from 'react';

interface HistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  metricKey: keyof SensorData | null;
  metricLabel: string;
  data: SensorData[];
  color: string;
}

export default function HistoryModal({ isOpen, onClose, metricKey, metricLabel, data, color }: HistoryModalProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (isOpen) setMounted(true);
    // Escape key listener
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;
  if (!metricKey) return null;

  // Format data for chart
  const chartData = data.map(d => ({
    time: new Date(d.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
    value: d[metricKey] as number,
  }));

  // Extract color hex from Tailwind class or default
  const getHexColor = (colorClass: string) => {
    if (colorClass.includes('emerald')) return '#34d399';
    if (colorClass.includes('amber')) return '#fbbf24';
    if (colorClass.includes('cyan')) return '#22d3ee';
    if (colorClass.includes('purple')) return '#c084fc';
    return '#38bdf8'; // Default sky blue
  };

  const hexColor = getHexColor(color);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900/90 border border-slate-700/50 rounded-2xl w-full max-w-4xl p-6 shadow-2xl relative animate-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-xl font-light text-slate-100">
              Historical Analysis: <span style={{ color: hexColor }} className="font-semibold">{metricLabel}</span>
            </h2>
            <p className="text-slate-500 text-sm mt-1">Past 1 hour of sensor readings</p>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Chart */}
        <div className="h-[400px] w-full bg-slate-800/20 rounded-xl p-4 border border-slate-700/30">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={hexColor} stopOpacity={0.3}/>
                  <stop offset="95%" stopColor={hexColor} stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis 
                dataKey="time" 
                stroke="#64748b" 
                fontSize={12} 
                tickMargin={10} 
                minTickGap={30}
              />
              <YAxis 
                stroke="#64748b" 
                fontSize={12} 
                domain={['auto', 'auto']}
                tickFormatter={(val) => Math.round(val).toString()}
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                itemStyle={{ color: hexColor }}
                labelStyle={{ color: '#94a3b8', marginBottom: '4px' }}
              />
              <Area 
                type="monotone" 
                dataKey="value" 
                stroke={hexColor} 
                strokeWidth={2}
                fillOpacity={1} 
                fill="url(#colorValue)" 
                animationDuration={1000}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Footer */}
        <div className="mt-6 flex justify-end">
           <span className="text-xs text-slate-600 font-mono">Live Data Stream • Interval: 2s</span>
        </div>
      </div>
    </div>
  );
}
