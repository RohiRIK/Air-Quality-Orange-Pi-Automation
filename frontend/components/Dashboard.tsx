"use client";

import { useState } from 'react';
import useSWR from 'swr';
import { fetcher, API_URL } from '@/lib/api';
import { SensorData } from '@/types/sensor';
import AirQualityGauge from './AirQualityGauge';
import MetricCard from './MetricCard';
import LiveClock from './LiveClock';
import HistoryModal from './HistoryModal';
import { Thermometer, Droplets, Gauge, Activity } from 'lucide-react';

export default function Dashboard() {
  // State for Modal
  const [selectedMetric, setSelectedMetric] = useState<{key: keyof SensorData, label: string, color: string} | null>(null);

  // Poll live data every 2 seconds
  const { data: sensor, error, isLoading } = useSWR<SensorData>(`${API_URL}/data`, fetcher, {
    refreshInterval: 2000,
  });

  // Fetch history only when needed (or pre-fetch if you want instant open)
  // We'll pre-fetch lazily or just fetch always (it's small JSON)
  const { data: history } = useSWR<SensorData[]>(`${API_URL}/history`, fetcher, {
    refreshInterval: 5000, // Update history every 5s
  });

  if (error) return (
    <div className="flex items-center justify-center min-h-screen text-red-400">
      Failed to load sensor data. Is the backend running?
    </div>
  );

  if (isLoading || !sensor) return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-12 h-12 border-4 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto p-6 lg:p-10 space-y-6">
      {/* Header */}
      <header className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-2xl font-light tracking-wide text-slate-100">
            Environment <span className="font-bold text-emerald-400">Monitor</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">System Status: <span className="text-emerald-400">Online</span> • ID: {sensor.device_id}</p>
        </div>
        <LiveClock />
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* Left Col: Hero Gauge (Span 8) */}
        <div 
          onClick={() => setSelectedMetric({ key: 'air_quality_score', label: 'Air Quality Score', color: 'text-emerald-400' })}
          className="md:col-span-8 lg:col-span-8 h-[400px] cursor-pointer hover:scale-[1.01] transition-transform duration-300"
        >
          <AirQualityGauge 
            score={sensor.air_quality_score || 0} 
            status={sensor.air_quality_status || "Initializing..."} 
          />
        </div>

        {/* Right Col: Metrics (Span 4) */}
        <div className="md:col-span-4 space-y-6">
          <MetricCard 
            label="Temperature" 
            value={sensor.temperature_c} 
            unit="°C" 
            icon={Thermometer} 
            color="text-amber-400"
            onClick={() => setSelectedMetric({ key: 'temperature_c', label: 'Temperature', color: 'text-amber-400' })}
          />
          <MetricCard 
            label="Humidity" 
            value={sensor.humidity_rh} 
            unit="%" 
            icon={Droplets} 
            color="text-cyan-400"
            onClick={() => setSelectedMetric({ key: 'humidity_rh', label: 'Humidity', color: 'text-cyan-400' })}
          />
          <MetricCard 
            label="Pressure" 
            value={sensor.pressure_hpa} 
            unit="hPa" 
            icon={Gauge} 
            color="text-purple-400"
            onClick={() => setSelectedMetric({ key: 'pressure_hpa', label: 'Pressure', color: 'text-purple-400' })}
          />
        </div>

        {/* Bottom Row: Insights / Explanation (Span 12) */}
        <div className="md:col-span-12">
          <div className="glass-panel p-6 flex flex-col md:flex-row items-start md:items-center gap-6">
            <div className="bg-slate-800/50 p-3 rounded-full">
              <Activity className="w-6 h-6 text-emerald-400" />
            </div>
            <div className="flex-1">
              <h3 className="text-slate-300 font-medium mb-1">System Analysis</h3>
              <p className="text-slate-400 font-light leading-relaxed">
                {sensor.explanation || "Analyzing environmental patterns..."}
              </p>
            </div>
            <div className="hidden md:block text-right text-xs text-slate-500">
              <p>Baseline: {sensor.gas_baseline_ohms} Ω</p>
              <p>Uptime: {Math.round(sensor.uptime_seconds / 60)}m</p>
            </div>
          </div>
        </div>
      </div>

      {/* History Modal */}
      <HistoryModal 
        isOpen={!!selectedMetric}
        onClose={() => setSelectedMetric(null)}
        metricKey={selectedMetric?.key || null}
        metricLabel={selectedMetric?.label || ''}
        color={selectedMetric?.color || ''}
        data={history || []}
      />
    </div>
  );
}
