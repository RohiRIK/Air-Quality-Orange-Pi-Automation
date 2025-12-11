"use client";

import { X } from 'lucide-react';
import { useTheme } from '@/lib/ThemeContext';
import { useEffect } from 'react';
import AirQualityDetails from './AirQualityDetails';
import type { SensorData } from '@/types/sensor';

interface AqiDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentData: SensorData | null;
}

export default function AqiDetailsModal({ isOpen, onClose, currentData }: AqiDetailsModalProps) {
  const { theme } = useTheme();

  useEffect(() => {
    if (!isOpen) return;
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen || !currentData) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div
        className="glass-panel w-full max-w-3xl p-6 relative animate-in zoom-in-95 duration-200 flex flex-col max-h-[90vh]"
        style={{ backgroundColor: theme.colors.bg, borderColor: theme.colors.border }}
      >

        {/* Header */}
        <div className="flex justify-between items-center mb-4 border-b pb-4" style={{ borderColor: theme.colors.border }}>
          <div>
            <h2 className="text-xl font-light" style={{ color: theme.colors.text }}>
              Air Quality Index (AQI) Analysis
            </h2>
            <p className="text-sm mt-1" style={{ color: theme.colors.muted }}>
              Historical trend and breakdown of the current score.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-full transition-colors hover:bg-white/10"
            style={{ color: theme.colors.muted }}
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="overflow-y-auto custom-scrollbar pr-2">
            <AirQualityDetails currentData={currentData} onClose={onClose} />
        </div>
      </div>
    </div>
  );
}
