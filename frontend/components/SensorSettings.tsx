"use client";

import { useState } from 'react';
import useSWR, { mutate } from 'swr';
import { fetcher, API_URL } from '@/lib/api';
import { useTheme } from '@/lib/ThemeContext';
import { Edit2, Save, X, Server, Wifi, WifiOff } from 'lucide-react';

interface SensorInfo {
  device_id: string;
  name: string | null;
  last_seen: string;
  is_active: number;
}

export default function SensorSettings() {
  const { theme } = useTheme();
  const { data: sensors } = useSWR<SensorInfo[]>(`${API_URL}/sensors`, fetcher);
  
  const [editingId, setEditingId] = useState<string | null>(null);
  const [newName, setNewName] = useState("");

  const handleEdit = (sensor: SensorInfo) => {
    setEditingId(sensor.device_id);
    setNewName(sensor.name || sensor.device_id);
  };

  const handleSave = async (deviceId: string) => {
    try {
      await fetch(`${API_URL}/sensors/${deviceId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newName }),
      });
      // Refresh the list
      mutate(`${API_URL}/sensors`);
      setEditingId(null);
    } catch (error) {
      console.error("Failed to rename sensor", error);
    }
  };

  const isOnline = (lastSeen: string) => {
      // Simple check: online if seen in last 15 mins
      // Note: Timezone handling might be tricky, checking diff
      const diff = new Date().getTime() - new Date(lastSeen).getTime();
      return diff < 15 * 60 * 1000; 
  };

  if (!sensors) return <div className="text-center p-4">Loading sensors...</div>;

  return (
    <div className="space-y-4">
      {sensors.map((sensor) => {
        const online = isOnline(sensor.last_seen);
        const isEditing = editingId === sensor.device_id;

        return (
          <div 
            key={sensor.device_id}
            className="flex items-center justify-between p-4 rounded-xl border transition-all"
            style={{ 
              backgroundColor: `${theme.colors.bg}40`,
              borderColor: theme.colors.border
            }}
          >
            <div className="flex items-center gap-4 flex-1">
              <div className={`p-2 rounded-full ${online ? 'bg-green-500/10' : 'bg-red-500/10'}`}>
                {online ? (
                    <Wifi className="w-5 h-5 text-green-500" />
                ) : (
                    <WifiOff className="w-5 h-5 text-red-500" />
                )}
              </div>
              
              <div className="flex-1">
                {isEditing ? (
                  <input 
                    type="text"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    className="w-full bg-black/20 border rounded px-2 py-1 outline-none focus:border-primary"
                    style={{ borderColor: theme.colors.primary, color: theme.colors.text }}
                    autoFocus
                  />
                ) : (
                  <>
                    <h3 className="font-medium" style={{ color: theme.colors.text }}>
                        {sensor.name || sensor.device_id}
                    </h3>
                    <p className="text-xs font-mono" style={{ color: theme.colors.muted }}>
                        ID: {sensor.device_id}
                    </p>
                  </>
                )}
              </div>
            </div>

            <div className="flex gap-2 ml-4">
              {isEditing ? (
                <>
                  <button 
                    onClick={() => handleSave(sensor.device_id)}
                    className="p-2 hover:bg-green-500/20 text-green-500 rounded-lg transition-colors"
                  >
                    <Save className="w-4 h-4" />
                  </button>
                  <button 
                    onClick={() => setEditingId(null)}
                    className="p-2 hover:bg-red-500/20 text-red-500 rounded-lg transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </>
              ) : (
                <button 
                    onClick={() => handleEdit(sensor)}
                    className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                    style={{ color: theme.colors.muted }}
                >
                  <Edit2 className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>
        );
      })}
      
      {sensors.length === 0 && (
          <div className="text-center py-8" style={{ color: theme.colors.muted }}>
              <Server className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>No sensors discovered yet.</p>
              <p className="text-xs mt-1">Power on your ESP32 nodes to start.</p>
          </div>
      )}
    </div>
  );
}
