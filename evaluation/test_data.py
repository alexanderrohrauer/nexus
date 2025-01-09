import copy
import json
from os import path

import pydash as _

from app.settings import get_settings


class TestDataInjector:
    batches_cache = {}
    settings = get_settings()

    def inject(self, batch_id: int, json_path: str, results: list[dict]):
        if self.settings.evaluation_mode:
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
