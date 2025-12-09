# 7. Sensor Calibration and Air Quality Baseline

This document provides guidance on initial sensor calibration and explains the dynamic air quality baseline feature implemented in `bmp_reader.py`.

## BME688 Sensor Warm-up and Calibration

The BME688 gas sensor requires a warm-up period to stabilize its readings. During this time, the sensor heats up to a specific temperature to achieve accurate gas resistance measurements.

**Initial Warm-up:**
When you first power on the Orange Pi and start the `bmp_reader.py` script, the BME688 will undergo a warm-up phase. During this time, the gas resistance readings might fluctuate significantly. The script is configured with a `BASELINE_WARMUP_PERIOD` (default: 300 seconds or 5 minutes) to allow the sensor to stabilize before establishing the initial air quality baseline.

**Calibration for Specific Environments:**
While the BME688 provides relative gas resistance measurements, for precise air quality (e.g., specific VOC concentrations), you might need to calibrate it against known gas concentrations or reference instruments in your specific environment. This project uses a relative approach, focusing on changes from a dynamic baseline.

**Best Practices for Consistent Readings:**
*   **Stable Environment:** Ensure the sensor is in a stable environment, away from direct airflow, strong odors, or sudden temperature changes, especially during the initial warm-up and baseline establishment.
*   **Avoid Contaminants:** Do not expose the sensor to high concentrations of gases or solvents that could permanently affect its sensitivity.

## Dynamic Air Quality Baseline

To provide a more meaningful interpretation of the gas sensor's readings, this project implements a dynamic air quality baseline. Instead of using a fixed reference value, the baseline adapts to the ambient conditions over time.

### How it Works:

1.  **Rolling Average:** The `bmp_reader.py` script maintains a `collections.deque` (a double-ended queue) that stores the most recent gas resistance readings.
2.  **`GAS_READINGS_WINDOW_SIZE`:** This parameter (default: 60 readings) defines how many past readings are kept to calculate the moving average. With a 5-second sleep interval, a window size of 60 means the baseline is calculated over the last 5 minutes of readings.
3.  **`BASELINE_WARMUP_PERIOD`:** An initial period (default: 300 seconds) is observed during which the sensor collects data without establishing a baseline. This allows the sensor to warm up and the `deque` to fill with stable readings.
4.  **Dynamic Baseline Calculation:** Once the warmup period is over and enough readings are collected, the average of the `gas_readings` deque becomes the dynamic `gas_baseline_ohms`.
5.  **Air Quality Score:** An `air_quality_score` is calculated based on the current gas resistance reading relative to the dynamic baseline. The formula used aims to provide a score between 0 and 100, where:
    *   **50:** Represents the current baseline (typical ambient air quality).
    *   **Greater than 50:** Indicates air quality that is better than the recent baseline (higher gas resistance).
    *   **Less than 50:** Indicates air quality that is worse than the recent baseline (lower gas resistance, suggesting more pollutants).

    *Note: The BME688 measures Total Volatile Organic Compounds (TVOCs). Generally, a higher gas resistance implies fewer reducing gases (cleaner air), while a lower gas resistance suggests more reducing gases (more pollutants).* 

### Understanding the Air Quality Score:

The score provides a relative indication of air quality in your specific environment. It's not an absolute measure (like a specific PPM value) but rather shows how the current air quality compares to recent conditions. Adjust the `calculate_air_quality_score` function in `bmp_reader.py` if you need to fine-tune its sensitivity or range.

This dynamic approach helps to account for natural fluctuations in ambient air and provides a more context-aware assessment of air quality changes.
