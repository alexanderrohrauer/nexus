from app.visualizations.institution import InstitutionCurrentResearchers
from app.visualizations.mixed import ResearcherEdgeBundling, InstitutionsMap, Bubble, WorksGeoHeatmap, \
    TopResearcherWorksCount, BasicStats, MixedInstitutionAggregation, MixedWorkAggregation
from app.visualizations.researcher import ResearcherAffiliations, ResearcherPerformance, ResearcherRelationGraph
from app.visualizations.work import WorkAuthors

CHARTS = [
    # Mixed
    ResearcherEdgeBundling,
    InstitutionsMap,
    Bubble,
    WorksGeoHeatmap,
    TopResearcherWorksCount,
    BasicStats,
    MixedInstitutionAggregation,
    MixedWorkAggregation,
    # Works
    WorkAuthors,
    # Researchers
    ResearcherAffiliations,
    ResearcherPerformance,
    ResearcherRelationGraph,
    # Institutions
    InstitutionCurrentResearchers
]
