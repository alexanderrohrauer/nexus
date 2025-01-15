from app.visualizations.institution import InstitutionCurrentResearchers
from app.visualizations.mixed import InstitutionsMap, WorksGeoHeatmap, \
    TopResearcherWorksCount, BasicStats, MixedInstitutionAggregation, MixedWorkAggregation, MixedResearchActivity, \
    MixedActivityYearsTypes, KeywordCloud, PackedKeywordsBubbleChart
from app.visualizations.researcher import ResearcherAffiliations, ResearcherPerformance, ResearcherRelationGraph, \
    ResearcherActivity
from app.visualizations.work import WorkAuthors

CHARTS = [
    # Mixed
    # ResearcherEdgeBundling,
    InstitutionsMap,
    WorksGeoHeatmap,
    TopResearcherWorksCount,
    BasicStats,
    MixedInstitutionAggregation,
    MixedWorkAggregation,
    MixedResearchActivity,
    MixedActivityYearsTypes,
    KeywordCloud,
    PackedKeywordsBubbleChart,
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
