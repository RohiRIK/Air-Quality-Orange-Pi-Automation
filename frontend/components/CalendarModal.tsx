"use client";

import { X, ChevronLeft, ChevronRight, Calendar as CalendarIcon, Clock } from 'lucide-react';
import { useTheme } from '@/lib/ThemeContext';
import { useEffect, useState } from 'react';
import useSWR from 'swr';
import { fetcher, API_URL } from '@/lib/api';

interface CalendarModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface CalendarEvent {
  id: string;
  title: string;
  date: string; // YYYY-MM-DD
  time: string;
  type: 'meeting' | 'personal' | 'reminder';
}

export default function CalendarModal({ isOpen, onClose }: CalendarModalProps) {
  const { theme } = useTheme();
  const [viewDate, setViewDate] = useState(new Date()); // The month we are looking at
  const [selectedDate, setSelectedDate] = useState(new Date()); // The specific day clicked

  // Fetch events
  const { data: events } = useSWR<CalendarEvent[]>(isOpen ? `${API_URL}/calendar` : null, fetcher);

  // Reset to today when opening
  useEffect(() => {
    if (isOpen) {
      const now = new Date();
      setViewDate(now);
      setSelectedDate(now);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const year = viewDate.getFullYear();
  const month = viewDate.getMonth();

  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const daysInMonth = lastDay.getDate();
  const startingDayIndex = firstDay.getDay();

  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  const prevMonth = () => setViewDate(new Date(year, month - 1, 1));
  const nextMonth = () => setViewDate(new Date(year, month + 1, 1));

  // Filter events for selected date
  const selectedEvents = (events || []).filter(evt => {
    // Basic date comparison (assuming API returns YYYY-MM-DD local time)
    // To handle timezones robustly, we'd need a library like date-fns, 
    // but this suffices for a local dash.
    const evtDate = new Date(evt.date); 
    return evtDate.getDate() === selectedDate.getDate() &&
           evtDate.getMonth() === selectedDate.getMonth() &&
           evtDate.getFullYear() === selectedDate.getFullYear();
  });

  const days = [];
  // Empty slots
  for (let i = 0; i < startingDayIndex; i++) {
    days.push(<div key={`empty-${i}`} className="p-2" />);
  }
  
  // Render Days
  for (let d = 1; d <= daysInMonth; d++) {
    const currentDate = new Date(year, month, d);
    const isToday = currentDate.toDateString() === new Date().toDateString();
    const isSelected = currentDate.toDateString() === selectedDate.toDateString();
    
    // Check if day has events
    const hasEvents = (events || []).some(evt => {
        const evtDate = new Date(evt.date);
        return evtDate.getDate() === d && 
               evtDate.getMonth() === month && 
               evtDate.getFullYear() === year;
    });

    days.push(
      <button 
        key={d} 
        onClick={() => setSelectedDate(currentDate)}
        className={`
          aspect-square flex items-center justify-center rounded-xl text-sm transition-all relative
          ${isSelected ? 'shadow-lg scale-105 font-bold' : 'hover:bg-white/5'}
          ${!isSelected && isToday ? 'ring-2 ring-inset' : ''}
        `}
        style={{ 
          backgroundColor: isSelected ? theme.colors.primary : 'transparent',
          color: isSelected ? theme.colors.bg : theme.colors.text,
          borderColor: isToday ? theme.colors.primary : 'transparent' 
        }}
      >
        {d}
        {/* Dot for today if not selected */}
        {!isSelected && isToday && (
          <div className="absolute bottom-1 w-1 h-1 rounded-full" style={{ backgroundColor: theme.colors.primary }} />
        )}
        {/* Small dot for events */}
        {!isSelected && !isToday && hasEvents && (
          <div className="absolute bottom-1 w-1 h-1 rounded-full bg-white/50" />
        )}
      </button>
    );
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="glass-panel w-full max-w-lg p-6 relative animate-in zoom-in-95 duration-200 flex flex-col md:flex-row gap-6"
        style={{ backgroundColor: theme.colors.bg, borderColor: theme.colors.border }}
      >
        {/* Calendar Side */}
        <div className="flex-1">
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
        </div>

        {/* Events Side Panel (Divider on desktop, top border on mobile) */}
        <div className="md:w-64 border-t md:border-t-0 md:border-l pt-6 md:pt-0 md:pl-6 flex flex-col" style={{ borderColor: theme.colors.border }}>
            <h3 className="text-sm font-medium uppercase tracking-wider mb-4" style={{ color: theme.colors.muted }}>
                {selectedDate.toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' })}
            </h3>

            <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar max-h-[300px]">
                {selectedEvents.length > 0 ? (
                    selectedEvents.map(evt => (
                        <div 
                            key={evt.id} 
                            className="p-3 rounded-xl border transition-colors hover:brightness-110"
                            style={{ 
                                backgroundColor: `${theme.colors.bg}`, 
                                borderColor: theme.colors.border 
                            }}
                        >
                            <div className="flex items-center gap-2 mb-1" style={{ color: theme.colors.primary }}>
                                <Clock className="w-3 h-3" />
                                <span className="text-xs font-medium">{evt.time}</span>
                            </div>
                            <p className="text-sm font-medium" style={{ color: theme.colors.text }}>{evt.title}</p>
                        </div>
                    ))
                ) : (
                    <div className="flex flex-col items-center justify-center h-32 text-center space-y-2 opacity-50">
                        <CalendarIcon className="w-8 h-8" style={{ color: theme.colors.muted }} />
                        <p className="text-xs" style={{ color: theme.colors.muted }}>No events scheduled</p>
                    </div>
                )}
            </div>
            
            <div className="mt-4 pt-4 border-t text-xs text-center" style={{ borderColor: theme.colors.border, color: theme.colors.muted }}>
                Synced with Google Calendar
            </div>
        </div>
      </div>
    </div>
  );
}
