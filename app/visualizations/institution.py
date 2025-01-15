from beanie import PydanticObjectId

from app.models import Researcher
from app.utils.visualization_utils import Chart, ChartType, ChartTemplates, ChartInput, SeriesMap, \
    create_basic_generator, EntityType, Series


class InstitutionCurrentResearchers(Chart):
    identifier = "institution_current_researchers"
    name = "Current researchers"
    type = ChartType.INSTITUTION
    chart_template = ChartTemplates.CUSTOM
    generator = create_basic_generator(["researchers"])

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("researchers")
        institution = chart_input.institution
        researchers = await Researcher.find(query, Researcher.institution.id == PydanticObjectId(institution.id), fetch_links=True, nesting_depth=2).to_list()

        result.add("researchers", Series(data=researchers, entity_type=EntityType.RESEARCHER))
        return result
