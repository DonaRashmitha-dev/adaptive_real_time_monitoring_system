import time
import requests
import threading
import logging
from queue import PriorityQueue

class EventDispatcher:
    def __init__(self, config):
        self.queue = PriorityQueue()
        self.cooldown = config["alert_cooldown"]
        self.last_sent = {}
        self.webhook = config["webhook_url"]
        self.lock = threading.Lock()

    def worker(self):
        while True:
            severity, message = self.queue.get()
            self._send(message)

    def _send(self, message):
        now = time.time()

        with self.lock:
            if message in self.last_sent:
                if now - self.last_sent[message] < self.cooldown:
                    return
            self.last_sent[message] = now

        logging.warning(f"[ALERT] {message}")

        for _ in range(3):
            try:
                requests.post(self.webhook, json={"alert": message}, timeout=2)
                break
            except:
                time.sleep(1)