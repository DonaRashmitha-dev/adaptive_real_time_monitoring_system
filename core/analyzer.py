class SignalAnalyzer:
    def __init__(self, config):
        self.cpu_history = []
        self.memory_history = []
        self.window = config["adaptive_window"]

    def _update(self, history, value):
        history.append(value)
        if len(history) > self.window:
            history.pop(0)

    def _avg(self, history):
        return sum(history) / len(history) if history else 0

    def analyze_metrics(self, metrics):
        alerts = []

        cpu = metrics["cpu"]
        mem = metrics["memory"]
        latency = metrics["latency"]

        self._update(self.cpu_history, cpu)
        self._update(self.memory_history, mem)

        cpu_avg = self._avg(self.cpu_history)
        mem_avg = self._avg(self.memory_history)

        if cpu > cpu_avg + 20:
            alerts.append(("CPU anomaly", self._severity(cpu, mem, latency)))

        if mem > mem_avg + 20:
            alerts.append(("Memory anomaly", self._severity(cpu, mem, latency)))

        return alerts

    def analyze_log(self, log):
        alerts = []
        if log["level"] == "ERROR":
            alerts.append(("Critical log error", 90))
        return alerts

    def _severity(self, cpu, mem, latency):
        return int(cpu * 0.5 + mem * 0.3 + latency * 0.2)