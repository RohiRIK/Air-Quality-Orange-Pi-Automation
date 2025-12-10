"use client";

import { X, Check } from 'lucide-react';
import { useTheme } from '@/lib/ThemeContext';
import { themes } from '@/lib/themes';
import { useEffect, useState } from 'react';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function SettingsModal({ isOpen, onClose }: SettingsModalProps) {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (isOpen) setMounted(true);
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="glass-panel w-full max-w-2xl p-6 relative animate-in zoom-in-95 duration-200 flex flex-col max-h-[90vh]"
        style={{ backgroundColor: theme.colors.bg, borderColor: theme.colors.border }}
      >
        
        {/* Header */}
        <div className="flex justify-between items-center mb-6 border-b pb-4" style={{ borderColor: theme.colors.border }}>
          <div>
            <h2 className="text-xl font-light" style={{ color: theme.colors.text }}>
              Appearance Settings
            </h2>
            <p className="text-sm mt-1" style={{ color: theme.colors.muted }}>
              Customize your dashboard theme
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

        {/* Theme Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 overflow-y-auto p-1 custom-scrollbar">
          {themes.map((t) => (
            <button
              key={t.id}
              onClick={() => setTheme(t.id)}
              className={`
                group relative flex flex-col items-center gap-3 p-4 rounded-xl border transition-all duration-300
                ${theme.id === t.id ? 'ring-2 ring-offset-2 ring-offset-black/50' : 'hover:scale-[1.02]'}
              `}
              style={{
                backgroundColor: t.colors.bg,
                borderColor: theme.id === t.id ? t.colors.primary : t.colors.border,
                ringColor: t.colors.primary,
              }}
            >
              {/* Preview Circles */}
              <div className="flex gap-2 mb-2">
                <div className="w-6 h-6 rounded-full shadow-lg" style={{ backgroundColor: t.colors.primary }} />
                <div className="w-6 h-6 rounded-full shadow-lg" style={{ backgroundColor: t.colors.secondary }} />
                <div className="w-6 h-6 rounded-full shadow-lg border border-white/10" style={{ backgroundColor: t.colors.bg }} />
              </div>
              
              <span className="text-sm font-medium" style={{ color: t.colors.text }}>
                {t.name}
              </span>

              {/* Active Indicator */}
              {theme.id === t.id && (
                <div className="absolute top-3 right-3 p-1 rounded-full" style={{ backgroundColor: t.colors.primary, color: t.colors.bg }}>
                  <Check className="w-3 h-3" />
                </div>
              )}
            </button>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-6 pt-4 border-t flex justify-between items-center" style={{ borderColor: theme.colors.border }}>
          <a
            href={`${process.env.NEXT_PUBLIC_API_URL || '/api'}/auth/google`}
            className="text-sm hover:underline"
            style={{ color: theme.colors.muted }}
          >
            Connect Google Calendar
          </a>

          <button
            onClick={onClose}
            className="px-6 py-2 rounded-lg font-medium transition-colors hover:brightness-110"
            style={{ backgroundColor: theme.colors.primary, color: theme.colors.bg }}
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
