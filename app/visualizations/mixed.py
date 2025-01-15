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
            author_nodes = [{"id": a.uuid, "name": a.full_name, "$nexus": {"type": EntityType.RESEARCHER, "id": a.uuid}}
                            for a in w.authors]
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
        icon = kwargs.get("icon") or "institution.png"
        series = {"type": "marker",
                  "showAtZoom": kwargs.get("show_at_zoom"),
                  "data": [{"id": i.uuid, "name": i.name, "position": i.location, "icon": icon,
                            "$nexus": {"type": EntityType.INSTITUTION, "id": i.uuid}} for i in institutions]}
        result.add("institutions", Series(data=series, entity_type=EntityType.INSTITUTION))
        return result


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
                    if isinstance(affiliation.institution,
                                  Institution) and affiliation.institution.location is not None:
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
            points.append([researcher.full_name, {"value": len(researcher.works),
                                                  "$nexus": {"type": EntityType.RESEARCHER, "id": researcher.uuid}}])
        #     TODO limit could be dynamic
        # TODO maybe set color?
        points = list(reversed(sorted(points, key=lambda row: row[-1]["value"])))[:20]
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


class MixedInstitutionAggregation(Chart):
    identifier = "mixed_institution_aggregation"
    name = "Institution aggregation"
    type = ChartType.MIXED
    chart_template = ChartTemplates.DATATABLE
    generator = create_basic_generator(["institutions"])

    INSTITUTION_FIELD_NAME = "aggregate_field_name"

    @classmethod
    def to_table_series(cls, dataframe: pd.DataFrame, field_name: str):
        headers = [str(c) for c in dataframe.columns]
        headers.insert(0, field_name)
        rows = [[index] + row for index, row in zip(dataframe.index, dataframe.values.tolist())]
        return {"header": headers, "rows": rows}

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        institution_query = chart_input.get_series_query("institutions")
        field_name = chart_input.special_fields.get(MixedInstitutionAggregation.INSTITUTION_FIELD_NAME)

        institutions = await Institution.find(institution_query, nesting_depth=3, fetch_links=True).to_list()
        institutions = pd.DataFrame([i.model_dump() for i in institutions])
        institutions["avg_h_index"] = institutions["openalex_meta"].apply(
            lambda inst: inst.get("summary_stats").get("h_index"))

        grouped = institutions.groupby([field_name])

        count_series = grouped.count().rename(columns={"uuid": "count"})["count"]
        avg_h_index_series = grouped["avg_h_index"].mean()

        final_df = pd.concat([count_series, avg_h_index_series], axis=1)

        result.add("institutions", Series(data=MixedInstitutionAggregation.to_table_series(final_df, field_name),
                                          entity_type=EntityType.INSTITUTION))
        return result


class MixedWorkAggregation(Chart):
    identifier = "mixed_work_aggregation"
    name = "Work aggregation"
    type = ChartType.MIXED
    chart_template = ChartTemplates.DATATABLE
    generator = create_basic_generator(["works"])

    WORK_FIELD_NAME = "aggregate_field_name"

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        work_query = chart_input.get_series_query("works")
        field_name = chart_input.special_fields.get(MixedWorkAggregation.WORK_FIELD_NAME)

        works = await Work.find(work_query, nesting_depth=3, fetch_links=True).to_list()
        works = pd.DataFrame([i.model_dump() for i in works])
        works["avg_citations"] = works["openalex_meta"].apply(
            lambda meta: int(meta.get("cited_by_count")) if meta is not None else None)
        works["dblp_type"] = works["type"].apply(lambda inst: inst.get("dblp"))
        works["openalex_type"] = works["type"].apply(lambda inst: inst.get("openalex"))

        grouped = works.groupby([field_name])

        count_series = grouped.count().rename(columns={"uuid": "count"})["count"]
        avg_h_index_series = grouped["avg_citations"].mean()

        final_df = pd.concat([count_series, avg_h_index_series], axis=1)

        result.add("works", Series(data=MixedInstitutionAggregation.to_table_series(final_df, field_name),
                                   entity_type=EntityType.WORK))
        return result


class MixedResearchActivity(Chart):
    identifier = "mixed_research_activity"
    name = "Research activity"
    type = ChartType.MIXED
    chart_template = ChartTemplates.ECHARTS
    generator = read_generator("mixedResearchActivity.js")

    @classmethod
    def get_chart_data(cls, works: list[Work]):
        df = pd.DataFrame([w.model_dump() for w in works])

        grouped = df.groupby(["publication_date"])
        count_series = grouped.count().rename(columns={"uuid": "count"})
        dates = count_series.index.tolist()
        data = count_series["count"].tolist()

        return {"data": data, "date": dates}

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        work_query = chart_input.get_series_query("works")

        works = await Work.find(work_query, Not(Work.publication_date == None), nesting_depth=3,
                                fetch_links=True).to_list()

        chart_data = MixedResearchActivity.get_chart_data(works)

        result.add("works", Series(data=chart_data, entity_type=EntityType.WORK))
        return result


class MixedActivityYearsTypes(Chart):
    identifier = "mixed_activity_years_types"
    name = "Publication activity (years/types)"
    type = ChartType.MIXED
    chart_template = ChartTemplates.ECHARTS
    generator = read_generator("researchActivityYearsTypes.js")

    TYPE_FIELD_NAME = "activity_field_name"

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        work_query = chart_input.get_series_query("works")

        field_name = chart_input.special_fields.get(MixedActivityYearsTypes.TYPE_FIELD_NAME)

        works = await Work.find(work_query, Not(Work.publication_year == None), nesting_depth=3,
                                fetch_links=True).to_list()
        works_df = pd.DataFrame([i.model_dump() for i in works])
        works_df["dblp_type"] = works_df["type"].apply(lambda inst: inst.get("dblp"))
        works_df["openalex_type"] = works_df["type"].apply(lambda inst: inst.get("openalex"))

        grouped = works_df.groupby(['publication_year', field_name]).size().unstack(fill_value=0)

        data = grouped.to_dict(orient='list')

        years = grouped.index.tolist()

        result.add("works", Series(data={"data": data, "years": years}, entity_type=EntityType.WORK))
        return result


class KeywordCloud(Chart):
    identifier = "keyword_cloud"
    name = "Keywords (Cloud)"
    type = ChartType.MIXED
    chart_template = ChartTemplates.HIGHCHARTS
    generator = read_generator("keywordCloud.js")

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        work_query = chart_input.get_series_query("works")

        works = await Work.find(work_query, Not(Work.keywords == None), nesting_depth=3, fetch_links=True).to_list()
        df = pd.DataFrame([i.model_dump() for i in works])

        df = df.explode("keywords")
        grouped = df.groupby(["keywords"])
        count_df = grouped.count().rename(columns={"uuid": "weight"})
        data = count_df[["weight"]].to_dict(orient='index')
        result.add("works", Series(data=data, entity_type=EntityType.WORK))
        return result


class PackedKeywordsBubbleChart(Chart):
    identifier = "packed_keywords_bubble_chart"
    name = "Top-10 Keywords Researchers (Bubble)"
    type = ChartType.MIXED
    chart_template = ChartTemplates.HIGHCHARTS
    generator = read_generator("packedKeywordsBubbleChart.js")

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        work_query = chart_input.get_series_query("works")

        works = await Work.find(work_query, Not(Work.keywords == None), nesting_depth=3, fetch_links=True).to_list()
        df = pd.DataFrame([i.model_dump() for i in works])

        df_exploded = df.explode("keywords")
        top_keywords = (
            df_exploded["keywords"]
            .value_counts()
            .head(10)
            .index
        )
        filtered_df = df_exploded[df_exploded["keywords"].isin(top_keywords)]

        def get_author_stats(group):
            authors = group.explode("authors")
            author_counts = authors.value_counts()
            return [{"name": author["full_name"], "value": count,
                     "$nexus": {"type": EntityType.RESEARCHER, "id": author["uuid"]}} for author, count in
                    author_counts.items()]

        data = []
        for keyword in top_keywords:
            keyword_group = filtered_df[filtered_df["keywords"] == keyword]
            author_stats = get_author_stats(keyword_group["authors"])
            data.append({"name": keyword, "data": author_stats})

        result.add("works", Series(data=data, entity_type=EntityType.WORK))
        return result
