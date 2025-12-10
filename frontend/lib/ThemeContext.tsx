"use client";

import React, { createContext, useContext, useEffect, useState } from 'react';
import { Theme, themes } from '@/lib/themes';

interface ThemeContextType {
  theme: Theme;
  setTheme: (id: string) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(themes[0]);

  useEffect(() => {
    const saved = localStorage.getItem('aqi-theme');
    if (saved) {
      const found = themes.find(t => t.id === saved);
      if (found) setThemeState(found);
    }
  }, []);

  const setTheme = (id: string) => {
    const found = themes.find(t => t.id === id);
    if (found) {
      setThemeState(found);
      localStorage.setItem('aqi-theme', id);
    }
  };

  // Apply CSS variables for dynamic styling
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty('--color-primary', theme.colors.primary);
    root.style.setProperty('--color-secondary', theme.colors.secondary);
    root.style.setProperty('--color-bg', theme.colors.bg);
    root.style.setProperty('--color-panel', theme.colors.panel);
    root.style.setProperty('--color-text', theme.colors.text);
    root.style.setProperty('--color-muted', theme.colors.muted);
    root.style.setProperty('--color-border', theme.colors.border);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
