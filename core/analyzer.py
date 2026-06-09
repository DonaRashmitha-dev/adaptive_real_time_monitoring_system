import math

# EWMA Adaptive Threshold Algorithm:
# 1. mean and variance update each data point using alpha=0.3 (recent data weighted more)
# 2. std_dev = sqrt(ewma_variance); threshold = ewma_mean + 2.5 * std_dev
# 3. anomaly fires only when value exceeds this dynamic threshold, never a fixed number

ALPHA = 0.3
SIGMA = 1.5

class EWMAState:
    def __init__(self):
        self.mean = None
        self.var = 0.0

    def update(self, value: float) -> tuple[float, float]:
        if self.mean is None:
            self.mean = float(value)
            self.var = 0.0
        else:
            diff = value - self.mean
            self.mean += ALPHA * diff
            self.var = (1 - ALPHA) * (self.var + ALPHA * diff * diff)
        std_dev = math.sqrt(self.var) if self.var > 0 else 0.0
        return self.mean, std_dev

    @property
    def threshold(self) -> float:
        std_dev = math.sqrt(self.var) if self.var > 0 else 0.0
        return (self.mean or 0.0) + SIGMA * std_dev

class SignalAnalyzer:
    def __init__(self, config):
        self.cpu_state     = EWMAState()
        self.memory_state  = EWMAState()
        self.latency_state = EWMAState()

    def analyze_metrics(self, metrics: dict) -> list[tuple[str, int, dict]]:
        alerts = []
        for key, state in [("cpu", self.cpu_state), ("memory", self.memory_state), ("latency", self.latency_state)]:
            value = metrics[key]
            mean, std_dev = state.update(value)
            threshold = state.threshold
            if state.mean is not None and std_dev > 1.0 and value > threshold:
                severity = self._severity(metrics)
                alerts.append((f"{key.upper()} anomaly", severity, {
                    "type": key, "value": value,
                    "threshold_at_time": round(threshold, 2),
                    "ewma_mean": round(mean, 2),
                    "ewma_std": round(std_dev, 2),
                }))
        return alerts

    def analyze_log(self, log: dict) -> list[tuple[str, int, dict]]:
        alerts = []
        if log.get("level") == "ERROR":
            alerts.append(("Critical log error", 90, {
                "type": "log", "value": 0, "threshold_at_time": 0,
                "message": log.get("message", "")
            }))
        return alerts

    def get_thresholds(self) -> dict:
        return {
            "cpu":     round(self.cpu_state.threshold, 2),
            "memory":  round(self.memory_state.threshold, 2),
            "latency": round(self.latency_state.threshold, 2),
        }

    def _severity(self, metrics: dict) -> int:
        return int(metrics["cpu"] * 0.5 + metrics["memory"] * 0.3 + metrics["latency"] * 0.2)
