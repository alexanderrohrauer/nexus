import numpy as np
import pandas as pd
from beanie.odm.operators.find.logical import Not

from app.models import Work, Institution, Researcher
from app.utils.db_utils import fix_location_util
from app.utils.visualization_utils import Chart, ChartType, ChartTemplates, read_generator, SeriesMap, ChartInput, \
    Series, EntityType, create_basic_generator


# class ResearcherEdgeBundling(Chart):
#     identifier = "researcher_edge_bundling"
#     name = "Researcher Edge-Bundling"
#     type = ChartType.MIXED
#     chart_template = ChartTemplates.ECHARTS
#     generator = read_generator("relations.js")
#
#     async def get_series(self, chart_input: ChartInput) -> SeriesMap:
#         result = SeriesMap()
#         query = chart_input.get_series_query("researchers")
#         works = await Work.find(query, nesting_depth=2, fetch_links=True).limit(30).to_list()
#         nodes = []
#         links = []
#         for w in works:
#             author_nodes = [{"id": a.uuid, "name": a.full_name, "$nexus": {"type": EntityType.RESEARCHER, "id": a.uuid}}
#                             for a in w.authors]
#             nodes = nodes + author_nodes
#             author_ids = [a.uuid for a in w.authors]
#             pairs = list(combinations(author_ids, 2))
#             pairs = [{"source": s, "target": t} for s, t in pairs]
#             links = links + pairs
#         nodes = _.uniq_by(nodes, lambda a: a["id"])
#         result.add("researchers", Series(data={"data": nodes, "links": links}, entity_type=EntityType.WORK))
#         return result


class InstitutionsMap(Chart):
    identifier = "institutions_map"
    name = "Institutions map"
    type = ChartType.MIXED
    chart_template = ChartTemplates.LEAFLET
    generator = create_basic_generator(["institutions"])

    async def get_series(self, chart_input: ChartInput, **kwargs) -> SeriesMap:
        result = SeriesMap()
        institutions = await Institution.find(Not(Institution.location == None),
                                              chart_input.get_series_query("institutions"), nesting_depth=2,
                                              fetch_links=True).to_list()
        icon = kwargs.get("icon") or "institution.png"
        series = {"type": "marker",
                  "showAtZoom": kwargs.get("show_at_zoom"),
                  "data": [{"id": i.uuid, "name": i.name, "position": fix_location_util(i.location), "icon": icon,
                            "$nexus": {"type": EntityType.INSTITUTION, "id": i.uuid}} for i in institutions]}
        result.add("institutions", Series(data=series, entity_type=EntityType.INSTITUTION))
        return result

class ResearcherMap(Chart):
    identifier = "researcher_map"
    name = "Researcher map"
    type = ChartType.MIXED
    chart_template = ChartTemplates.LEAFLET
    generator = create_basic_generator(["researchers"])

    async def get_series(self, chart_input: ChartInput, **kwargs) -> SeriesMap:
        result = SeriesMap()
        researchers = await Researcher.find(Not(Researcher.institution == None),
                                              chart_input.get_series_query("researchers"), nesting_depth=2,
                                              fetch_links=True).to_list()
        icon = kwargs.get("icon") or "researcher.png"
        series = {"type": "marker",
                  "showAtZoom": kwargs.get("show_at_zoom"),
                  "data": [{"id": r.uuid, "name": r.full_name, "position": fix_location_util(r.institution.location), "icon": icon,
                            "$nexus": {"type": EntityType.RESEARCHER, "id": r.uuid}} for r in researchers]}
        result.add("researchers", Series(data=series, entity_type=EntityType.RESEARCHER))
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
        works = await Work.find(query, nesting_depth=2, fetch_links=True).to_list()
        lng_lat_map = {}
        for work in works:
            for author in work.authors:
                if isinstance(author.institution,
                              Institution) and author.institution.location is not None:
                    lng_lat = author.institution.location
                    key = str(author.institution.location)
                    try:
                        lng_lat_map[key][-1] = lng_lat_map[key][-1] + 1
                    except KeyError:
                        lng_lat_map[key] = [lng_lat[1], lng_lat[0], 1]


        heatmap_data = list(lng_lat_map.values())
        np_data = np.array(heatmap_data)
        series_data = []
        q1 = 1
        q2 = 1
        q3 = 1
        if len(np_data)> 0:
            series = pd.Series(np_data[:, 2])
            scaled = series / series.abs().max()
            np_data[:, 2] = scaled
            q1 = np.percentile(scaled, 25)
            q2 = np.percentile(scaled, 50)
            q3 = np.percentile(scaled, 80)
            series_data = np_data.tolist()

        data = {"type": "heatmap",
                "data": {
                    "data": series_data,
                    "gradient": {q1: "blue", q2: "lime", q3: "red"},
                    "radius": 10,
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
        researchers = await Researcher.find(query, Not(Researcher.openalex_meta == None), nesting_depth=2, fetch_links=True).to_list()
        points = []
        for researcher in researchers:
            points.append([researcher.full_name, {"value": researcher.openalex_meta["works_count"],
                                                  "$nexus": {"type": EntityType.RESEARCHER, "id": researcher.uuid}}])
        #     TODO limit could be dynamic
        # TODO maybe set color?
        points = list(reversed(sorted(points, key=lambda row: row[-1]["value"])))[:20]
        result.add("researchers", Series(data=points, entity_type=EntityType.RESEARCHER))
        return result


class SummaryChart(Chart):
    identifier = "basic_stats"
    name = "Summary chart"
    type = ChartType.MIXED
    chart_template = ChartTemplates.MARKDOWN
    generator = create_basic_generator(["researchers", "institutions", "works"])

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        works_query = chart_input.get_series_query("works")
        researcher_query = chart_input.get_series_query("researchers")
        institution_query = chart_input.get_series_query("institutions")

        works = await Work.find(works_query, nesting_depth=2, fetch_links=True).to_list()
        works_df = pd.DataFrame([w.model_dump() for w in works])
        highest_keywords = works_df.explode("keywords")["keywords"].value_counts().head(3)

        researchers = await Researcher.find(researcher_query, nesting_depth=2, fetch_links=True).to_list()
        researchers_df = pd.DataFrame([r.model_dump() for r in researchers])
        researchers_df["works_count"] = researchers_df["openalex_meta"].apply(lambda meta: meta["works_count"] if meta is not None else None)
        highest_researchers = researchers_df.iloc[researchers_df["works_count"].sort_values(ascending=False).head(3).index]
        highest_researchers = [f"<a href=\"/researchers/{r['uuid']}\" target=\"_blank\">{r['full_name']}</a>" for r in highest_researchers.to_dict(orient="records")]

        researchers_df["h_index"] = researchers_df["openalex_meta"].apply(lambda meta: meta["summary_stats"]["h_index"] if meta is not None else None)
        highest_h_score = researchers_df.iloc[researchers_df["h_index"].idxmax()]

        institutions = await Institution.find(institution_query, nesting_depth=2, fetch_links=True).to_list()

        works_md = f"""
### Works
**Total count:** {len(works)}

**Most used keywords:** {", ".join(highest_keywords.index)}
        """
        result.add("works", Series(data=works_md, entity_type=EntityType.WORK))
        researchers_md = f"""
### Researchers
**Total count:** {len(researchers)}

**Most publications:** {", ".join(highest_researchers)}

**Highest H-Index:** <a href=\"/researchers/{highest_h_score['uuid']}\" target=\"_blank\">{highest_h_score['full_name']}</a> ({highest_h_score["h_index"]})
        """
        result.add("researchers", Series(data=researchers_md, entity_type=EntityType.RESEARCHER))
        institutions_md = f"""
### Institutions
**Total count:** {len(institutions)}
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

        institutions = await Institution.find(institution_query, nesting_depth=2, fetch_links=True).to_list()
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

        works = await Work.find(work_query, nesting_depth=2, fetch_links=True).to_list()
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

        works = await Work.find(work_query, Not(Work.publication_date == None), nesting_depth=2,
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

        works = await Work.find(work_query, Not(Work.publication_year == None), fetch_links=True, nesting_depth=2).to_list()
        if len(works) > 0:
            works_df = pd.DataFrame([i.model_dump() for i in works])
            works_df["dblp_type"] = works_df["type"].apply(lambda inst: inst.get("dblp"))
            works_df["openalex_type"] = works_df["type"].apply(lambda inst: inst.get("openalex"))

            grouped = works_df.groupby(['publication_year', field_name]).size().unstack(fill_value=0)

            data = grouped.to_dict(orient='list')

            years = grouped.index.tolist()
        else:
            data = []
            years = []

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

        works = await Work.find(work_query, Not(Work.keywords == None), nesting_depth=2, fetch_links=True).to_list()
        df = pd.DataFrame([i.model_dump() for i in works])

        df = df.explode("keywords")
        grouped = df.groupby(["keywords"])
        count_df = grouped.count().rename(columns={"uuid": "weight"})
        data = count_df[["weight"]].to_dict(orient='index')
        result.add("works", Series(data=data, entity_type=EntityType.WORK))
        return result


"""class PackedKeywordsBubbleChart(Chart):
    identifier = "packed_keywords_bubble_chart"
    name = "Top-10 Keywords Researchers (Bubble)"
    type = ChartType.MIXED
    chart_template = ChartTemplates.HIGHCHARTS
    generator = read_generator("packedKeywordsBubbleChart.js")

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        work_query = chart_input.get_series_query("works")

        works = await Work.find(work_query, Not(Work.keywords == None), nesting_depth=2, fetch_links=True).to_list()
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
"""
