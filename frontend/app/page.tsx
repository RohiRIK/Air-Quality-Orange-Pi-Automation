'use client';
import { useState, useEffect } from 'react';

interface SensorData {
  timestamp: string;
  device_id: string;
  reading_count: number;
  uptime_seconds: number;
  temperature: number;
  pressure: number;
  humidity: number;
  gas_ohms: number;
  altitude_m: number;
  gas_baseline_ohms?: number;
  air_quality_score?: number;
  dew_point_c?: number;
  heat_index_c?: number;
  gas_readings_buffer_size?: number;
  baseline_established?: boolean;
}

interface Recommendation {
  recommendation_text: string;
}

export default function Home() {
  const [sensorData, setSensorData] = useState<SensorData | null>(null);
  // const [recommendation, setRecommendation] = useState<Recommendation | null>(null); // Commented out
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        // Fetch sensor data (assuming backend exposes /api/data)
        const sensorResponse = await fetch('http://localhost:8999/api/data');
        if (!sensorResponse.ok) {
          throw new Error(`HTTP error! status: ${sensorResponse.status}`);
        }
        const sensorJson = await sensorResponse.json();
        setSensorData(sensorJson);

        // AI recommendation fetching removed for now due to quota issues
        // setRecommendation({ recommendation_text: "AI recommendation temporarily unavailable due to quota limits." }); // Placeholder
        
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError('An unknown error occurred');
        }
        console.error("Error fetching data:", error);
      }
    }

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  // Modified conditional rendering: only check for sensorData
  if (!sensorData) {
    return <div className="p-4">Loading sensor data...</div>;
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-3xl">
        <h1 className="text-4xl font-bold mb-8 text-center text-gray-800">Air Quality Monitor</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex flex-col gap-4 p-4 border border-gray-200 rounded-lg">
            <h2 className="text-2xl font-semibold text-gray-700">Sensor Data</h2>
            <p className="text-lg text-gray-600">Timestamp: <span className="font-medium">{new Date(sensorData.timestamp).toLocaleString()}</span></p>
            <p className="text-lg text-gray-600">Device ID: <span className="font-medium">{sensorData.device_id}</span></p>
            <p className="text-lg text-gray-600">Reading Count: <span className="font-medium">{sensorData.reading_count}</span></p>
            <p className="text-lg text-gray-600">Uptime: <span className="font-medium">{sensorData.uptime_seconds} s</span></p>
            <p className="text-lg text-gray-600">Temperature: <span className="font-medium">{sensorData.temperature}°C</span></p>
            <p className="text-lg text-gray-600">Pressure: <span className="font-medium">{sensorData.pressure} hPa</span></p>
            <p className="text-lg text-gray-600">Humidity: <span className="font-medium">{sensorData.humidity}%</span></p>
            <p className="text-lg text-gray-600">Gas Ohms: <span className="font-medium">{sensorData.gas_ohms}</span></p>
            <p className="text-lg text-gray-600">Altitude: <span className="font-medium">{sensorData.altitude_m} m</span></p>
            {sensorData.gas_baseline_ohms !== undefined && <p className="text-lg text-gray-600">Gas Baseline Ohms: <span className="font-medium">{sensorData.gas_baseline_ohms}</span></p>}
            {sensorData.air_quality_score !== undefined && <p className="text-lg text-gray-600">Air Quality Score: <span className="font-medium">{sensorData.air_quality_score}</span></p>}
            {sensorData.dew_point_c !== undefined && <p className="text-lg text-gray-600">Dew Point: <span className="font-medium">{sensorData.dew_point_c}°C</span></p>}
            {sensorData.heat_index_c !== undefined && <p className="text-lg text-gray-600">Heat Index: <span className="font-medium">{sensorData.heat_index_c}°C</span></p>}
            {sensorData.gas_readings_buffer_size !== undefined && <p className="text-lg text-gray-600">Gas Readings Buffer Size: <span className="font-medium">{sensorData.gas_readings_buffer_size}</span></p>}
            {sensorData.baseline_established !== undefined && <p className="text-lg text-gray-600">Baseline Established: <span className="font-medium">{sensorData.baseline_established ? 'Yes' : 'No'}</span></p>}
          </div>

          {/* AI Recommendation section - conditionally rendered */}
          {/* For now, AI recommendation is disabled due to quota limits */}
          {false && (
            <div className="flex flex-col gap-4 p-4 border border-gray-200 rounded-lg">
              <h2 className="text-2xl font-semibold text-gray-700">AI Recommendation</h2>
              <p className="text-lg text-gray-600">AI recommendation temporarily unavailable due to quota limits.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}