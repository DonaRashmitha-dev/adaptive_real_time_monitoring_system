# 🚀 Adaptive Real-Time Monitoring System

## 📌 Overview
This project is a fault-aware real-time monitoring system designed to detect anomalies in system behavior using adaptive thresholds instead of static rules.

It simulates production-like environments where systems must detect failures such as crashes, latency spikes, and resource exhaustion in real time.

---

## 🧠 Key Concepts Implemented
- Adaptive anomaly detection (dynamic thresholds based on runtime behavior)
- Severity-based prioritization of events
- Multithreaded log processing
- Fault injection testing integration
- Cross-language system design (Python + C++ + Node.js)

---

## ⚙️ System Architecture
# 🚀 Adaptive Real-Time Monitoring System

## 📌 Overview
This project is a fault-aware real-time monitoring system designed to detect anomalies in system behavior using adaptive thresholds instead of static rules.

It simulates production-like environments where systems must detect failures such as crashes, latency spikes, and resource exhaustion in real time.

---

## 🧠 Key Concepts Implemented
- Adaptive anomaly detection (dynamic thresholds based on runtime behavior)
- Severity-based prioritization of events
- Multithreaded log processing
- Fault injection testing integration
- Cross-language system design (Python + C++ + Node.js)

---

## ⚙️ System Architecture
Log Generator → Core Analyzer → Metric Engine (C++) → Alert System (Webhook)

---

## 🔥 Features

- Detects anomalies using runtime behavior (not fixed thresholds)
- Classifies events based on severity
- Handles concurrent log processing
- Integrates C++ for high-performance metric computation
- Sends alerts via webhook server

---

## 🛠️ Tech Stack

- Python (core logic, anomaly detection)
- C++ (high-performance metrics computation)
- Node.js (webhook alert system)
- Multithreading & system-level debugging concepts

---

## ▶️ How to Run

### 1. Install dependencies
'''bash
pip install -r requirements.txt
'''
### 2. Compile C++ module
'''bash
g++ metrics_cpp/metrics.cpp -o metrics
'''
### 3. Start webhook server
'''bash
node webhook_server/server.js
'''
### 4. Start log generator
'''bash
python generator/log_generator.py
'''
### 5. Run Monitoring System
'''bash
python -m core.monitor
'''
monitor

🔄 How It Works
Log generator simulates real system logs
Core analyzer processes logs in real time
Metrics engine evaluates anomalies
Alerts are triggered based on severity
Webhook server receives and displays alerts
Example Output
🚨 ALERT: CPU anomaly
🚨 ALERT: Memory anomaly
