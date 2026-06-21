import json
from owner import Owner

def save(owner, path):
    with open(path, "w") as file:
        json.dump(owner.to_dict(), file, indent=2)

def load(path):
    with open(path) as file:
        return Owner.from_dict(json.load(file))
