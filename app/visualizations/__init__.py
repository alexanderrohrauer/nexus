from app.visualizations.institution import InstitutionCurrentResearchers
from app.visualizations.mixed import ResearcherEdgeBundling, InstitutionsMap, Bubble, WorksGeoHeatmap, \
    TopResearcherWorksCount, BasicStats, MixedInstitutionAggregation, MixedWorkAggregation, MixedResearchActivity
from app.visualizations.researcher import ResearcherAffiliations, ResearcherPerformance, ResearcherRelationGraph, \
    ResearcherActivity
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
    MixedResearchActivity,
    # Works
    WorkAuthors,
    # Researchers
    ResearcherAffiliations,
    ResearcherPerformance,
    ResearcherRelationGraph,
    ResearcherActivity,
    # Institutions
    InstitutionCurrentResearchers
]
