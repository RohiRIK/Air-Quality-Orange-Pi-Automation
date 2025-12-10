export interface Theme {
  id: string;
  name: string;
  colors: {
    primary: string;    // Main accent (e.g., text-emerald-400)
    secondary: string;  // Secondary accent
    bg: string;        // Main background (e.g., bg-slate-900)
    panel: string;     // Glass panel bg (e.g., bg-slate-800/50)
    text: string;      // Main text color
    muted: string;     // Muted text color
    border: string;    // Border color
  };
}

export const themes: Theme[] = [
  {
    id: 'default',
    name: 'Emerald AI',
    colors: {
      primary: '#34d399', // emerald-400
      secondary: '#06b6d4', // cyan-500
      bg: '#0f172a',      // slate-900
      panel: 'rgba(30, 41, 59, 0.5)', // slate-800/50
      text: '#f1f5f9',    // slate-100
      muted: '#94a3b8',   // slate-400
      border: 'rgba(51, 65, 85, 0.5)', // slate-700/50
    }
  },
  {
    id: 'ocean',
    name: 'Deep Ocean',
    colors: {
      primary: '#38bdf8', // sky-400
      secondary: '#818cf8', // indigo-400
      bg: '#0c0a1f',      // deep blue
      panel: 'rgba(17, 24, 39, 0.6)', 
      text: '#e0f2fe',
      muted: '#94a3b8',
      border: 'rgba(30, 58, 138, 0.3)',
    }
  },
  {
    id: 'cyberpunk',
    name: 'Night City',
    colors: {
      primary: '#e879f9', // fuchsia-400
      secondary: '#22d3ee', // cyan-400
      bg: '#09090b',      // zinc-950
      panel: 'rgba(24, 24, 27, 0.7)',
      text: '#fafafa',
      muted: '#a1a1aa',
      border: 'rgba(232, 121, 249, 0.2)',
    }
  },
  {
    id: 'sunset',
    name: 'Solar Flare',
    colors: {
      primary: '#fb923c', // orange-400
      secondary: '#f472b6', // pink-400
      bg: '#1c1917',      // stone-900
      panel: 'rgba(41, 37, 36, 0.6)',
      text: '#fafaf9',
      muted: '#a8a29e',
      border: 'rgba(251, 146, 60, 0.2)',
    }
  },
  {
    id: 'forest',
    name: 'Deep Forest',
    colors: {
      primary: '#4ade80', // green-400
      secondary: '#a3e635', // lime-400
      bg: '#052e16',      // green-950
      panel: 'rgba(20, 83, 45, 0.4)',
      text: '#f0fdf4',
      muted: '#86efac',
      border: 'rgba(74, 222, 128, 0.2)',
    }
  },
  {
    id: 'dracula',
    name: 'Vampire',
    colors: {
      primary: '#c084fc', // purple-400
      secondary: '#f87171', // red-400
      bg: '#1e1b2e',      // dark purple
      panel: 'rgba(45, 42, 66, 0.6)',
      text: '#f3e8ff',
      muted: '#d8b4fe',
      border: 'rgba(192, 132, 252, 0.2)',
    }
  },
  {
    id: 'monochrome',
    name: 'Obsidian',
    colors: {
      primary: '#ffffff',
      secondary: '#94a3b8',
      bg: '#000000',
      panel: 'rgba(255, 255, 255, 0.1)',
      text: '#ffffff',
      muted: '#a3a3a3',
      border: 'rgba(255, 255, 255, 0.2)',
    }
  },
  {
    id: 'royal',
    name: 'Royal Gold',
    colors: {
      primary: '#facc15', // yellow-400
      secondary: '#60a5fa', // blue-400
      bg: '#172554',      // blue-950
      panel: 'rgba(30, 58, 138, 0.5)',
      text: '#fefce8',
      muted: '#93c5fd',
      border: 'rgba(250, 204, 21, 0.2)',
    }
  },
  {
    id: 'berry',
    name: 'Wild Berry',
    colors: {
      primary: '#fb7185', // rose-400
      secondary: '#c084fc', // purple-400
      bg: '#4c0519',      // rose-950
      panel: 'rgba(136, 19, 55, 0.4)',
      text: '#fff1f2',
      muted: '#fda4af',
      border: 'rgba(251, 113, 133, 0.2)',
    }
  },
  {
    id: 'glacier',
    name: 'Glacier',
    colors: {
      primary: '#22d3ee', // cyan-400
      secondary: '#cbd5e1', // slate-300
      bg: '#0f172a',      // slate-900 (reused but bluer accents)
      panel: 'rgba(56, 189, 248, 0.15)',
      text: '#f0f9ff',
      muted: '#bae6fd',
      border: 'rgba(34, 211, 238, 0.3)',
    }
  }
];
