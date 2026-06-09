import time
import random
import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

LEVELS   = ["INFO", "WARNING", "ERROR"]
MESSAGES = {
    "INFO":    ["Task started", "Processing complete", "Heartbeat OK", "Cache hit"],
    "WARNING": ["High memory usage", "Latency spike detected", "Queue backlog growing"],
    "ERROR":   ["Task failed", "Connection timeout", "Service unreachable", "OOM killed"],
}

print(f"[log_generator] Writing to {LOG_FILE}")

while True:
    level = random.choices(LEVELS, weights=[0.6, 0.3, 0.1])[0]
    log   = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level":     level,
        "service":   "core-engine",
        "message":   random.choice(MESSAGES[level]),
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")
    print(json.dumps(log))
    time.sleep(1)
