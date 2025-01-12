from beanie.odm.operators.find.comparison import In

from app.models import Researcher
from app.utils.visualization_utils import Chart, ChartType, ChartTemplates, ChartInput, SeriesMap, \
    create_basic_generator, EntityType, Series


class WorkAuthors(Chart):
    identifier = "work_authors"
    name = "Authors"
    type = ChartType.WORK
    chart_template = ChartTemplates.CUSTOM
    generator = create_basic_generator(["authors"])

    async def get_series(self, chart_input: ChartInput) -> SeriesMap:
        result = SeriesMap()
        query = chart_input.get_series_query("authors")
        work = chart_input.work
        ids = [a.ref.id for a in work.authors] if work.authors is not None else []
        researchers = await Researcher.find(query, In(Researcher.id, ids), fetch_links=True, nesting_depth=3).to_list()

        result.add("authors", Series(data=researchers, entity_type=EntityType.RESEARCHER))
        return result
