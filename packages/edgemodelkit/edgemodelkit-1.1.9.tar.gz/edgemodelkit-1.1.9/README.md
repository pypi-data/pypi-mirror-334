# **EdgeModelKit**: Sensor Data Acquisition and Logging Library

EdgeModelKit is a Python library developed by **EdgeNeuron**, designed to simplify sensor data acquisition, logging, and real-time processing for IoT devices. It works seamlessly with the **DataLogger script** from the [EdgeNeuron Arduino library](https://github.com/ConsentiumIoT/EdgeNeuron), making it ideal for edge computing and machine learning applications.

---

## **Features**

- **Serial Communication**: Supports data acquisition over serial ports with robust error handling.  
- **Flexible Data Fetching**: Retrieve sensor data as Python lists or NumPy arrays.  
- **Customizable Logging**: Log sensor data into CSV files with optional timestamps and counters.  
- **Class-Based Organization**: Log data with class labels to prepare datasets for machine learning tasks.  
- **Custom Preprocessing**: Apply custom preprocessing functions to sensor data before logging or inference.  
- **Error Handling**: Gracefully handles data decoding errors and missing keys in sensor data packets.  

---

## **Usage Prerequisites**

This library is designed to work in conjunction with the **DataLogger script** available in the [EdgeNeuron Arduino library](https://github.com/ConsentiumIoT/EdgeNeuron). The DataLogger script configures your Arduino-based IoT device to send structured JSON sensor data over a serial connection.

Before using EdgeModelKit, ensure:  
1. Your Arduino device is programmed with the **DataLogger script** from the [EdgeNeuron Arduino library](https://github.com/ConsentiumIoT/EdgeNeuron).  
2. The device is connected to your system via a serial interface.  

---

## **Installation**

Install EdgeModelKit using pip:

```bash
pip install edgemodelkit
```

---

## **Quick Start**

### **1. Initialize the DataFetcher**

```python
from edgemodelkit import DataFetcher

# Initialize the DataFetcher with the desired serial port and baud rate
fetcher = DataFetcher(serial_port="COM3", baud_rate=9600)
```

### **2. Fetch Sensor Data**

```python
# Fetch data as a Python list
sensor_data = fetcher.fetch_data(return_as_numpy=False)
print("Sensor Data:", sensor_data)

# Fetch data as a NumPy array
sensor_data_numpy = fetcher.fetch_data(return_as_numpy=True)
print("Sensor Data (NumPy):", sensor_data_numpy)
```

### **3. Log Sensor Data**

```python
# Log 10 samples to a CSV file with timestamp and count columns
fetcher.log_sensor_data(class_label="ClassA", num_samples=10, add_timestamp=True, add_count=True)
```

---

## **CSV Logging Details**

The CSV file is generated automatically based on the sensor name (e.g., `TemperatureSensor_data_log.csv`) and contains the following:  

- **Timestamp**: (Optional) Records the time when the data was logged.  
- **Sample Count**: (Optional) A sequential counter for each data sample.  
- **Data Columns**: Each element in the sensor data array is stored in separate columns (e.g., `data_value_1`, `data_value_2`, ...).  

The data is saved under a folder named `Dataset`, with subfolders organized by `class_label` (if specified).  

---

## **Real-Time Data Processing Example**

```python
from edgemodelkit import DataFetcher

fetcher = DataFetcher(serial_port="COM3", baud_rate=9600)

def custom_preprocess(data):
    # Example: Normalize the data
    return (data - min(data)) / (max(data) - min(data))

try:
    while True:
        # Fetch data as NumPy array
        sensor_data = fetcher.fetch_data(return_as_numpy=True)
        print("Received Data (Raw):", sensor_data)

        # Apply custom preprocessing
        processed_data = custom_preprocess(sensor_data)
        print("Preprocessed Data:", processed_data)

        # Perform custom processing (e.g., feed to a TensorFlow model)
        # prediction = model.predict(processed_data)
        # print("Prediction:", prediction)
finally:
    fetcher.close_connection()
```

---

## **Using ModelPlayGround**

### **1. Initialize the ModelPlayGround**

```python
from edgemodelkit import ModelPlayGround

# Initialize the ModelPlayGround with the path to your .keras model
playground = ModelPlayGround()
playground.load_model(model_path="path_to_your_model.keras")
```

### **2. View Model Summary**

```python
# Display the model architecture
playground.model_summary()
```

### **3. View Model Statistics**

```python
# View model size and number of parameters
playground.model_stats()
```

### **4. Convert Model to TensorFlow Lite**

```python
# Convert the model to TFLite format with default quantization
playground.model_converter(quantization_type="default")

# Convert the model to TFLite format with float16 quantization
playground.model_converter(quantization_type="float16")

# Convert the model to TFLite format with int8 quantization
playground.model_converter(quantization_type="int8")
```

### **5. Test TFLite Model on Live Data**

```python
from edgemodelkit import DataFetcher

# Initialize a DataFetcher
fetcher = DataFetcher(serial_port="COM3", baud_rate=9600)

def custom_preprocess(data):
    # Example: Normalize the data
    return (data - min(data)) / (max(data) - min(data))

# Perform live testing of the TFLite model
playground_output = playground.edge_testing(
    data_fetcher=fetcher,
    preprocess_func=custom_preprocess
)
print("Model Prediction: ", playground_output['ModelOutput'])
print("Sensor data: ", playground_output['SensorData'])
```

### **6. Export the TFLM model**

```python
from edgemodelkit import DataFetcher

# Initialize a DataFetcher
fetcher = DataFetcher(serial_port="COM3", baud_rate=9600)

def custom_preprocess(data):
    # Example: Normalize the data
    return (data - min(data)) / (max(data) - min(data))

# Perform live testing of the TFLite model
playground_output = playground.edge_testing(
    tflite_model_path="path_to_tflite_model.tflite",
    data_fetcher=fetcher,
    preprocess_func=custom_preprocess
)
print("Model Prediction: ", playground_output['ModelOutput'])
print("Sensor data: ", playground_output['SensorData'])
```

---

## **Disclaimer**

Currently, the `ModelPlayGround` class supports only `.keras` models for conversion and testing. Support for other model formats may be added in future updates.

---

## **Contributing**

We welcome contributions to EdgeModelKit! Feel free to submit bug reports, feature requests, or pull requests on our [GitHub repository](https://github.com/ConsentiumIoT/edgemodelkit).

---

## **License**

EdgeModelKit is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Support**

For support and inquiries, contact us at **support@edgeneuronai.com** or visit our [GitHub repository](https://github.com/ConsentiumIoT/edgemodelkit).

---

## **About EdgeNeuron**

EdgeNeuron is a pioneer in edge computing solutions, enabling developers to build intelligent IoT applications with state-of-the-art tools and libraries. Learn more at [edgeneuronai.com](https://edgeneuronai.com).

