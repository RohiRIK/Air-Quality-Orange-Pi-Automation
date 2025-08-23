# Hardware Setup

## Hardware Setup
1. **Identify Pins**:
   - On the Orange Pi 3 LTS, GPIO pin numbering starts at Pin 1 (top-left, marked by a triangle), which is 3.3V.
   - Connect BMP688:
     - VCC → Pin 1 (3.3V)
     - GND → Pin 6 (GND)
     - SDA → Pin 3 (SDA.1)
     - SCL → Pin 5 (SCL.1)
2. **Power On**: Use a 5V power supply for the Orange Pi.
3. **Verify**: Run `sudo i2cdetect -y 0` to detect the sensor (address: 0x76 or 0x77).

Refer to `docs/pinout_diagram.md` for visual guides.