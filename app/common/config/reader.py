import yaml


def read_config(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)
