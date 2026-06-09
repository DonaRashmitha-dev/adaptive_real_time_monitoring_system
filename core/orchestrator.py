class StreamOrchestrator:
    def __init__(self, analyzer, queue):
        self.analyzer = analyzer
        self.queue    = queue

    def handle_metrics(self, metrics: dict):
        for msg, severity, meta in self.analyzer.analyze_metrics(metrics):
            self.queue.put((-severity, msg, meta))

    def handle_log(self, log: dict):
        for msg, severity, meta in self.analyzer.analyze_log(log):
            self.queue.put((-severity, msg, meta))
