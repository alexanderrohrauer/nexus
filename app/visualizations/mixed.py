from itertools import combinations

import numpy as np
import pandas as pd
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
        works = await Work.find(query, nesting_depth=3, fetch_links=True).limit(30).to_list()
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
    generator = create_basic_generator(["institutions"])

    async def get_series(self, chart_input: ChartInput, **kwargs) -> SeriesMap:
        result = SeriesMap()
        institutions = await Institution.find(Not(Institution.location == None),
                                              chart_input.get_series_query("institutions"), nesting_depth=3,
                                              fetch_links=True).to_list()
        series = {"type": "marker",
                  "showAtZoom": kwargs.get("show_at_zoom"),
                  "data": [{"id": i.uuid, "name": i.name, "position": i.location, "icon": kwargs.get("icon"),
                            "$nexus": {"type": EntityType.INSTITUTION, "id": i.uuid}} for i in institutions]}
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
    generator = create_basic_generator(["works", "institutions"])

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("works")
        works = await Work.find(query, nesting_depth=3, fetch_links=True).to_list()
        lng_lat_map = {}
        for work in works:
            for author in work.authors:
                affiliations = filter(lambda a: work.publication_year in a.years, author.affiliations or [])
                for affiliation in affiliations:
                    if isinstance(affiliation.institution, Institution) and affiliation.institution.location is not None:
                        lng_lat = affiliation.institution.location
                        inst_id = str(affiliation.institution.id)
                        try:
                            lng_lat_map[inst_id][-1] = lng_lat_map[inst_id][-1] + 1
                        except KeyError:
                            lng_lat_map[inst_id] = [lng_lat[1], lng_lat[0], 1]

        heatmap_data = list(lng_lat_map.values())
        np_data = np.array(heatmap_data)
        series = pd.Series(np_data[:, 2])
        scaled = series / series.abs().max()
        np_data[:, 2] = scaled
        q2 = str(scaled.quantile(.5))
        q3 = str(scaled.quantile(.75))

        data = {"type": "heatmap",
                "data": {
                    "data": np_data.tolist(),
                    "gradient": {"0.0": "blue", q2: "lime", q3: "red"},
                    "radius": 15,
                    "minOpacity": .2
                }
                }

        result.add("works", Series(data=data, entity_type=EntityType.WORK))

        institution_vis = InstitutionsMap()
        institution_map = await institution_vis.get_series(chart_input, icon="dot.svg", show_at_zoom=3)

        return result + institution_map


class TopResearcherWorksCount(Chart):
    identifier = "top_researcher_works_count"
    name = "Top Researcher works count"
    type = ChartType.MIXED
    chart_template = ChartTemplates.ECHARTS
    generator = read_generator("topResearcherWorksCount.js")

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("researchers")
        researchers = await Researcher.find(query, nesting_depth=3, fetch_links=True).to_list()
        points = []
        for researcher in researchers:
            points.append([researcher.full_name, len(researcher.works)])
        #     TODO limit could be dynamic
        # TODO maybe set color?
        points = list(reversed(sorted(points, key=lambda row: row[-1])))[:20]
        result.add("researchers", Series(data=points, entity_type=EntityType.RESEARCHER))
        return result


class BasicStats(Chart):
    identifier = "basic_stats"
    name = "Basic stats"
    type = ChartType.MIXED
    chart_template = ChartTemplates.MARKDOWN
    generator = create_basic_generator(["researchers", "institutions", "works"])

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        works_query = chart_input.get_series_query("works")
        researcher_query = chart_input.get_series_query("researchers")
        institution_query = chart_input.get_series_query("institutions")

        works_count = await Work.find(works_query, nesting_depth=3, fetch_links=True).count()
        researchers_count = await Researcher.find(researcher_query, nesting_depth=3, fetch_links=True).count()
        institutions_count = await Institution.find(institution_query, nesting_depth=3, fetch_links=True).count()

        # TODO maybe add some more stats...
        works_md = f"""
### Works
**Total count:** {works_count}
        """
        result.add("works", Series(data=works_md, entity_type=EntityType.WORK))
        researchers_md = f"""
### Researchers
**Total count:** {researchers_count}
        """
        result.add("researchers", Series(data=researchers_md, entity_type=EntityType.RESEARCHER))
        institutions_md = f"""
### Institutions
**Total count:** {institutions_count}
        """
        result.add("institutions", Series(data=institutions_md, entity_type=EntityType.INSTITUTION))
        return result

#TODO complete
class MixedInstitutionAggregation(Chart):
    identifier = "mixed_institution_aggregation"
    name = "Institution aggregation"
    type = ChartType.MIXED
    chart_template = ChartTemplates.DATATABLE
    generator = create_basic_generator(["institutions"])

    INSTITUTION_FIELD_NAME = "aggregate_field_name"

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        institution_query = chart_input.get_series_query("institutions")
        field_name = chart_input.special_fields.get(MixedInstitutionAggregation.INSTITUTION_FIELD_NAME)

        institutions = await Institution.find(institution_query, nesting_depth=3, fetch_links=True).to_list()
        institutions = pd.DataFrame([i.model_dump() for i in institutions])
        grouped = institutions.groupby([field_name])
        count_series = grouped.count().rename(columns={"uuid": "count"})["count"]
        final_df = pd.DataFrame(count_series)
        # TODO eventually add other aggregates
        headers = [str(c) for c in final_df.columns]
        headers.insert(0, field_name)
        rows = [[index] + row for index, row in zip(final_df.index, final_df.values.tolist())]
        result.add("institutions", Series(data={"header": headers, "rows": rows}, entity_type=EntityType.INSTITUTION))
        return result
