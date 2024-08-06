import json
import os

from utils.env import Env

Env.init()

json_paths = {
    "run_process": os.path.join(Env.base_path, "src/dataset/run_process.json"),
    "find_requirement": os.path.join(Env.base_path, "src/dataset/find_Req.json"),
    "fix_error": os.path.join(Env.base_path, "src/dataset/fix_error.json"),
    "divide_to_simple": os.path.join(
        Env.base_path, "src/dataset/divide_to_simple.json"
    ),
}

data = {}
for name, path in json_paths.items():
    data[name] = json.load(open(path))


id = 0
dataset_id = 0


def parse(items):
    global id, dataset_id
    dataset_id += 1
    i = 0
    for item in items:
        id += 1
        item["id"] = id
        item["dataset_id"] = dataset_id
        item = {"id": id, "dataset_id": dataset_id, **item}
        items[i] = item
        i += 1
    return items


all = []
for name in data:
    all += parse(data[name])

print(json.dumps(all, indent=2))
open(os.path.join(Env.base_path, "database/seeders/dataset_item.json"), "w").write(
    json.dumps({"table": "dataset_items", "items": all}, indent=2)
)
