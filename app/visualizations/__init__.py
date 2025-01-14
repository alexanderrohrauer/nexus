from app.visualizations.institution import InstitutionCurrentResearchers
from app.visualizations.mixed import ResearcherEdgeBundling, InstitutionsMap, WorksGeoHeatmap, \
    TopResearcherWorksCount, BasicStats, MixedInstitutionAggregation, MixedWorkAggregation, MixedResearchActivity, \
    MixedActivityYearsTypes, KeywordCloud
from app.visualizations.researcher import ResearcherAffiliations, ResearcherPerformance, ResearcherRelationGraph, \
    ResearcherActivity
from app.visualizations.work import WorkAuthors

CHARTS = [
    # Mixed
    ResearcherEdgeBundling,
    InstitutionsMap,
    WorksGeoHeatmap,
    TopResearcherWorksCount,
    BasicStats,
    MixedInstitutionAggregation,
    MixedWorkAggregation,
    MixedResearchActivity,
    MixedActivityYearsTypes,
    KeywordCloud,
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
