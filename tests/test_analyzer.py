import math
from core.analyzer import EWMAState, SignalAnalyzer

def test_ewma_updates():
    state = EWMAState()
    mean, std = state.update(50.0)
    assert mean == 50.0
    assert std == 0.0

def test_ewma_detects_spike():
    state = EWMAState()
    for v in [50, 51, 49, 50, 52, 50]:
        state.update(float(v))
    mean, std = state.update(200.0)
    assert mean > 50
    assert state.threshold < 200.0

def test_analyzer_returns_alert_on_spike():
    config = {}
    analyzer = SignalAnalyzer(config)
    for _ in range(10):
        analyzer.analyze_metrics({"cpu": 50, "memory": 50, "latency": 100})
    alerts = analyzer.analyze_metrics({"cpu": 99, "memory": 99, "latency": 499})
    assert len(alerts) > 0
