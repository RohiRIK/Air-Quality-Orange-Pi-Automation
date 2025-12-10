"use client";

import { useState } from 'react';
import useSWR from 'swr';
import { fetcher, API_URL } from '@/lib/api';
import { SensorData } from '@/types/sensor';
import AirQualityGauge from './AirQualityGauge';
import MetricCard from './MetricCard';
import LiveClock from './LiveClock';
import HistoryModal from './HistoryModal';
import SettingsModal from './SettingsModal';
import CalendarModal from './CalendarModal';
import { Thermometer, Droplets, Gauge, Activity, Settings, Palette } from 'lucide-react';
import { useTheme } from '@/lib/ThemeContext';

export default function Dashboard() {
  const { theme } = useTheme();
  
  // State for Modals
  const [selectedMetric, setSelectedMetric] = useState<{key: keyof SensorData, label: string, color: string} | null>(null);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);

  // Poll live data every 2 seconds
  const { data: sensor, error, isLoading } = useSWR<SensorData>(`${API_URL}/data`, fetcher, {
    refreshInterval: 2000,
  });

  const { data: history } = useSWR<SensorData[]>(`${API_URL}/history`, fetcher, {
    refreshInterval: 5000,
  });

  if (error) return (
    <div className="flex items-center justify-center min-h-screen text-red-400">
      Failed to load sensor data. Is the backend running?
    </div>
  );

  if (isLoading || !sensor) return (
    <div className="flex items-center justify-center min-h-screen">
      <div 
        className="w-12 h-12 border-4 rounded-full animate-spin" 
        style={{ borderColor: `${theme.colors.primary}33`, borderTopColor: theme.colors.primary }}
      />
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto p-6 lg:p-10 space-y-6">
      {/* Header */}
      <header className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-2xl font-light tracking-wide" style={{ color: theme.colors.text }}>
            Environment <span className="font-bold" style={{ color: theme.colors.primary }}>Monitor</span>
          </h1>
          <p className="text-sm mt-1" style={{ color: theme.colors.muted }}>
            System Status: <span style={{ color: theme.colors.primary }}>Online</span> • ID: {sensor.device_id}
          </p>
        </div>
        
        <div className="flex items-center gap-4">
           {/* Calendar Trigger */}
          <button 
            onClick={() => setIsCalendarOpen(true)}
            className="hover:scale-105 transition-transform"
          >
            <LiveClock />
          </button>

          {/* Settings Trigger */}
          <button 
            onClick={() => setIsSettingsOpen(true)}
            className="p-3 rounded-xl glass-panel hover:brightness-125 transition-all group"
          >
            <Settings className="w-5 h-5 group-hover:rotate-90 transition-transform duration-500" style={{ color: theme.colors.muted }} />
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* Left Col: Hero Gauge (Span 8) */}
        <div 
          onClick={() => setSelectedMetric({ key: 'air_quality_score', label: 'Air Quality Score', color: theme.colors.primary })}
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
            color={theme.colors.secondary} // Use theme secondary color
            onClick={() => setSelectedMetric({ key: 'temperature_c', label: 'Temperature', color: theme.colors.secondary })}
          />
          <MetricCard 
            label="Humidity" 
            value={sensor.humidity_rh} 
            unit="%" 
            icon={Droplets} 
            color={theme.colors.primary} // Use theme primary
            onClick={() => setSelectedMetric({ key: 'humidity_rh', label: 'Humidity', color: theme.colors.primary })}
          />
          <MetricCard 
            label="Pressure" 
            value={sensor.pressure_hpa} 
            unit="hPa" 
            icon={Gauge} 
            color="#c084fc" // Keep specific color for pressure or use theme accent
            onClick={() => setSelectedMetric({ key: 'pressure_hpa', label: 'Pressure', color: '#c084fc' })}
          />
        </div>

        {/* Bottom Row: Insights / Explanation (Span 12) */}
        <div className="md:col-span-12">
          <div className="glass-panel p-6 flex flex-col md:flex-row items-start md:items-center gap-6">
            <div className="p-3 rounded-full" style={{ backgroundColor: `${theme.colors.bg}80` }}>
              <Activity className="w-6 h-6" style={{ color: theme.colors.primary }} />
            </div>
            <div className="flex-1">
              <h3 className="font-medium mb-1" style={{ color: theme.colors.text }}>System Analysis</h3>
              <p className="font-light leading-relaxed" style={{ color: theme.colors.muted }}>
                {sensor.explanation || "Analyzing environmental patterns..."}
              </p>
            </div>
            <div className="hidden md:block text-right text-xs" style={{ color: theme.colors.muted }}>
              <p>Baseline: {sensor.gas_baseline_ohms} Ω</p>
              <p>Uptime: {Math.round(sensor.uptime_seconds / 60)}m</p>
            </div>
          </div>
        </div>
      </div>

      {/* Modals */}
      <HistoryModal 
        isOpen={!!selectedMetric}
        onClose={() => setSelectedMetric(null)}
        metricKey={selectedMetric?.key || null}
        metricLabel={selectedMetric?.label || ''}
        color={selectedMetric?.color || ''}
        data={history || []}
      />

      <SettingsModal 
        isOpen={isSettingsOpen} 
        onClose={() => setIsSettingsOpen(false)} 
      />

      <CalendarModal 
        isOpen={isCalendarOpen} 
        onClose={() => setIsCalendarOpen(false)} 
      />
    </div>
  );
}
