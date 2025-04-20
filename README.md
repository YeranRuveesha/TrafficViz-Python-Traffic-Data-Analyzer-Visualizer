# 🚦 TrafficViz – Python Traffic Data Analyzer & Visualizer

**TrafficViz** is a Python-based traffic data analysis and visualization tool designed to process real-world CSV datasets. It calculates insightful traffic statistics such as vehicle counts, peak hours, weather-based patterns, and speeding incidents. The application also visualizes traffic distribution across hours via a custom-built GUI histogram using Tkinter.

---

## 🔍 Features

- 📅 User-friendly date input with validation (including leap year support)
- 📊 Processes CSV traffic data to extract key statistics
- 📈 Visualizes data using a Tkinter Canvas histogram
- 🚗 Tracks various vehicle types (trucks, bicycles, electric vehicles, etc.)
- ⚡ Detects speeding, turning behavior, and rainy-hour patterns
- 🗂️ Supports multiple traffic datasets by date
- 💾 Saves analyzed data to a local `results.txt` file

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** – for GUI and histogram visualization
- **CSV Module** – for data parsing and analysis
- **Basic File I/O** – to store analyzed results

---

## 🚀 How to Use

### 1. Prepare the Dataset

Ensure your traffic data files are in `.csv` format and follow the expected naming pattern.  
**Examples**:
-traffic_data15062024.csv
-traffic_data16062024.csv
-traffic_data21062024.csv


📁 Place these files in the same directory as the main Python file: `Python_File.py`

---

### 2. Run the Program

Make sure Python 3.x is installed on your system. Then run:

```bash
python Python_File.py
```

### 3. Follow the Prompts

When the program starts, you will be prompted to:

- Enter a valid date (e.g., `15/06/2024`)

If a matching CSV file is found:

- 🚦 **Traffic statistics** will be displayed in the terminal  
- 📝 **Results** will be saved in `results.txt`  
- 📊 A **GUI histogram** will open showing vehicle frequency per hour

---

### 4. Switch or Exit

After analyzing a dataset:

- Type `Y` to analyze another date  
- Type `N` to exit the program

---

## 📸 Preview

![image](https://github.com/user-attachments/assets/4d5c1072-a03e-432b-8954-e382c13acaff)

![image](https://github.com/user-attachments/assets/9d217ce5-beff-4b00-9838-d637b0407c11)

---



