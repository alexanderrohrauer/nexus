from app.visualizations.institution import InstitutionCurrentResearchers
from app.visualizations.mixed import ResearcherEdgeBundling, InstitutionsMap, Bubble, WorksGeoHeatmap, \
    TopResearcherWorksCount, BasicStats
from app.visualizations.researcher import ResearcherAffiliations
from app.visualizations.work import WorkAuthors

CHARTS = [
    # Mixed
    ResearcherEdgeBundling,
    InstitutionsMap,
    Bubble,
    WorksGeoHeatmap,
    TopResearcherWorksCount,
    BasicStats,
    # Works
    WorkAuthors,
    # Researchers
    ResearcherAffiliations,
    # Institutions
    InstitutionCurrentResearchers
]
