import gzip
import json
import pickle

import yaml


def load_traj_file(path: str):
    if path.endswith(".pkl"):
        with open(path, "rb") as f:
            return pickle.load(f)
    elif path.endswith(".pkl.gz"):
        with gzip.open(path, "rb") as f:
            return pickle.load(f)
    elif path.endswith(".json"):
        with open(path) as f:
            return json.load(f)
    elif path.endswith(".yaml"):
        with open(path) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    else:
        raise ValueError(f"Unsupported file extension: {path}")


def save_traj_file(data: dict, path: str):
    if path.endswith(".pkl"):
        with open(path, "wb") as f:
            pickle.dump(data, f)
    elif path.endswith(".pkl.gz"):
        with gzip.open(path, "wb", compresslevel=1) as f:
            pickle.dump(data, f)
    elif path.endswith(".json"):
        with open(path, "w") as f:
            json.dump(data, f)
    elif path.endswith(".yaml"):
        with open(path, "w") as f:
            yaml.dump(data, f)
    else:
        raise ValueError(f"Unsupported file extension: {path}")
