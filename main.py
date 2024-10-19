import matplotlib
matplotlib.use('TkAgg')
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import threading

# Rest of the code remains the same


from collections import deque
sns.set(style="darkgrid")

# Define the data stream generator
def simulate_data_stream(season_length=50, noise_level=0.5, trend=0.01, duration=1000):
    t = 0
    while t < duration:
        # Seasonality
        seasonal = np.sin(2 * np.pi * t / season_length)
        # Random noise
        noise = np.random.normal(0, noise_level)
        value = seasonal + trend * t + noise

        # Occasionally inject an anomaly   # 15% chance of anomaly
        if np.random.rand() < 0.15:
            value += np.random.uniform(-3, 3)
            #further overall 7.5% of chance of anomaly in range(-10 , 10)
            if np.random.rand() < 0.5: 
                value += np.random.uniform(-7, 7)

        yield value
        t += 1
        # Simulate real-time streaming with delay
        time.sleep(0.1)

# Anomaly Detection Class
# window_size: Number of data points in the moving window
# z_threshold: Z-score threshold for anomaly detection
# Data window for calculating moving average and std deviation
class RealTimeAnomalyDetectorZScore:
    def __init__(self, window_size=50, z_threshold=1.5):
        self.window_size = window_size  
        self.z_threshold = z_threshold  
        self.data_window = deque(maxlen=window_size)

    def update_model(self, value):
        # Update the moving window with the new value
        self.data_window.append(value)

    def detect_anomaly(self, value):
        # Not enough data for anomaly detection
        if len(self.data_window) < self.window_size:
            return None  

        # Calculate moving average and standard deviation
        mean = np.mean(self.data_window)
        std_dev = np.std(self.data_window)

        # Calculate the Z-score for the current value
        if std_dev == 0:
            z_score = 0
        else:
            z_score = (value - mean) / std_dev

        # Detect anomaly if the Z-score exceeds the threshold
        if np.abs(z_score) > self.z_threshold:
            print(f"Anomaly Detected: Value [{value}], Z-Score [{z_score}], Mean [{mean}], Standard Deviation [{std_dev}]")
            return "Anomaly Detected", z_score, mean, std_dev
        else:
            return None

sns.set(style="darkgrid", context="talk")
check = True

stop_event = threading.Event()

def on_close(event):
    """Handler for closing the graph window."""
    print("Closing the graph window...")
    stop_event.set()  # Trigger the stop event when the window is closed
xlen = 100000 
def run_plot():
    sns.set_context("talk")
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    
    # Create plots for the data stream, normal points, and anomalies
    # Black dashed line for the data stream
    line, = ax.plot([], [], 'k--', lw=1, label='Data Stream')  
    # Red points for anomalies and Blue points for normal data
    anomaly_points, = ax.plot([], [], 'ro', label='Anomalies', markersize=8)  
    normal_points, = ax.plot([], [], 'bo', label='Normal', markersize=5)  

    fig.canvas.mpl_connect('close_event', on_close)


    ax.set_title('Live Data Stream with Anomaly Detection')
    ax.set_xlabel('Time (milliseconds)')
    ax.set_ylabel('Value (floating point)')

    # Create a transparent legend
    ax.legend(loc='upper left', frameon=True, fontsize='small', shadow=True, fancybox=True, framealpha=0.5)

    xdata, ydata = [], []
    normal_xdata, normal_ydata = [], []
    anomaly_xdata, anomaly_ydata = [] ,[]
    detector = RealTimeAnomalyDetectorZScore(window_size=50, z_threshold=1.5)

    # Record the start time for elapsed time tracking
    start_time = time.time()

    # Simulate data stream
    data_gen = simulate_data_stream()

    for frame in data_gen:
        # Check if stop event is triggered
        if stop_event.is_set():
            break
        # Elapsed time in milliseconds
        current_time = (time.time() - start_time) * 1000
        value = frame

        # Update the main data points
        xdata.append(current_time)
        ydata.append(value)

        # Update the anomaly detector model
        detector.update_model(value)

        # Detect anomalies
        anomaly_result = detector.detect_anomaly(value)
        if anomaly_result:
            anomaly_xdata.append(current_time)
            anomaly_ydata.append(value)
        else:
            normal_xdata.append(current_time)
            normal_ydata.append(value)

        # Limit the data to the latest 100 points
        if len(xdata) > xlen:
            xdata.pop(0)
            ydata.pop(0)
        if len(normal_xdata) > xlen:
            normal_xdata.pop(0)
            normal_ydata.pop(0)
        if len(anomaly_xdata) > xlen:
            anomaly_xdata.pop(0)
            anomaly_ydata.pop(0)

        # Update the lines and points in the plot
        line.set_data(xdata, ydata)
        normal_points.set_data(normal_xdata, normal_ydata)
        anomaly_points.set_data(anomaly_xdata, anomaly_ydata)
        # Dynamically adjust the x-axis to show the latest data upto xlen= 100000 no of points
        if current_time < xlen:
            ax.set_xlim(0, current_time)
        else:
            ax.set_xlim(current_time - xlen, current_time)

        # Dynamically adjust the y-axis to fit the data
        if ydata:  # Check if ydata is not empty
            # Add 10% buffer below the minimum and 10% buffer above the maximum
            y_min = min(ydata) - 0.1 * abs(min(ydata)) 
            y_max = max(ydata) + 0.1 * abs(max(ydata))  
            ax.set_ylim(y_min, y_max)
        # Pause to allow for the GUI to update
        plt.pause(0.1)

    # Pause to allow for the GUI to update
    plt.ioff()
    if( check == False):
        return 
    plt.show()

# Main function to run the plotting and input handling
def main():
    print("Anomaly Detection")
    print("-----------------")
    # Run the plot
    run_plot()
    print("Exiting Program")
    sys.exit(0)

if __name__ == "__main__":
    main()