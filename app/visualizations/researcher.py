from beanie.odm.operators.find.comparison import In

from app.models import Affiliation
from app.utils.visualization_utils import Chart, ChartType, ChartTemplates, ChartInput, SeriesMap, \
    create_basic_generator, EntityType, Series


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
        affiliations = await Affiliation.find(query, In(Affiliation.id, ids), fetch_links=True, nesting_depth=3).to_list()

        result.add("affiliations", Series(data=affiliations, entity_type=EntityType.AFFILIATIONS))
        return result
