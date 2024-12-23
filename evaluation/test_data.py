import copy
import json
from os import path

import pydash as _


class TestData:
    batches_cache = {}

    def populate(self, batch_id: int, json_path: str, results: list[dict]):
        self.batches_cache[f"{json_path}.{batch_id}"] = results
        # TODO configure
        docs = json.loads(
            open(path.join("/Users/alexanderrohrauer/IdeaProjects/nexus/evaluation/data", json_path), "r").read())
        batches = docs[batch_id]
        for batch in batches:
            source = self.batches_cache[f"{json_path}.{batch['batchId']}"]
            doc = copy.deepcopy(source[batch["copyOf"]])
            merged = _.merge(doc, batch["data"])
            results.append(merged)
