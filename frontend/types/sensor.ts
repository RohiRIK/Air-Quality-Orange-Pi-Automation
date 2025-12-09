export interface SensorData {
  timestamp: string;
  device_id: string;
  reading_count: number;
  uptime_seconds: number;
  temperature_c: number;
  pressure_hpa: number;
  humidity_rh: number;
  gas_ohms: number;
  altitude_m: number;
  gas_baseline_ohms: number;
  air_quality_score: number;
  air_quality_status: string;
  components?: {
    gas_score: number;
    humidity_score: number;
  };
  dew_point_c?: number;
  heat_index_c?: number;
  baseline_established?: boolean;
  explanation?: string; // From n8n if available
}

export interface ApiResponse {
  data: SensorData;
  status: string;
}
