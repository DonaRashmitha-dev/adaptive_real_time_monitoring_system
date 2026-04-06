import json
import threading
import time
import subprocess
import os
import logging
import signal
import sys

from core.analyzer import SignalAnalyzer
from core.orchestrator import StreamOrchestrator
from core.dispatcher import EventDispatcher
from core.cli import parse_args

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(threadName)s | %(message)s"
)

running = True

def shutdown(sig, frame):
    global running
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)


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

                cpu, mem, lat = map(int, line.strip().split(","))
                yield {"cpu": cpu, "memory": mem, "latency": lat}

        except:
            time.sleep(2)


def log_stream():
    os.makedirs("logs", exist_ok=True)
    open("logs/app.log", "a").close()

    with open("logs/app.log") as f:
        f.seek(0, 2)

        while running:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue

            try:
                yield json.loads(line.strip())
            except:
                continue


def main():
    args = parse_args()

    with open(args.config) as f:
        config = json.load(f)

    analyzer = SignalAnalyzer(config)
    dispatcher = EventDispatcher(config)
    orchestrator = StreamOrchestrator(analyzer, dispatcher.queue)

    threads = [
        threading.Thread(target=dispatcher.worker, daemon=True),
        threading.Thread(target=lambda: [orchestrator.handle_metrics(m) for m in metric_stream()], daemon=True),
        threading.Thread(target=lambda: [orchestrator.handle_log(l) for l in log_stream()], daemon=True),
    ]

    for t in threads:
        t.start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()