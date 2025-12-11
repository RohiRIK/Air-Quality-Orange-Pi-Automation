"use client";

import { X, Database, Clipboard } from 'lucide-react';
import { useTheme } from '@/lib/ThemeContext';
import { SensorData } from '@/types/sensor';
import { useEffect, useState } from 'react';

interface RawDataModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: SensorData | undefined;
}

export default function RawDataModal({ isOpen, onClose, data }: RawDataModalProps) {
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (isOpen) setMounted(true);
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen || !data) return null;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
  };

  // Helper to flatten nested objects for display
  const flattenData = (obj: any, prefix = ''): { key: string, value: any }[] => {
    return Object.keys(obj).reduce((acc: any[], key) => {
      const value = obj[key];
      const newKey = prefix ? `${prefix}.${key}` : key;
      
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        return [...acc, ...flattenData(value, newKey)];
      }
      return [...acc, { key: newKey, value: value?.toString() }];
    }, []);
  };

  const tableData = flattenData(data);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="glass-panel w-full max-w-2xl p-6 relative animate-in zoom-in-95 duration-200 flex flex-col max-h-[85vh]"
        style={{ backgroundColor: theme.colors.bg, borderColor: theme.colors.border }}
      >
        
        {/* Header */}
        <div className="flex justify-between items-center mb-6 pb-4 border-b" style={{ borderColor: theme.colors.border }}>
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-slate-800">
                <Database className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h2 className="text-xl font-light" style={{ color: theme.colors.text }}>
                Raw Sensor Data
              </h2>
              <p className="text-xs font-mono mt-1" style={{ color: theme.colors.muted }}>
                ID: {data.device_id} • {new Date(data.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <button 
                onClick={copyToClipboard}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors"
                title="Copy JSON"
                style={{ color: theme.colors.muted }}
            >
                <Clipboard className="w-5 h-5" />
            </button>
            <button 
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors"
                style={{ color: theme.colors.muted }}
            >
                <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Table Content */}
        <div className="overflow-y-auto custom-scrollbar flex-1 -mx-2 px-2">
            <table className="w-full text-left text-sm border-collapse">
                <thead>
                    <tr className="border-b" style={{ borderColor: theme.colors.border }}>
                        <th className="py-3 px-2 font-medium uppercase tracking-wider text-xs" style={{ color: theme.colors.muted }}>Metric Key</th>
                        <th className="py-3 px-2 font-medium uppercase tracking-wider text-xs" style={{ color: theme.colors.muted }}>Current Value</th>
                    </tr>
                </thead>
                <tbody>
                    {tableData.map((row, idx) => (
                        <tr 
                            key={row.key} 
                            className="border-b last:border-0 hover:bg-white/5 transition-colors"
                            style={{ borderColor: theme.colors.border }}
                        >
                            <td className="py-3 px-2 font-mono text-xs" style={{ color: theme.colors.primary }}>
                                {row.key}
                            </td>
                            <td className="py-3 px-2 font-mono text-xs break-all" style={{ color: theme.colors.text }}>
                                {row.value}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
      </div>
    </div>
  );
}
