import time
import random
import json
from datetime import datetime, timezone
import os

LOG_FILE = "../logs/app.log"
os.makedirs("../logs", exist_ok=True)

levels = ["INFO", "WARNING", "ERROR"]

messages = {
    "INFO": ["Task started", "Processing", "Heartbeat OK"],
    "WARNING": ["High memory usage", "Latency spike"],
    "ERROR": ["Task failed", "Connection timeout"]
}

while True:
    level = random.choice(levels)
    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": "core-engine",
        "message": random.choice(messages[level])
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")

    print(log)
    time.sleep(1)