import json
import threading
import time
import subprocess
import os
import logging
import signal
import requests

from core.analyzer     import SignalAnalyzer
from core.orchestrator import StreamOrchestrator
from core.dispatcher   import EventDispatcher
from core.cli          import parse_args

logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","thread":"%(threadName)s","level":"%(levelname)s","msg":%(message)s}'
)
logger = logging.getLogger(__name__)
running = True
_stop_event = threading.Event()

def shutdown(sig, frame):
    global running
    running = False
    _stop_event.set()

signal.signal(signal.SIGINT,  shutdown)
signal.signal(signal.SIGTERM, shutdown)

def binary():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "metrics_cpp", "metrics")

def metric_stream():
    while running:
        try:
            p = subprocess.Popen([binary()], stdout=subprocess.PIPE, text=True)
            for line in p.stdout:
                if not running:
                    p.terminate()
                    break
                try:
                    cpu, mem, lat = map(int, line.strip().split(","))
                    yield {"cpu": cpu, "memory": mem, "latency": lat}
                except ValueError:
                    continue
            p.wait()
        except Exception as e:
            logger.error(f'"metric_stream error: {e}"')
            time.sleep(2)

def log_stream():
    base     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base, "logs", "app.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    open(log_path, "a").close()
    with open(log_path) as f:
        f.seek(0, 2)
        while running:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            try:
                yield json.loads(line.strip())
            except json.JSONDecodeError:
                continue

def forward_metrics(metrics: dict, webhook_url: str):
    try:
        requests.post(webhook_url.replace("/alert", "/metric"), json=metrics, timeout=1)
    except Exception:
        pass

def main():
    args = parse_args()
    with open(args.config) as f:
        config = json.load(f)
    analyzer     = SignalAnalyzer(config)
    dispatcher   = EventDispatcher(config)
    orchestrator = StreamOrchestrator(analyzer, dispatcher.queue)

    def metrics_loop():
        for m in metric_stream():
            orchestrator.handle_metrics(m)
            forward_metrics(m, config["webhook_url"])

    threads = [
        threading.Thread(target=dispatcher.worker, name="dispatcher", daemon=True),
        threading.Thread(target=metrics_loop, name="metrics", daemon=True),
        threading.Thread(target=lambda: [orchestrator.handle_log(l) for l in log_stream()], name="log-watcher", daemon=True),
    ]
    for t in threads:
        t.start()
    logger.info('"monitoring system started"')
    _stop_event.wait()
    logger.info('"monitoring system stopped"')

if __name__ == "__main__":
    main()
