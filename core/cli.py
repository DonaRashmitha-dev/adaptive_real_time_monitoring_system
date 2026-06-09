import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Adaptive Real-Time Monitoring System")
    parser.add_argument("--config", default="config/config.json", help="Path to config JSON")
    return parser.parse_args()
