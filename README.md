# Real-Time Anomaly Detection System

A Python-based real-time data stream anomaly detection system using Z-Score with live visualization.

## Features

- Real-time data stream simulation with seasonality, noise, and random anomalies.
- Z-Score anomaly detection using sliding windows.
- Live plotting of normal and anomalous data points.
- Customizable detection thresholds and window size.

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sagar-patidar-07/Anomaly_Detection-.git
   cd real-time-anomaly-detection
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py
   ```

## Usage

- The live plot shows normal data (blue) and anomalies (red) in real-time.
- Close the plot window to stop the program.

### Customization

- **Seasonality and Noise**: Adjust parameters in `simulate_data_stream()`.
- **Anomaly Probability**: Modify anomaly injection in the data stream.
- **Window Size & Z-Score Threshold**: Adjust in `RealTimeAnomalyDetectorZScore`.

```python
detector = RealTimeAnomalyDetectorZScore(window_size=100, z_threshold=2.0)
```

## License

This project is open-source under the [MIT License](LICENSE).