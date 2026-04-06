# 🚀 Adaptive Real-Time Monitoring System

## Overview
A real-time monitoring system that detects anomalies using adaptive thresholds and severity scoring.

## Features
- Adaptive anomaly detection (not fixed thresholds)
- Severity-based priority queue
- Multithreaded processing
- C++ metric engine integration
- Webhook alerting system

## Run

pip install -r requirements.txt

g++ metrics.cpp -o metrics

node webhook_server/server.js

python generator/log_generator.py

python -m core.monitor