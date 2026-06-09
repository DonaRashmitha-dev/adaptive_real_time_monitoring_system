import time
import threading
import logging
import json
import os
import requests
from queue import PriorityQueue
from datetime import datetime, timezone

try:
    import redis
    REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379")
    _redis = redis.from_url(REDIS_URL)
    _redis.ping()
    REDIS_AVAILABLE = True
except Exception:
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)


class EventDispatcher:
    def __init__(self, config):
        self.queue     = PriorityQueue()
        self.cooldown  = config["alert_cooldown"]
        self.last_sent = {}
        self.webhook   = config["webhook_url"]
        self.lock      = threading.Lock()

    def worker(self):
        while True:
            severity, message, meta = self.queue.get()
            self._send(message, meta)

    def _send(self, message: str, meta: dict):
        now = time.time()
        with self.lock:
            if message in self.last_sent and now - self.last_sent[message] < self.cooldown:
                return
            self.last_sent[message] = now

        ratio = (meta.get("value", 0) / meta.get("threshold_at_time", 1)) if meta.get("threshold_at_time") else 1
        severity_label = "CRITICAL" if ratio >= 1.5 else "WARNING" if ratio >= 1.2 else "INFO"

        payload = {
            "timestamp":         datetime.now(timezone.utc).isoformat(),
            "alert":             message,
            "type":              meta.get("type", "unknown"),
            "severity":          severity_label,
            "value":             meta.get("value", 0),
            "threshold_at_time": meta.get("threshold_at_time", 0),
        }

        logger.warning(json.dumps({"event": "alert_dispatched", **payload}))

        # Push to Redis pub/sub if available, else fall back to direct webhook
        if REDIS_AVAILABLE:
            try:
                _redis.publish("alerts", json.dumps(payload))
                logger.info(json.dumps({"event": "alert_published_to_redis", "alert": message}))
                return
            except Exception as e:
                logger.error(json.dumps({"event": "redis_publish_failed", "error": str(e)}))

        # Fallback: direct webhook
        for attempt in range(3):
            try:
                requests.post(self.webhook, json=payload, timeout=2)
                break
            except Exception as e:
                logger.error(json.dumps({"event": "webhook_failed", "attempt": attempt + 1, "error": str(e)}))
                time.sleep(1)
