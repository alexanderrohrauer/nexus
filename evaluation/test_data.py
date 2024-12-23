import copy
import json
from os import path

import pydash as _


class TestDataInjector:
    batches_cache = {}

    def inject(self, batch_id: int, json_path: str, results: list[dict]):
        self.batches_cache[f"{json_path}.{batch_id}"] = results
        # TODO configure
        docs = json.loads(
            open(path.join("/Users/alexanderrohrauer/IdeaProjects/nexus/evaluation/data", json_path), "r").read())
        mutations = docs[batch_id]
        for mutation in mutations:
            source = self.batches_cache[f"{json_path}.{mutation['batchId']}"]
            doc = copy.deepcopy(source[mutation["copyOf"]])
            merged = _.merge(doc, mutation["data"])
            results.append(merged)
