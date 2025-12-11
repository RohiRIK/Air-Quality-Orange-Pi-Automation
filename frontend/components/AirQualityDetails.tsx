"use client";

import useSWR from 'swr';
import { fetcher } from '@/lib/api';
import type { SensorData } from '@/types/sensor';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { useTheme } from '@/lib/ThemeContext';
import { Thermometer, Droplets, Wind } from 'lucide-react';

interface AirQualityDetailsProps {
  currentData: SensorData;
  onClose: () => void;
}

// Helper to format timestamp for the chart
const formatTimestamp = (isoString: string) => {
  const date = new Date(isoString);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

function Reasons({ currentData }: { currentData: SensorData }) {
  const { theme } = useTheme();
  const reasons = [];

  if (!currentData.components) {
    return <p>Analysis data is not available.</p>;
  }

  const { gas_score, humidity_score } = currentData.components;

  if (gas_score < 70) {
    reasons.push({
      Icon: Wind,
      color: theme.colors.primary,
      text: `The primary factor is a drop in air purity due to detected pollutants (VOCs).`,
      value: `Gas Score: ${gas_score}/100`
    });
  } else {
     reasons.push({
      Icon: Wind,
      color: theme.colors.primary,
      text: `Air purity from pollutants (VOCs) is currently good.`,
      value: `Gas Score: ${gas_score}/100`
    });
  }

  if (humidity_score < 95) {
    const isHigh = currentData.humidity_rh > 60;
    reasons.push({
      Icon: Droplets,
      color: 'text-cyan-400',
      text: `The humidity (${currentData.humidity_rh}%) is ${isHigh ? 'higher' : 'lower'} than the ideal 40-60% range.`,
      value: `Humidity Score: ${humidity_score}/100`
    });
  }

  return (
    <div className="space-y-4">
      {reasons.map((reason, index) => (
        <div key={index} className="flex items-start gap-4 p-4 rounded-lg" style={{ backgroundColor: theme.colors.panel }}>
          <div className="p-2 rounded-full" style={{ backgroundColor: theme.colors.primary, color: theme.colors.bg }}>
            <reason.Icon className="w-5 h-5" />
          </div>
          <div className="flex-1">
            <p className="font-light" style={{ color: theme.colors.text }}>{reason.text}</p>
            <p className="text-sm font-medium" style={{ color: theme.colors.primary }}>{reason.value}</p>
          </div>
        </div>
      ))}
    </div>
  );
}


export default function AirQualityDetails({ currentData, onClose }: AirQualityDetailsProps) {
  const { theme } = useTheme();
  const { data: history, error } = useSWR<SensorData[]>('/api/history', fetcher, {
    refreshInterval: 5000, // Refresh history every 5 seconds
  });

  if (error) return <div className="text-red-400 p-4">Failed to load historical data.</div>;
  if (!history) return (
    <div className="h-64 flex items-center justify-center">
      <div className="w-8 h-8 border-4 border-slate-500/30 border-t-slate-500 rounded-full animate-spin" />
    </div>
  );

  const chartData = history.map(d => ({
    ...d,
    time: formatTimestamp(d.timestamp),
  }));

  return (
    <div className="w-full mt-6 p-1 flex flex-col gap-6">
      {/* Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
            <XAxis
              dataKey="time"
              stroke={theme.colors.muted}
              fontSize={12}
              tickLine={false}
              axisLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              domain={[0, 100]}
              stroke={theme.colors.muted}
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: theme.colors.panel,
                borderColor: theme.colors.border,
                color: theme.colors.text
              }}
            />
            <Line
              type="monotone"
              dataKey="air_quality_score"
              stroke={theme.colors.primary}
              strokeWidth={2}
              dot={false}
              name="AQI"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Analysis */}
      <div>
        <h3 className="text-lg font-light mb-4" style={{ color: theme.colors.text }}>
          What does this score mean?
        </h3>
        <Reasons currentData={currentData} />
      </div>
    </div>
  );
}
