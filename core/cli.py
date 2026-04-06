import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Monitoring System")
    parser.add_argument("--config", default="config/config.json")
    return parser.parse_args()