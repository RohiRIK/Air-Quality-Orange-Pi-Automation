"use client";

import { X, ChevronLeft, ChevronRight } from 'lucide-react';
import { useTheme } from '@/lib/ThemeContext';
import { useEffect, useState } from 'react';

interface CalendarModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function CalendarModal({ isOpen, onClose }: CalendarModalProps) {
  const { theme } = useTheme();
  const [date, setDate] = useState(new Date());

  // Reset to today when opening
  useEffect(() => {
    if (isOpen) setDate(new Date());
  }, [isOpen]);

  if (!isOpen) return null;

  const year = date.getFullYear();
  const month = date.getMonth(); // 0-indexed

  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const daysInMonth = lastDay.getDate();
  const startingDayIndex = firstDay.getDay(); // 0 = Sunday

  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  const prevMonth = () => setDate(new Date(year, month - 1, 1));
  const nextMonth = () => setDate(new Date(year, month + 1, 1));

  const days = [];
  // Empty slots for previous month
  for (let i = 0; i < startingDayIndex; i++) {
    days.push(<div key={`empty-${i}`} className="p-2" />);
  }
  // Days of current month
  for (let d = 1; d <= daysInMonth; d++) {
    const isToday = d === new Date().getDate() && month === new Date().getMonth() && year === new Date().getFullYear();
    days.push(
      <div 
        key={d} 
        className={`
          aspect-square flex items-center justify-center rounded-xl text-sm transition-all
          ${isToday ? 'font-bold shadow-lg scale-110' : 'hover:bg-white/5 cursor-pointer'}
        `}
        style={{ 
          backgroundColor: isToday ? theme.colors.primary : 'transparent',
          color: isToday ? theme.colors.bg : theme.colors.text 
        }}
      >
        {d}
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="glass-panel w-full max-w-md p-6 relative animate-in zoom-in-95 duration-200"
        style={{ backgroundColor: theme.colors.bg, borderColor: theme.colors.border }}
      >
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-light tracking-wider" style={{ color: theme.colors.text }}>Calendar</h2>
          <button onClick={onClose} style={{ color: theme.colors.muted }} className="hover:text-white">
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Controls */}
        <div className="flex justify-between items-center mb-6 px-2">
          <button onClick={prevMonth} className="p-2 hover:bg-white/5 rounded-lg transition-colors" style={{ color: theme.colors.text }}>
            <ChevronLeft className="w-5 h-5" />
          </button>
          <span className="text-lg font-medium" style={{ color: theme.colors.primary }}>
            {monthNames[month]} {year}
          </span>
          <button onClick={nextMonth} className="p-2 hover:bg-white/5 rounded-lg transition-colors" style={{ color: theme.colors.text }}>
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>

        {/* Grid Header */}
        <div className="grid grid-cols-7 mb-2 text-center text-xs font-semibold tracking-widest uppercase" style={{ color: theme.colors.muted }}>
          {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map(day => (
            <div key={day} className="py-1">{day}</div>
          ))}
        </div>

        {/* Grid Days */}
        <div className="grid grid-cols-7 gap-1">
          {days}
        </div>

        <div className="mt-6 text-center text-xs" style={{ color: theme.colors.muted }}>
          * Historical data log is currently limited to 1 hour.
        </div>
      </div>
    </div>
  );
}
