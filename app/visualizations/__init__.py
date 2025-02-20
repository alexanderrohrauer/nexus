from app.visualizations.institution import InstitutionCurrentResearchers
from app.visualizations.mixed import InstitutionsMap, WorksGeoHeatmap, \
    TopResearcherWorksCount, SummaryChart, MixedInstitutionAggregation, MixedWorkAggregation, MixedResearchActivity, \
    MixedActivityYearsTypes, KeywordCloud, ResearcherMap
from app.visualizations.researcher import ResearcherAffiliations, ResearcherPerformance, ResearcherRelationGraph
from app.visualizations.work import WorkAuthors

CHARTS = [
    # Mixed
    # ResearcherEdgeBundling,
    InstitutionsMap,
    WorksGeoHeatmap,
    TopResearcherWorksCount,
    SummaryChart,
    MixedInstitutionAggregation,
    MixedWorkAggregation,
    MixedResearchActivity,
    MixedActivityYearsTypes,
    KeywordCloud,
    # PackedKeywordsBubbleChart,
    ResearcherMap,
    # Works
    WorkAuthors,
    # Researchers
    ResearcherAffiliations,
    ResearcherPerformance,
    ResearcherRelationGraph,
    # ResearcherActivity,
    # Institutions
    InstitutionCurrentResearchers
]
