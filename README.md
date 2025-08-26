# Air Quality Orange Pi Automation

A Docker-based air quality monitoring system using BME680/BMP680 sensor on Orange Pi 3 LTS, outputting structured JSON logs for easy data collection and analysis.

## Features

- 🌡️ **Multi-sensor readings**: Temperature, humidity, pressure, gas resistance, altitude
- 📊 **Real-time JSON logging**: Structured data output every 2 seconds (configurable)
- 🔍 **Air quality analysis**: Baseline establishment and air quality scoring
- 📈 **Smart analytics**: Dew point, heat index, gas trend analysis
- 🐳 **Docker containerized**: Easy deployment and management
- 🔄 **Auto-restart**: Handles sensor errors gracefully
- ⚡ **Unbuffered output**: Real-time log streaming

## Hardware Requirements

- Orange Pi 3 LTS (or compatible SBC)
- BME680 or BMP680 sensor
- I2C connection (typically GPIO pins 3 & 5)

## Quick Start

### 1. Clone and Build
```bash
git clone <your-repo-url>
cd Air-Quality-Orange-Pi-Automation
sudo docker-compose build
```

### 2. Run with Docker Compose
```bash
# Start the container
sudo docker-compose up -d

# View live JSON logs
sudo docker logs -f bmp-sensor-container

# Pretty print JSON
sudo docker logs --tail 10 bmp-sensor-container | jq .
```

### 3. Custom Configuration
```bash
# Set custom reading interval (default: 2 seconds)
sudo docker-compose stop bmp-sensor
sudo docker-compose run -e READ_INTERVAL=1.0 -d bmp-sensor

# Set custom device ID
sudo docker-compose run -e DEVICE_ID=my-sensor-01 -d bmp-sensor
```

## JSON Output Format

### Sensor Readings (every READ_INTERVAL)
```json
{
  "timestamp": "2025-08-26T07:27:17.205478+00:00",
  "device_id": "e37e75c56562",
  "reading_count": 50,
  "uptime_seconds": 81.5,
  "temperature_c": 31.04,
  "pressure_hpa": 1009.22,
  "humidity_rh": 68.55,
  "gas_ohms": 43345.0,
  "altitude_m": 33.6,
  "gas_baseline_ohms": 42150.5,
  "air_quality_score": 52.3,
  "dew_point_c": 24.75,
  "heat_index_c": 34.47,
  "gas_readings_buffer_size": 38,
  "baseline_established": true
}
```

### Summary Reports (every 10 readings)
```json
{
  "timestamp": "2025-08-26T07:27:17.205478+00:00",
  "device_id": "e37e75c56562",
  "type": "SUMMARY",
  "reading_count": 50,
  "avg_temp_last_10": 31.03,
  "avg_humidity_last_10": 68.55,
  "avg_pressure_last_10": 1009.22,
  "current_gas_trend": "changing"
}
```

### Statistical Reports (every 30 readings)
```json
{
  "timestamp": "2025-08-26T07:27:47.318901+00:00",
  "device_id": "e37e75c56562",
  "type": "STATISTICS",
  "gas_stats": {
    "min_ohms": 28450.0,
    "max_ohms": 45120.0,
    "avg_ohms": 38750.5,
    "readings_count": 60
  },
  "sensor_status": "healthy",
  "memory_usage_readings": 60
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `READ_INTERVAL` | `2.0` | Seconds between sensor readings |
| `DEVICE_ID` | hostname | Unique identifier for this sensor |
| `I2C_DEVICE` | `/dev/i2c-0` | I2C device path |
| `BLINKA_FORCEBOARD` | `ORANGE_PI_3_LTS` | Force board detection |

## Air Quality System

The system establishes a dynamic baseline for gas resistance readings:

1. **Warmup Period**: 120 seconds initial sensor warmup
2. **Baseline Collection**: Collects 60 readings for moving average
3. **Air Quality Scoring**: 0-100 scale where 50 is baseline
   - Higher scores = cleaner air (higher gas resistance)
   - Lower scores = more pollutants (lower gas resistance)

## Data Processing Examples

### Stream to File
```bash
sudo docker logs -f bmp-sensor-container > sensor_data.jsonl
```

### Process with jq
```bash
# Get temperature readings only
sudo docker logs bmp-sensor-container | jq -r '.temperature_c // empty'

# Filter only sensor readings (exclude INFO logs)
sudo docker logs bmp-sensor-container | jq 'select(.temperature_c)'

# Get air quality scores
sudo docker logs bmp-sensor-container | jq -r '.air_quality_score // empty'
```

### Import to Database
```bash
# Example: Import to InfluxDB
sudo docker logs bmp-sensor-container | \
jq -r 'select(.temperature_c) | "sensor,device_id=\(.device_id) temperature=\(.temperature_c),humidity=\(.humidity_rh),pressure=\(.pressure_hpa) \((.timestamp | fromdateiso8601) * 1000000000)"'
```

## Project Structure

```
Air-Quality-Orange-Pi-Automation/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Container build instructions
├── bmp_reader.py              # Main sensor reading script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                # Git ignore patterns
└── docs/                     # Additional documentation
```

## Hardware Setup

1. **I2C Connection**: Connect BME680 to Orange Pi I2C pins
   - VCC → 3.3V
   - GND → Ground
   - SDA → GPIO 3 (Pin 3)
   - SCL → GPIO 5 (Pin 5)

2. **Enable I2C**: Ensure I2C is enabled in Orange Pi configuration

3. **Test Connection**: Verify sensor detection
   ```bash
   sudo i2cdetect -y 0
   # Should show device at address 0x77 or 0x76
   ```

## Troubleshooting

### Container Keeps Restarting
```bash
# Check logs for errors
sudo docker logs bmp-sensor-container

# Test sensor connectivity
sudo i2cdetect -y 0

# Run container interactively
sudo docker run --rm -it --privileged -v /dev:/dev rohirikman/air-quality-sensor bash
```

### No JSON Output
```bash
# Verify unbuffered output is enabled
sudo docker exec bmp-sensor-container printenv PYTHONUNBUFFERED

# Check if sensor is connected
sudo docker exec bmp-sensor-container python -c "import board, busio; print('I2C OK')"
```

### Permission Issues
```bash
# Check I2C device permissions
ls -la /dev/i2c*

# Add user to i2c group (if running without Docker)
sudo usermod -a -G i2c $USER
```

## Development

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export BLINKA_FORCEBOARD=ORANGE_PI_3_LTS
export READ_INTERVAL=1.0

# Run locally
python bmp_reader.py
```

### Building Custom Images
```bash
# Build with custom tag
sudo docker build -t my-air-sensor:v1.0 .

# Build for different architectures
sudo docker buildx build --platform linux/arm64 -t my-air-sensor:arm64 .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with your hardware
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Adafruit CircuitPython BME680](https://github.com/adafruit/Adafruit_CircuitPython_BME680)
- Supports Orange Pi via [Adafruit Blinka](https://github.com/adafruit/Adafruit_Blinka)
- Containerized for easy deployment and portability
