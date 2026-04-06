class StreamOrchestrator:
    def __init__(self, analyzer, queue):
        self.analyzer = analyzer
        self.queue = queue

    def handle_metrics(self, metrics):
        alerts = self.analyzer.analyze_metrics(metrics)
        for msg, severity in alerts:
            self.queue.put((-severity, msg))

    def handle_log(self, log):
        alerts = self.analyzer.analyze_log(log)
        for msg, severity in alerts:
            self.queue.put((-severity, msg))