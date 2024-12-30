from itertools import combinations

import pydash as _

from app.models import Work
from app.utils.visualization_utils import Chart, ChartType, ChartTemplates, read_generator, SeriesMap, ChartInput, \
    Series, EntityType


class ResearcherEdgeBundling(Chart):
    identifier = "researcher_edge_bundling"
    name = "Researcher Edge-Bundling"
    type = ChartType.MIXED
    chart_template = ChartTemplates.ECHARTS
    generator = read_generator("relations.js")

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("researchers")
        works = await Work.find(query, nesting_depth=2, fetch_links=True).limit(30).to_list()
        nodes = []
        links = []
        for w in works:
            author_nodes = [{"id": a.uuid, "name": a.full_name} for a in w.authors]
            nodes = nodes + author_nodes
            author_ids = [a.uuid for a in w.authors]
            pairs = list(combinations(author_ids, 2))
            pairs = [{"source": s, "target": t} for s, t in pairs]
            links = links + pairs
        nodes = _.uniq_by(nodes, lambda a: a["id"])
        result.add("researchers", Series(data={"data": nodes, "links": links}, entity_type=EntityType.WORK))
        return result
