from itertools import combinations

import pydash as _
from beanie import PydanticObjectId
from beanie.odm.operators.find.comparison import In

from app.models import Affiliation, Work
from app.utils.visualization_utils import Chart, ChartType, ChartTemplates, ChartInput, SeriesMap, \
    create_basic_generator, EntityType, Series, read_generator


# from app.visualizations import MixedResearchActivity


class ResearcherAffiliations(Chart):
    identifier = "researcher_affiliations"
    name = "Researcher affiliations"
    type = ChartType.RESEARCHER
    chart_template = ChartTemplates.CUSTOM
    generator = create_basic_generator(["affiliations"])

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("affiliations")
        researcher = chart_input.researcher
        affiliations = researcher.affiliations or []
        ids = [a.ref.id for a in affiliations]
        affiliations = await Affiliation.find(query, In(Affiliation.id, ids), fetch_links=True, nesting_depth=2).to_list()

        result.add("affiliations", Series(data=affiliations, entity_type=EntityType.AFFILIATIONS))
        return result

class ResearcherPerformance(Chart):
    identifier = "researcher_performance"
    name = "Performance"
    type = ChartType.RESEARCHER
    chart_template = ChartTemplates.ECHARTS
    generator = read_generator("researcherPerformance.js")

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        researcher = chart_input.researcher

        if researcher.openalex_meta is not None and "summary_stats" in researcher.openalex_meta:
            stats = researcher.openalex_meta["summary_stats"]

            result.add("h_index", Series(data=stats["h_index"], entity_type=None))
            result.add("2yr_mean_citedness", Series(data=stats["2yr_mean_citedness"], entity_type=None))
            result.add("i10_index", Series(data=stats["i10_index"], entity_type=None))


        return result

class ResearcherRelationGraph(Chart):
    identifier = "researcher_relation_graph"
    name = "Relations"
    type = ChartType.RESEARCHER
    chart_template = ChartTemplates.ECHARTS
    generator = read_generator("researcherRelationGraph.js")

    def get_nodes_and_links(self, l1: list[Work], cat_func, size_func ):
        nodes = []
        links = []
        for w in l1:
            author_nodes = [{"id": a.uuid, "name": a.full_name, "category": cat_func(a), "symbolSize": size_func(a), "$nexus": {"type": EntityType.RESEARCHER, "id": a.uuid}} for a in w.authors]
            nodes = nodes + author_nodes
            author_ids = [a.uuid for a in w.authors]
            pairs = list(combinations(author_ids, 2))
            pairs = [{"source": s, "target": t} for s, t in pairs]
            links = links + pairs
        return nodes, links

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("works")
        researcher = chart_input.researcher

        l1 = await Work.find(query, Work.authors.id == PydanticObjectId(researcher.id), fetch_links=True, nesting_depth=2).to_list()
        nodes1, links1 = self.get_nodes_and_links(l1, lambda a: 0 if a.uuid == researcher.uuid else 1, lambda a: 60 if a.uuid == researcher.uuid else 25)

        l2_nodes = filter(lambda a: a["category"] == 1, nodes1)
        l2 = await Work.find(query, In(Work.authors.uuid, [n["id"] for n in l2_nodes]), fetch_links=True, nesting_depth=2).to_list()
        nodes2, links2 = self.get_nodes_and_links(l2, lambda a: 2, lambda a: 10)

        nodes = nodes1 + nodes2
        links = links1 + links2
        nodes = _.uniq_by(nodes, lambda a: a["id"])

        result.add("works", Series(data={"data": nodes, "links": links}, entity_type=EntityType.WORK))

        return result

# class ResearcherActivity(Chart):
#     identifier = "researcher_activity"
#     name = "Publication activity"
#     type = ChartType.RESEARCHER
#     chart_template = ChartTemplates.ECHARTS
#     generator = read_generator("mixedResearchActivity.js")
#
#     async def get_series(self, chart_input: ChartInput) -> SeriesMap:
#         result = SeriesMap()
#         work_query = chart_input.get_series_query("works")
#         researcher = chart_input.researcher
#
#         works = await Work.find(work_query, Work.authors.id == PydanticObjectId(researcher.id), nesting_depth=2, fetch_links=True).to_list()
#
#         chart_data = MixedResearchActivity.get_chart_data(works)
#
#         result.add("works", Series(data=chart_data, entity_type=EntityType.WORK))
#         return result
