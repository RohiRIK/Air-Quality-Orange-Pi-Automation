# Orange Pi 3 LTS GPIO Pinout Diagram

Below is a simplified pinout for the Orange Pi 3 LTS 40-pin header. Use this as a reference for connecting sensors and peripherals.

```
  1  3.3V   |  2  5V
  3  SDA.1  |  4  5V
  5  SCL.1  |  6  GND
  7  GPIO   |  8  TXD
  9  GND    | 10  RXD
 11  GPIO   | 12  GPIO
 13  GPIO   | 14  GND
 15  GPIO   | 16  GPIO
 17  3.3V   | 18  GPIO
 19  MOSI   | 20  GND
 21  MISO   | 22  GPIO
 23  SCLK   | 24  CE0
 25  GND    | 26  CE1
 27  SDA.2  | 28  SCL.2
 29  GPIO   | 30  GND
 31  GPIO   | 32  GPIO
 33  GPIO   | 34  GND
 35  GPIO   | 36  GPIO
 37  GPIO   | 38  GPIO
 39  GND    | 40  GPIO
```

## BMP688 Sensor Wiring Example
- **VCC** → Pin 1 (3.3V)
- **GND** → Pin 6 (GND)
- **SDA** → Pin 3 (SDA.1)
- **SCL** → Pin 5 (SCL.1)

> For more details, refer to the official Orange Pi documentation.
