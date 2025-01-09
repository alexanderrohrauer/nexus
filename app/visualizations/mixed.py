from itertools import combinations

import pydash as _
from beanie.odm.operators.find.logical import Not

from app.models import Work, Institution, Researcher
from app.utils.visualization_utils import Chart, ChartType, ChartTemplates, read_generator, SeriesMap, ChartInput, \
    Series, EntityType, create_basic_generator


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


class InstitutionsMap(Chart):
    identifier = "institutions_map"
    name = "Institutions map"
    type = ChartType.MIXED
    chart_template = ChartTemplates.LEAFLET
    generator = """
        export default function(nexus) {
            return {
                series: [
                    nexus.series("institutions", {})
                ]
            }
        }
    """

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        institutions = await Institution.find(Not(Institution.location == None),
                                              chart_input.get_series_query("institutions"), nesting_depth=2,
                                              fetch_links=True).to_list()
        series = {"type": "marker",
                  "data": [{"id": i.uuid, "name": i.name, "position": i.location} for i in institutions]}
        result.add("institutions", Series(data=series, entity_type=EntityType.INSTITUTION))
        return result

# TODO remove
class Bubble(Chart):
    identifier = "bubble"
    name = "Bubble"
    type = ChartType.MIXED
    chart_template = ChartTemplates.HIGHCHARTS
    generator = read_generator("bubble.js")

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        return SeriesMap()


class WorksGeoHeatmap(Chart):
    identifier = "works_geo_heatmap"
    name = "Works Geo-Heatmap"
    type = ChartType.MIXED
    chart_template = ChartTemplates.LEAFLET
    generator = create_basic_generator(["works"])

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("works")
        works = await Work.find(query, nesting_depth=2, fetch_links=True).to_list()
        lng_lat_map = {}
        for work in works:
            for author in work.authors:
                # TODO maybe add affiliations too
                if author.institution is not None and author.institution.location is not None:
                    lng_lat = author.institution.location
                    inst_id = str(author.institution.id)
                    try:
                        lng_lat_map[inst_id][-1] = lng_lat_map[inst_id][-1] + .1
                    except KeyError:
                        lng_lat_map[inst_id] = [lng_lat[1], lng_lat[0], .1]
        data = {"type": "heatmap",
                "data": {
                    "data": list(lng_lat_map.values()),
                    # TODO could use percentiles for that...
                    "gradient": {"0.1": "blue", "0.3": "lime", "0.6": "red"},
                    "radius": 30
                }
                }
        result.add("works", Series(data=data, entity_type=EntityType.WORK))
        return result

class TopResearcherWorksCount(Chart):
    identifier = "top_researcher_works_count"
    name = "Top Researcher works count"
    type = ChartType.MIXED
    chart_template = ChartTemplates.ECHARTS
    generator = read_generator("topResearcherWorksCount.js")

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("researchers")
        researchers = await Researcher.find(query, nesting_depth=2, fetch_links=True).to_list()
        points = []
        for researcher in researchers:
            points.append([researcher.full_name, len(researcher.works)])
        #     TODO limit could be dynamic
        # TODO maybe set color?
        points = list(reversed(sorted(points, key=lambda row: row[-1])))[:20]
        result.add("researchers", Series(data=points, entity_type=EntityType.RESEARCHER))
        return result
