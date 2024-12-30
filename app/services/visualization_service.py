from itertools import combinations
from uuid import UUID

import pydash as _
from beanie.odm.operators.find.logical import Not
from fastapi import HTTPException

from app.dtos.visualizations import VisualizationData
from app.models import Dashboard, Work, Institution
from app.utils.visualization_utils import ChartInput
from app.visualizations import CHARTS

# TODO remove
# mock_data =  {
#     "vis-1":[
#         {
#             "$schema": "https://vega.github.io/schema/vega/v5.json",
#             "description": "A basic line chart example.",
#             "data": [
#                 {
#                     "name": "table"
#                 }
#             ],
#
#             "scales": [
#                 {
#                     "name": "x",
#                     "type": "point",
#                     "range": "width",
#                     "domain": {"data": "table", "field": "x"}
#                 },
#                 {
#                     "name": "y",
#                     "type": "linear",
#                     "range": "height",
#                     "nice": True,
#                     "zero": True,
#                     "domain": {"data": "table", "field": "y"}
#                 },
#                 {
#                     "name": "color",
#                     "type": "ordinal",
#                     "range": "category",
#                     "domain": {"data": "table", "field": "c"}
#                 }
#             ],
#
#             "axes": [
#                 {"orient": "bottom", "scale": "x"},
#                 {"orient": "left", "scale": "y"}
#             ],
#
#             "marks": [
#                 {
#                     "type": "group",
#                     "from": {
#                         "facet": {
#                             "name": "series",
#                             "data": "table",
#                             "groupby": "c"
#                         }
#                     },
#                     "marks": [
#                         {
#                             "type": "line",
#                             "from": {"data": "series"},
#                             "encode": {
#                                 "enter": {
#                                     "x": {"scale": "x", "field": "x"},
#                                     "y": {"scale": "y", "field": "y"},
#                                     "stroke": {"scale": "color", "field": "c"},
#                                     "strokeWidth": {"value": 2}
#                                 },
#                                 "update": {
#                                     "interpolate": {"value": "linear"},
#                                     "strokeOpacity": {"value": 1}
#                                 },
#                                 "hover": {
#                                     "strokeOpacity": {"value": 0.5}
#                                 }
#                             }
#                         }
#                     ]
#                 }
#             ]
#         },
#         {
#             "table": [
#                 {"x": 0, "y": 28, "c":0}, {"x": 0, "y": 20, "c":1},
#                 {"x": 1, "y": 43, "c":0}, {"x": 1, "y": 35, "c":1},
#                 {"x": 2, "y": 81, "c":0}, {"x": 2, "y": 10, "c":1},
#                 {"x": 3, "y": 19, "c":0}, {"x": 3, "y": 15, "c":1},
#                 {"x": 4, "y": 52, "c":0}, {"x": 4, "y": 48, "c":1},
#                 {"x": 5, "y": 24, "c":0}, {"x": 5, "y": 28, "c":1},
#                 {"x": 6, "y": 87, "c":0}, {"x": 6, "y": 66, "c":1},
#                 {"x": 7, "y": 17, "c":0}, {"x": 7, "y": 27, "c":1},
#                 {"x": 8, "y": 68, "c":0}, {"x": 8, "y": 16, "c":1},
#                 {"x": 9, "y": 49, "c":0}, {"x": 9, "y": 25, "c":1}
#             ]
#         }
#     ],
#     "vis-2": [
#         {
#             "$schema": "https://vega.github.io/schema/vega/v5.json",
#             "description": "A basic bar chart example, with value labels shown upon pointer hover.",
#             "data": [
#                 {
#                     "name": "table",
#                 }
#             ],
#
#             "signals": [
#                 {
#                     "name": "tooltip",
#                     "value": {},
#                     "on": [
#                         {"events": "rect:pointerover", "update": "datum"},
#                         {"events": "rect:pointerout",  "update": "{}"}
#                     ]
#                 }
#             ],
#
#             "scales": [
#                 {
#                     "name": "xscale",
#                     "type": "band",
#                     "domain": {"data": "table", "field": "category"},
#                     "range": "width",
#                     "padding": 0.05,
#                     "round": True
#                 },
#                 {
#                     "name": "yscale",
#                     "domain": {"data": "table", "field": "amount"},
#                     "nice": True,
#                     "range": "height"
#                 }
#             ],
#
#             "axes": [
#                 { "orient": "bottom", "scale": "xscale" },
#                 { "orient": "left", "scale": "yscale" }
#             ],
#
#             "marks": [
#                 {
#                     "type": "rect",
#                     "from": {"data":"table"},
#                     "encode": {
#                         "enter": {
#                             "x": {"scale": "xscale", "field": "category"},
#                             "width": {"scale": "xscale", "band": 1},
#                             "y": {"scale": "yscale", "field": "amount"},
#                             "y2": {"scale": "yscale", "value": 0}
#                         },
#                         "update": {
#                             "fill": {"value": "steelblue"}
#                         },
#                         "hover": {
#                             "fill": {"value": "red"}
#                         }
#                     }
#                 },
#                 {
#                     "type": "text",
#                     "encode": {
#                         "enter": {
#                             "align": {"value": "center"},
#                             "baseline": {"value": "bottom"},
#                             "fill": {"value": "#333"}
#                         },
#                         "update": {
#                             "x": {"scale": "xscale", "signal": "tooltip.category", "band": 0.5},
#                             "y": {"scale": "yscale", "signal": "tooltip.amount", "offset": -2},
#                             "text": {"signal": "tooltip.amount"},
#                             "fillOpacity": [
#                                 {"test": "datum === tooltip", "value": 0},
#                                 {"value": 1}
#                             ]
#                         }
#                     }
#                 }
#             ]
#         },
#         {
#             "table": [
#                 {"category": "A", "amount": 28},
#                 {"category": "B", "amount": 55},
#                 {"category": "C", "amount": 43},
#                 {"category": "D", "amount": 91},
#                 {"category": "E", "amount": 81},
#                 {"category": "F", "amount": 53},
#                 {"category": "G", "amount": 19},
#                 {"category": "H", "amount": 87}
#             ]
#         }
#     ],
#     "vis-3": [
#         {
#             "$schema": "https://vega.github.io/schema/vega/v5.json",
#             "description": "A word cloud visualization depicting Vega research paper abstracts.",
#             "data": [
#                 {
#                     "name": "table",
#                     "transform": [
#                         {
#                             "type": "countpattern",
#                             "field": "data",
#                             "case": "upper",
#                             "pattern": "[\\w']{3,}",
#                             "stopwords": "(i|me|my|myself|we|us|our|ours|ourselves|you|your|yours|yourself|yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|what|which|who|whom|whose|this|that|these|those|am|is|are|was|were|be|been|being|have|has|had|having|do|does|did|doing|will|would|should|can|could|ought|i'm|you're|he's|she's|it's|we're|they're|i've|you've|we've|they've|i'd|you'd|he'd|she'd|we'd|they'd|i'll|you'll|he'll|she'll|we'll|they'll|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|doesn't|don't|didn't|won't|wouldn't|shan't|shouldn't|can't|cannot|couldn't|mustn't|let's|that's|who's|what's|here's|there's|when's|where's|why's|how's|a|an|the|and|but|if|or|because|as|until|while|of|at|by|for|with|about|against|between|into|through|during|before|after|above|below|to|from|up|upon|down|in|out|on|off|over|under|again|further|then|once|here|there|when|where|why|how|all|any|both|each|few|more|most|other|some|such|no|nor|not|only|own|same|so|than|too|very|say|says|said|shall)"
#                         },
#                         {
#                             "type": "formula", "as": "angle",
#                             "expr": "[-45, 0, 45][~~(random() * 3)]"
#                         },
#                         {
#                             "type": "formula", "as": "weight",
#                             "expr": "if(datum.text=='VEGA', 600, 300)"
#                         }
#                     ]
#                 }
#             ],
#
#             "scales": [
#                 {
#                     "name": "color",
#                     "type": "ordinal",
#                     "domain": {"data": "table", "field": "text"},
#                     "range": ["#d5a928", "#652c90", "#939597"]
#                 }
#             ],
#
#             "marks": [
#                 {
#                     "type": "text",
#                     "from": {"data": "table"},
#                     "encode": {
#                         "enter": {
#                             "text": {"field": "text"},
#                             "align": {"value": "center"},
#                             "baseline": {"value": "alphabetic"},
#                             "fill": {"scale": "color", "field": "text"}
#                         },
#                         "update": {
#                             "fillOpacity": {"value": 1}
#                         },
#                         "hover": {
#                             "fillOpacity": {"value": 0.5}
#                         }
#                     },
#                     "transform": [
#                         {
#                             "type": "wordcloud",
#                             "text": {"field": "text"},
#                             "rotate": {"field": "datum.angle"},
#                             "font": "Helvetica Neue, Arial",
#                             "fontSize": {"field": "datum.count"},
#                             "fontWeight": {"field": "datum.weight"},
#                             "fontSizeRange": [12, 56],
#                             "padding": 2
#                         }
#                     ]
#                 }
#             ]
#         },
#         {
#             "table": [
#                 "Declarative visualization grammars can accelerate development, facilitate retargeting across platforms, and allow language-level optimizations. However, existing declarative visualization languages are primarily concerned with visual encoding, and rely on imperative event handlers for interactive behaviors. In response, we introduce a model of declarative interaction design for data visualizations. Adopting methods from reactive programming, we model low-level events as composable data streams from which we form higher-level semantic signals. Signals feed predicates and scale inversions, which allow us to generalize interactive selections at the level of item geometry (pixels) into interactive queries over the data domain. Production rules then use these queries to manipulate the visualization’s appearance. To facilitate reuse and sharing, these constructs can be encapsulated as named interactors: standalone, purely declarative specifications of interaction techniques. We assess our model’s feasibility and expressivity by instantiating it with extensions to the Vega visualization grammar. Through a diverse range of examples, we demonstrate coverage over an established taxonomy of visualization interaction techniques.",
#                 "We present Reactive Vega, a system architecture that provides the first robust and comprehensive treatment of declarative visual and interaction design for data visualization. Starting from a single declarative specification, Reactive Vega constructs a dataflow graph in which input data, scene graph elements, and interaction events are all treated as first-class streaming data sources. To support expressive interactive visualizations that may involve time-varying scalar, relational, or hierarchical data, Reactive Vega’s dataflow graph can dynamically re-write itself at runtime by extending or pruning branches in a data-driven fashion. We discuss both compile- and run-time optimizations applied within Reactive Vega, and share the results of benchmark studies that indicate superior interactive performance to both D3 and the original, non-reactive Vega system.",
#                 "We present Vega-Lite, a high-level grammar that enables rapid specification of interactive data visualizations. Vega-Lite combines a traditional grammar of graphics, providing visual encoding rules and a composition algebra for layered and multi-view displays, with a novel grammar of interaction. Users specify interactive semantics by composing selections. In Vega-Lite, a selection is an abstraction that defines input event processing, points of interest, and a predicate function for inclusion testing. Selections parameterize visual encodings by serving as input data, defining scale extents, or by driving conditional logic. The Vega-Lite compiler automatically synthesizes requisite data flow and event handling logic, which users can override for further customization. In contrast to existing reactive specifications, Vega-Lite selections decompose an interaction design into concise, enumerable semantic units. We evaluate Vega-Lite through a range of examples, demonstrating succinct specification of both customized interaction methods and common techniques such as panning, zooming, and linked selection."
#             ],
#         }
#     ]
# }

mock_data = {
    "vis-1": [
        {
            "title": {
                "text": 'My chart'
            },
            "series": [{
                "data": [1, 2, 3]
            }],
        },
        []
    ],
    "vis-2": [
        {
            "chart": {
                "type": 'packedbubble'
            },
            "series": [{
                "data": [50, 12, 33, 45, 60]
            }]
        },
        []
    ],
    "vis-3": [
        {
            "chart": {
                "type": "packedbubble",
                "height": "100%"
            },
            "title": {
                "text": "Carbon emissions around the world (2022)",
                "align": "left"
            },
            "subtitle": {
                "text": "Source: <a href=\"https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions\" target=\"_blank\">Wikipedia</a>",
                "align": "left"
            },
            "tooltip": {
                "useHTML": True,
                "pointFormat": "<b>{point.name}:</b> {point.value}m CO<sub>2</sub>"
            },
            "plotOptions": {
                "packedbubble": {
                    "minSize": "20%",
                    "maxSize": "100%",
                    "zMin": 0,
                    "zMax": 1000,
                    "layoutAlgorithm": {
                        "gravitationalConstant": 0.05,
                        "splitSeries": True,
                        "seriesInteraction": False,
                        "dragBetweenSeries": True,
                        "parentNodeLimit": True
                    },
                    "dataLabels": {
                        "enabled": True,
                        "format": "{point.name}",
                        "filter": {
                            "property": "y",
                            "operator": ">",
                            "value": 250
                        }
                    }
                }
            },
            "series": [
                {
                    "name": "Europe",
                    "data": [
                        {
                            "name": "Germany",
                            "value": 673.6
                        },
                        {
                            "name": "Croatia",
                            "value": 17.2
                        },
                        {
                            "name": "Belgium",
                            "value": 90.4
                        },
                        {
                            "name": "Czech Republic",
                            "value": 111.5
                        },
                        {
                            "name": "Netherlands",
                            "value": 134.7
                        },
                        {
                            "name": "Spain",
                            "value": 254.4
                        },
                        {
                            "name": "Ukraine",
                            "value": 132.5
                        },
                        {
                            "name": "Poland",
                            "value": 322
                        },
                        {
                            "name": "France",
                            "value": 315.5
                        },
                        {
                            "name": "Romania",
                            "value": 77.3
                        },
                        {
                            "name": "United Kingdom",
                            "value": 340.6
                        },
                        {
                            "name": "Turkey",
                            "value": 481.2
                        },
                        {
                            "name": "Italy",
                            "value": 322.9
                        },
                        {
                            "name": "Greece",
                            "value": 56.8
                        },
                        {
                            "name": "Austria",
                            "value": 61.2
                        },
                        {
                            "name": "Belarus",
                            "value": 57.4
                        },
                        {
                            "name": "Serbia",
                            "value": 56.9
                        },
                        {
                            "name": "Finland",
                            "value": 37.3
                        },
                        {
                            "name": "Bulgaria",
                            "value": 50.1
                        },
                        {
                            "name": "Portugal",
                            "value": 41.3
                        },
                        {
                            "name": "Norway",
                            "value": 42.2
                        },
                        {
                            "name": "Sweden",
                            "value": 37.8
                        },
                        {
                            "name": "Hungary",
                            "value": 47.3
                        },
                        {
                            "name": "Switzerland",
                            "value": 36.1
                        },
                        {
                            "name": "Denmark",
                            "value": 29.2
                        },
                        {
                            "name": "Slovakia",
                            "value": 35.2
                        },
                        {
                            "name": "Ireland",
                            "value": 37.8
                        },
                        {
                            "name": "Croatia",
                            "value": 17.2
                        },
                        {
                            "name": "Estonia",
                            "value": 10.8
                        },
                        {
                            "name": "Slovenia",
                            "value": 13.9
                        },
                        {
                            "name": "Lithuania",
                            "value": 13.3
                        },
                        {
                            "name": "Luxembourg",
                            "value": 7.6
                        },
                        {
                            "name": "Macedonia",
                            "value": 8.3
                        },
                        {
                            "name": "Moldova",
                            "value": 8.7
                        },
                        {
                            "name": "Latvia",
                            "value": 6.7
                        },
                        {
                            "name": "Cyprus",
                            "value": 7.5
                        }
                    ]
                },
                {
                    "name": "Africa",
                    "data": [
                        {
                            "name": "Senegal",
                            "value": 12.1
                        },
                        {
                            "name": "Cameroon",
                            "value": 10.1
                        },
                        {
                            "name": "Zimbabwe",
                            "value": 10.2
                        },
                        {
                            "name": "Ghana",
                            "value": 24.5
                        },
                        {
                            "name": "Kenya",
                            "value": 21.5
                        },
                        {
                            "name": "Sudan",
                            "value": 24.5
                        },
                        {
                            "name": "Tunisia",
                            "value": 35.9
                        },
                        {
                            "name": "Angola",
                            "value": 20.2
                        },
                        {
                            "name": "Libya",
                            "value": 62.7
                        },
                        {
                            "name": "Ivory Coast",
                            "value": 14.5
                        },
                        {
                            "name": "Morocco",
                            "value": 72.6
                        },
                        {
                            "name": "Ethiopia",
                            "value": 21.1
                        },
                        {
                            "name": "United Republic of Tanzania",
                            "value": 17
                        },
                        {
                            "name": "Nigeria",
                            "value": 122.8
                        },
                        {
                            "name": "South Africa",
                            "value": 405
                        },
                        {
                            "name": "Egypt",
                            "value": 266
                        },
                        {
                            "name": "Algeria",
                            "value": 177.1
                        }
                    ]
                },
                {
                    "name": "Oceania",
                    "data": [
                        {
                            "name": "Australia",
                            "value": 393.2
                        },
                        {
                            "name": "New Zealand",
                            "value": 32.4
                        },
                        {
                            "name": "Papua New Guinea",
                            "value": 4.7
                        }
                    ]
                },
                {
                    "name": "North America",
                    "data": [
                        {
                            "name": "Costa Rica",
                            "value": 8.6
                        },
                        {
                            "name": "Honduras",
                            "value": 10.6
                        },
                        {
                            "name": "Jamaica",
                            "value": 6.1
                        },
                        {
                            "name": "Panama",
                            "value": 11.4
                        },
                        {
                            "name": "Guatemala",
                            "value": 20.1
                        },
                        {
                            "name": "Dominican Republic",
                            "value": 23.5
                        },
                        {
                            "name": "Cuba",
                            "value": 24.8
                        },
                        {
                            "name": "USA",
                            "value": 4853.8
                        },
                        {
                            "name": "Canada",
                            "value": 582.1
                        },
                        {
                            "name": "Mexico",
                            "value": 487.8
                        }
                    ]
                },
                {
                    "name": "South America",
                    "data": [
                        {
                            "name": "El Salvador",
                            "value": 8
                        },
                        {
                            "name": "Uruguay",
                            "value": 8.5
                        },
                        {
                            "name": "Bolivia",
                            "value": 22
                        },
                        {
                            "name": "Trinidad and Tobago",
                            "value": 29.2
                        },
                        {
                            "name": "Ecuador",
                            "value": 46.1
                        },
                        {
                            "name": "Chile",
                            "value": 92.9
                        },
                        {
                            "name": "Peru",
                            "value": 61.6
                        },
                        {
                            "name": "Colombia",
                            "value": 88.5
                        },
                        {
                            "name": "Brazil",
                            "value": 466.8
                        },
                        {
                            "name": "Argentina",
                            "value": 184
                        },
                        {
                            "name": "Venezuela",
                            "value": 96.9
                        }
                    ]
                },
                {
                    "name": "Asia",
                    "data": [
                        {
                            "name": "Nepal",
                            "value": 15.8
                        },
                        {
                            "name": "Georgia",
                            "value": 12
                        },
                        {
                            "name": "Brunei Darussalam",
                            "value": 9.4
                        },
                        {
                            "name": "Kyrgyzstan",
                            "value": 10.3
                        },
                        {
                            "name": "Afghanistan",
                            "value": 5.7
                        },
                        {
                            "name": "Myanmar",
                            "value": 37.4
                        },
                        {
                            "name": "Mongolia",
                            "value": 22.1
                        },
                        {
                            "name": "Sri Lanka",
                            "value": 18.5
                        },
                        {
                            "name": "Bahrain",
                            "value": 38
                        },
                        {
                            "name": "Yemen",
                            "value": 12.3
                        },
                        {
                            "name": "Jordan",
                            "value": 23.6
                        },
                        {
                            "name": "Lebanon",
                            "value": 23.8
                        },
                        {
                            "name": "Azerbaijan",
                            "value": 37.1
                        },
                        {
                            "name": "Singapore",
                            "value": 53.4
                        },
                        {
                            "name": "Hong Kong",
                            "value": 32.4
                        },
                        {
                            "name": "Syria",
                            "value": 28.2
                        },
                        {
                            "name": "DPR Korea",
                            "value": 54.4
                        },
                        {
                            "name": "Israel",
                            "value": 61.8
                        },
                        {
                            "name": "Turkmenistan",
                            "value": 69.9
                        },
                        {
                            "name": "Oman",
                            "value": 91.6
                        },
                        {
                            "name": "Qatar",
                            "value": 102.6
                        },
                        {
                            "name": "Philippines",
                            "value": 155.4
                        },
                        {
                            "name": "Kuwait",
                            "value": 110.1
                        },
                        {
                            "name": "Uzbekistan",
                            "value": 132.4
                        },
                        {
                            "name": "Iraq",
                            "value": 193.8
                        },
                        {
                            "name": "Pakistan",
                            "value": 199.3
                        },
                        {
                            "name": "Vietnam",
                            "value": 327.9
                        },
                        {
                            "name": "United Arab Emirates",
                            "value": 218.8
                        },
                        {
                            "name": "Malaysia",
                            "value": 277.5
                        },
                        {
                            "name": "Kazakhstan",
                            "value": 245.9
                        },
                        {
                            "name": "Thailand",
                            "value": 282.4
                        },
                        {
                            "name": "Taiwan",
                            "value": 275.6
                        },
                        {
                            "name": "Indonesia",
                            "value": 692.2
                        },
                        {
                            "name": "Saudi Arabia",
                            "value": 607.9
                        },
                        {
                            "name": "Japan",
                            "value": 1082.6
                        },
                        {
                            "name": "China",
                            "value": 12667.4
                        },
                        {
                            "name": "India",
                            "value": 2693
                        },
                        {
                            "name": "Russia",
                            "value": 1909
                        },
                        {
                            "name": "Iran",
                            "value": 686.4
                        },
                        {
                            "name": "Korea",
                            "value": 635.5
                        }
                    ]
                }
            ]
        },
        []
    ],
    "vis-4": [
        {
            "chart": {
                "type": "networkgraph",
                "height": "100%"
            },
            "title": {
                "text": "Researcher",
                "align": "left"
            },
            "plotOptions": {
                "networkgraph": {
                    "keys": [
                        "from",
                        "to"
                    ],
                    "layoutAlgorithm": {
                        "enableSimulation": True,
                        "friction": -0.9,
                        "repulsion": 200,
                        "linkLength": 20
                    },
                    "marker": {
                        "radius": 8
                    }
                }
            },
            "series": [
                {
                    "accessibility": {
                        "enabled": False
                    },
                    "dataLabels": {
                        "enabled": True,
                        "linkFormat": "",
                        "style": {
                            "fontSize": "0.8em",
                            "fontWeight": "normal"
                        }
                    },
                    "id": "lang-tree",
                    "data": [
                        [
                            "Proto Indo-European",
                            "Balto-Slavic"
                        ],
                        [
                            "Proto Indo-European",
                            "Germanic"
                        ],
                        [
                            "Proto Indo-European",
                            "Celtic"
                        ],
                        [
                            "Proto Indo-European",
                            "Italic"
                        ],
                        [
                            "Proto Indo-European",
                            "Hellenic"
                        ],
                        [
                            "Proto Indo-European",
                            "Anatolian"
                        ],
                        [
                            "Proto Indo-European",
                            "Indo-Iranian"
                        ],
                        [
                            "Proto Indo-European",
                            "Tocharian"
                        ],
                        [
                            "Indo-Iranian",
                            "Dardic"
                        ],
                        [
                            "Indo-Iranian",
                            "Indic"
                        ],
                        [
                            "Indo-Iranian",
                            "Iranian"
                        ],
                        [
                            "Iranian",
                            "Old Persian"
                        ],
                        [
                            "Old Persian",
                            "Middle Persian"
                        ],
                        [
                            "Indic",
                            "Sanskrit"
                        ],
                        [
                            "Italic",
                            "Osco-Umbrian"
                        ],
                        [
                            "Italic",
                            "Latino-Faliscan"
                        ],
                        [
                            "Latino-Faliscan",
                            "Latin"
                        ],
                        [
                            "Celtic",
                            "Brythonic"
                        ],
                        [
                            "Celtic",
                            "Goidelic"
                        ],
                        [
                            "Germanic",
                            "North Germanic"
                        ],
                        [
                            "Germanic",
                            "West Germanic"
                        ],
                        [
                            "Germanic",
                            "East Germanic"
                        ],
                        [
                            "North Germanic",
                            "Old Norse"
                        ],
                        [
                            "North Germanic",
                            "Old Swedish"
                        ],
                        [
                            "North Germanic",
                            "Old Danish"
                        ],
                        [
                            "West Germanic",
                            "Old English"
                        ],
                        [
                            "West Germanic",
                            "Old Frisian"
                        ],
                        [
                            "West Germanic",
                            "Old Dutch"
                        ],
                        [
                            "West Germanic",
                            "Old Low German"
                        ],
                        [
                            "West Germanic",
                            "Old High German"
                        ],
                        [
                            "Old Norse",
                            "Old Icelandic"
                        ],
                        [
                            "Old Norse",
                            "Old Norwegian"
                        ],
                        [
                            "Old Norwegian",
                            "Middle Norwegian"
                        ],
                        [
                            "Old Swedish",
                            "Middle Swedish"
                        ],
                        [
                            "Old Danish",
                            "Middle Danish"
                        ],
                        [
                            "Old English",
                            "Middle English"
                        ],
                        [
                            "Old Dutch",
                            "Middle Dutch"
                        ],
                        [
                            "Old Low German",
                            "Middle Low German"
                        ],
                        [
                            "Old High German",
                            "Middle High German"
                        ],
                        [
                            "Balto-Slavic",
                            "Baltic"
                        ],
                        [
                            "Balto-Slavic",
                            "Slavic"
                        ],
                        [
                            "Slavic",
                            "East Slavic"
                        ],
                        [
                            "Slavic",
                            "West Slavic"
                        ],
                        [
                            "Slavic",
                            "South Slavic"
                        ],
                        [
                            "Proto Indo-European",
                            "Phrygian"
                        ],
                        [
                            "Proto Indo-European",
                            "Armenian"
                        ],
                        [
                            "Proto Indo-European",
                            "Albanian"
                        ],
                        [
                            "Proto Indo-European",
                            "Thracian"
                        ],
                        [
                            "Tocharian",
                            "Tocharian A"
                        ],
                        [
                            "Tocharian",
                            "Tocharian B"
                        ],
                        [
                            "Anatolian",
                            "Hittite"
                        ],
                        [
                            "Anatolian",
                            "Palaic"
                        ],
                        [
                            "Anatolian",
                            "Luwic"
                        ],
                        [
                            "Anatolian",
                            "Lydian"
                        ],
                        [
                            "Iranian",
                            "Balochi"
                        ],
                        [
                            "Iranian",
                            "Kurdish"
                        ],
                        [
                            "Iranian",
                            "Pashto"
                        ],
                        [
                            "Iranian",
                            "Sogdian"
                        ],
                        [
                            "Old Persian",
                            "Pahlavi"
                        ],
                        [
                            "Middle Persian",
                            "Persian"
                        ],
                        [
                            "Hellenic",
                            "Greek"
                        ],
                        [
                            "Dardic",
                            "Dard"
                        ],
                        [
                            "Sanskrit",
                            "Sindhi"
                        ],
                        [
                            "Sanskrit",
                            "Romani"
                        ],
                        [
                            "Sanskrit",
                            "Urdu"
                        ],
                        [
                            "Sanskrit",
                            "Hindi"
                        ],
                        [
                            "Sanskrit",
                            "Bihari"
                        ],
                        [
                            "Sanskrit",
                            "Assamese"
                        ],
                        [
                            "Sanskrit",
                            "Bengali"
                        ],
                        [
                            "Sanskrit",
                            "Marathi"
                        ],
                        [
                            "Sanskrit",
                            "Gujarati"
                        ],
                        [
                            "Sanskrit",
                            "Punjabi"
                        ],
                        [
                            "Sanskrit",
                            "Sinhalese"
                        ],
                        [
                            "Osco-Umbrian",
                            "Umbrian"
                        ],
                        [
                            "Osco-Umbrian",
                            "Oscan"
                        ],
                        [
                            "Latino-Faliscan",
                            "Faliscan"
                        ],
                        [
                            "Latin",
                            "Portugese"
                        ],
                        [
                            "Latin",
                            "Spanish"
                        ],
                        [
                            "Latin",
                            "French"
                        ],
                        [
                            "Latin",
                            "Romanian"
                        ],
                        [
                            "Latin",
                            "Italian"
                        ],
                        [
                            "Latin",
                            "Catalan"
                        ],
                        [
                            "Latin",
                            "Franco-Provençal"
                        ],
                        [
                            "Latin",
                            "Rhaeto-Romance"
                        ],
                        [
                            "Brythonic",
                            "Welsh"
                        ],
                        [
                            "Brythonic",
                            "Breton"
                        ],
                        [
                            "Brythonic",
                            "Cornish"
                        ],
                        [
                            "Brythonic",
                            "Cuymbric"
                        ],
                        [
                            "Goidelic",
                            "Modern Irish"
                        ],
                        [
                            "Goidelic",
                            "Scottish Gaelic"
                        ],
                        [
                            "Goidelic",
                            "Manx"
                        ],
                        [
                            "East Germanic",
                            "Gothic"
                        ],
                        [
                            "Middle Low German",
                            "Low German"
                        ],
                        [
                            "Middle High German",
                            "(High) German"
                        ],
                        [
                            "Middle High German",
                            "Yiddish"
                        ],
                        [
                            "Middle English",
                            "English"
                        ],
                        [
                            "Middle Dutch",
                            "Hollandic"
                        ],
                        [
                            "Middle Dutch",
                            "Flemish"
                        ],
                        [
                            "Middle Dutch",
                            "Dutch"
                        ],
                        [
                            "Middle Dutch",
                            "Limburgish"
                        ],
                        [
                            "Middle Dutch",
                            "Brabantian"
                        ],
                        [
                            "Middle Dutch",
                            "Rhinelandic"
                        ],
                        [
                            "Old Frisian",
                            "Frisian"
                        ],
                        [
                            "Middle Danish",
                            "Danish"
                        ],
                        [
                            "Middle Swedish",
                            "Swedish"
                        ],
                        [
                            "Middle Norwegian",
                            "Norwegian"
                        ],
                        [
                            "Old Norse",
                            "Faroese"
                        ],
                        [
                            "Old Icelandic",
                            "Icelandic"
                        ],
                        [
                            "Baltic",
                            "Old Prussian"
                        ],
                        [
                            "Baltic",
                            "Lithuanian"
                        ],
                        [
                            "Baltic",
                            "Latvian"
                        ],
                        [
                            "West Slavic",
                            "Polish"
                        ],
                        [
                            "West Slavic",
                            "Slovak"
                        ],
                        [
                            "West Slavic",
                            "Czech"
                        ],
                        [
                            "West Slavic",
                            "Wendish"
                        ],
                        [
                            "East Slavic",
                            "Bulgarian"
                        ],
                        [
                            "East Slavic",
                            "Old Church Slavonic"
                        ],
                        [
                            "East Slavic",
                            "Macedonian"
                        ],
                        [
                            "East Slavic",
                            "Serbo-Croatian"
                        ],
                        [
                            "East Slavic",
                            "Slovene"
                        ],
                        [
                            "South Slavic",
                            "Russian"
                        ],
                        [
                            "South Slavic",
                            "Ukrainian"
                        ],
                        [
                            "South Slavic",
                            "Belarusian"
                        ],
                        [
                            "South Slavic",
                            "Rusyn"
                        ]
                    ]
                }
            ]
        },
        []
    ],
    "vis-5": [
        {
            "tooltip": {
                "headerFormat": "",
                "pointFormat": "{#if (eq 1 point.sets.length)}Product:<br><b>Highcharts {point.sets.0}</b>{else}Products:<br>{#each point.sets}Highcharts <b>{this}</b>{#unless @last} and {/unless}{/each}<br><br>Shared components:<br><b>{point.name}</b><br>{/if}"
            },
            "series": [
                {
                    "type": "venn",
                    "colors": [
                        "rgb(180, 210, 255)",
                        "rgb(180, 255, 210)",
                        "rgb(180, 235, 235)",
                        "rgb(200, 200, 200)",
                        "rgb(170, 230, 250)",
                        "rgb(170, 250, 230)",
                        "rgb(170, 240, 240)",
                        "rgb(190, 190, 190)",
                        "rgb(160, 220, 245)",
                        "rgb(160, 245, 220)"
                    ],
                    "data": [
                        {
                            "sets": [
                                "Core"
                            ],
                            "value": 10,
                            "name": "Highcharts Core",
                            "dataLabels": {
                                "style": {
                                    "fontSize": 15
                                }
                            }
                        },
                        {
                            "sets": [
                                "Stock"
                            ],
                            "value": 3,
                            "dataLabels": {
                                "style": {
                                    "fontSize": 13
                                }
                            }
                        },
                        {
                            "sets": [
                                "Dashboards"
                            ],
                            "value": 3,
                            "dataLabels": {
                                "style": {
                                    "fontSize": 13
                                }
                            }
                        },
                        {
                            "sets": [
                                "Gantt"
                            ],
                            "value": 2.5,
                            "dataLabels": {
                                "style": {
                                    "fontSize": 13
                                }
                            }
                        },
                        {
                            "sets": [
                                "Maps"
                            ],
                            "value": 3,
                            "dataLabels": {
                                "style": {
                                    "fontSize": 13
                                }
                            }
                        },
                        {
                            "sets": [
                                "Gantt",
                                "Maps",
                                "Stock"
                            ],
                            "value": 1,
                            "name": "Core"
                        },
                        {
                            "sets": [
                                "Stock",
                                "Core"
                            ],
                            "value": 1,
                            "name": "DateTime Series and Axis"
                        },
                        {
                            "sets": [
                                "Gantt",
                                "Core"
                            ],
                            "value": 1,
                            "name": "X-range Series and DateTime Axis"
                        },
                        {
                            "sets": [
                                "Maps",
                                "Core"
                            ],
                            "value": 1,
                            "name": "Heatmap and ColorAxis"
                        },
                        {
                            "sets": [
                                "Stock",
                                "Gantt"
                            ],
                            "value": 0.25,
                            "name": "Navigator & RangeSelector"
                        },
                        {
                            "sets": [
                                "Dashboards",
                                "Core"
                            ],
                            "value": 1,
                            "name": "Data Layer"
                        },
                        {
                            "sets": [
                                "Dashboards",
                                "DataGrid"
                            ],
                            "value": 0.5,
                            "name": "DataGrid"
                        },
                        {
                            "sets": [
                                "Dashboards",
                                "KPI"
                            ],
                            "value": 0.5,
                            "name": "KPI"
                        },
                        {
                            "sets": [
                                "DataGrid"
                            ],
                            "value": 0.5,
                            "name": ""
                        },
                        {
                            "sets": [
                                "KPI"
                            ],
                            "value": 0.2,
                            "name": "KPI"
                        },
                        {
                            "sets": [
                                "Custom"
                            ],
                            "value": 2,
                            "name": "Custom component"
                        },
                        {
                            "sets": [
                                "Custom",
                                "Dashboards"
                            ],
                            "value": 0.3,
                            "name": "Sync API"
                        }
                    ],
                    "dataLabels": {
                        "style": {
                            "textOutline": "none"
                        }
                    }
                }
            ],
            "title": {
                "text": "Highsoft products relationships"
            },
            "subtitle": {
                "text": "Highcharts Core, Stock, Maps, Gantt, and Dashboards"
            },
            "accessibility": {
                "point": {
                    "valueDescriptionFormat": "{#if (eq 1 point.sets.length)}Product: Highcharts {point.sets.0}{else}Products: {#each point.sets}Highcharts {this}{#unless @last} and {/unless}{/each}, Shared components: {point.name}{/if}"
                },
                "series": {
                    "describeSingleSeries": True,
                    "descriptionFormat": "Venn diagram with {series.points.length} relations."
                }
            }
        },
        []
    ],
    "vis-6": [
        {
            "accessibility": {
                "screenReaderSection": {
                    "beforeChartFormat": "<h5>{chartTitle}</h5><div>{chartSubtitle}</div><div>{chartLongdesc}</div><div>{viewTableButton}</div>"
                }
            },
            "series": [
                {
                    "type": "wordcloud",
                    "data": [
                        {
                            "name": "Chapter",
                            "weight": 1
                        },
                        {
                            "name": "Down",
                            "weight": 1
                        },
                        {
                            "name": "the",
                            "weight": 8
                        },
                        {
                            "name": "Rabbit-Hole",
                            "weight": 1
                        },
                        {
                            "name": "Alice",
                            "weight": 2
                        },
                        {
                            "name": "was",
                            "weight": 3
                        },
                        {
                            "name": "beginning",
                            "weight": 1
                        },
                        {
                            "name": "to",
                            "weight": 2
                        },
                        {
                            "name": "get",
                            "weight": 1
                        },
                        {
                            "name": "very",
                            "weight": 2
                        },
                        {
                            "name": "tired",
                            "weight": 1
                        },
                        {
                            "name": "of",
                            "weight": 5
                        },
                        {
                            "name": "sitting",
                            "weight": 1
                        },
                        {
                            "name": "by",
                            "weight": 2
                        },
                        {
                            "name": "her",
                            "weight": 5
                        },
                        {
                            "name": "sister",
                            "weight": 2
                        },
                        {
                            "name": "on",
                            "weight": 1
                        },
                        {
                            "name": "bank",
                            "weight": 1
                        },
                        {
                            "name": "and",
                            "weight": 4
                        },
                        {
                            "name": "having",
                            "weight": 1
                        },
                        {
                            "name": "nothing",
                            "weight": 1
                        },
                        {
                            "name": "do",
                            "weight": 1
                        },
                        {
                            "name": "once",
                            "weight": 1
                        },
                        {
                            "name": "or",
                            "weight": 3
                        },
                        {
                            "name": "twice",
                            "weight": 1
                        },
                        {
                            "name": "she",
                            "weight": 3
                        },
                        {
                            "name": "had",
                            "weight": 2
                        },
                        {
                            "name": "peeped",
                            "weight": 1
                        },
                        {
                            "name": "into",
                            "weight": 1
                        },
                        {
                            "name": "book",
                            "weight": 2
                        },
                        {
                            "name": "reading",
                            "weight": 1
                        },
                        {
                            "name": "but",
                            "weight": 1
                        },
                        {
                            "name": "it",
                            "weight": 2
                        },
                        {
                            "name": "no",
                            "weight": 1
                        },
                        {
                            "name": "pictures",
                            "weight": 2
                        },
                        {
                            "name": "conversations",
                            "weight": 1
                        },
                        {
                            "name": "in",
                            "weight": 2
                        },
                        {
                            "name": "what",
                            "weight": 1
                        },
                        {
                            "name": "is",
                            "weight": 1
                        },
                        {
                            "name": "use",
                            "weight": 1
                        },
                        {
                            "name": "a",
                            "weight": 3
                        },
                        {
                            "name": "thought",
                            "weight": 1
                        },
                        {
                            "name": "without",
                            "weight": 1
                        },
                        {
                            "name": "conversationSo",
                            "weight": 1
                        },
                        {
                            "name": "considering",
                            "weight": 1
                        },
                        {
                            "name": "own",
                            "weight": 1
                        },
                        {
                            "name": "mind",
                            "weight": 1
                        },
                        {
                            "name": "as",
                            "weight": 2
                        },
                        {
                            "name": "well",
                            "weight": 1
                        },
                        {
                            "name": "could",
                            "weight": 1
                        },
                        {
                            "name": "for",
                            "weight": 1
                        },
                        {
                            "name": "hot",
                            "weight": 1
                        },
                        {
                            "name": "day",
                            "weight": 1
                        },
                        {
                            "name": "made",
                            "weight": 1
                        },
                        {
                            "name": "feel",
                            "weight": 1
                        },
                        {
                            "name": "sleepy",
                            "weight": 1
                        },
                        {
                            "name": "stupid",
                            "weight": 1
                        },
                        {
                            "name": "whether",
                            "weight": 1
                        },
                        {
                            "name": "pleasure",
                            "weight": 1
                        },
                        {
                            "name": "making",
                            "weight": 1
                        },
                        {
                            "name": "daisy-chain",
                            "weight": 1
                        },
                        {
                            "name": "would",
                            "weight": 1
                        },
                        {
                            "name": "be",
                            "weight": 1
                        },
                        {
                            "name": "worth",
                            "weight": 1
                        },
                        {
                            "name": "trouble",
                            "weight": 1
                        },
                        {
                            "name": "getting",
                            "weight": 1
                        },
                        {
                            "name": "up",
                            "weight": 1
                        },
                        {
                            "name": "picking",
                            "weight": 1
                        },
                        {
                            "name": "daisies",
                            "weight": 1
                        },
                        {
                            "name": "when",
                            "weight": 1
                        },
                        {
                            "name": "suddenly",
                            "weight": 1
                        },
                        {
                            "name": "White",
                            "weight": 1
                        },
                        {
                            "name": "Rabbit",
                            "weight": 1
                        },
                        {
                            "name": "with",
                            "weight": 1
                        },
                        {
                            "name": "pink",
                            "weight": 1
                        },
                        {
                            "name": "eyes",
                            "weight": 1
                        },
                        {
                            "name": "ran",
                            "weight": 1
                        },
                        {
                            "name": "close",
                            "weight": 1
                        },
                        {
                            "name": "",
                            "weight": 1
                        }
                    ],
                    "name": "Occurrences"
                }
            ],
            "title": {
                "text": "Wordcloud of Alice's Adventures in Wonderland",
                "align": "left"
            },
            "subtitle": {
                "text": "An excerpt from chapter 1: Down the Rabbit-Hole",
                "align": "left"
            },
            "tooltip": {
                "headerFormat": "<span style=\"font-size: 16px\"><b>{point.name}</b></span><br>"
            }
        },
        []
    ],
    "vis-7": [
        {}, []
    ],
    "vis-8": [
        {
            "title": {
                "text": "Researcher",
                "subtext": "Circular layout",
                "top": "bottom",
                "left": "right"
            },
            "tooltip": {},
            "legend": [],
            "animationDurationUpdate": 1500,
            "animationEasingUpdate": "quinticInOut"
        },
        []
    ]
}

async def get_visualization_data(dashboard: Dashboard, visualization_uuid: UUID, queries: dict) -> VisualizationData:
    try:
        visualization = next(v for v in dashboard.visualizations if v.uuid == visualization_uuid)
        chart_cls = next(chart for chart in CHARTS if chart.identifier == visualization.chart)
        chart_instance = chart_cls()
        chart_input = ChartInput(queries=queries, pre_filters=visualization.query_preset)
        return VisualizationData(
            series=await chart_instance.get_series(chart_input),
            generator=chart_instance.generator,
            chart_template=chart_instance.chart_template,
            filters=chart_input.get_all_queries())
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization/Type not found")

async def get_visualization_data_old(dashboard: Dashboard, visualization_uuid: UUID):
    try:
        visualization = next(v for v in dashboard.visualizations if v.uuid == visualization_uuid)
        t = "Highcharts"
        spec = mock_data[visualization.chart][0]
        data = mock_data[visualization.chart][1]
        if visualization.chart == "vis-4":
            works = await Work.find_all(limit=30).to_list()
            base = works[0].authors[0]
            data = []
            for w in works:
                await w.fetch_link(Work.authors)
                data = data + [[base.full_name, a.full_name] for a in filter(lambda x: x.id != base.id, w.authors)]
            spec["series"][0]["data"] = data
        if visualization.chart == "vis-7":
            institutions = await Institution.find(Not(Institution.location == None)).to_list()
            data = [{"type": "marker",
                     "data": [{"id": i.uuid, "name": i.name, "position": i.location} for i in institutions]}]
            t = "Leaflet"
        if visualization.chart == "vis-8":
            works = await Work.find_all(limit=30).to_list()
            nodes = []
            links = []
            for w in works:
                await w.fetch_link(Work.authors)
                author_nodes = [{"id": a.uuid, "name": a.full_name} for a in w.authors]
                nodes = nodes + author_nodes
                author_ids = [a.uuid for a in w.authors]
                pairs = list(combinations(author_ids, 2))
                pairs = [{"source": s, "target": t} for s, t in pairs]
                links = links + pairs
            nodes = _.uniq_by(nodes, lambda a: a["id"])

            data = [
                {
                    "name": "Researcher",
                    "type": "graph",
                    "layout": "circular",
                    "circular": {
                        "rotateLabel": True
                    },
                    "focusNodeAdjacency": True,
                    "itemStyle": {
                        "opacity": 0.8
                    },
                    "emphasis": {
                        "itemStyle": {
                            "opacity": 1
                        },
                        "lineStyle": {
                            "opacity": 1
                        }
                    },
                    "data": nodes,
                    "links": links,
                    "roam": True,
                    "label": {
                        "position": "right",
                        "formatter": "{b}"
                    },
                    "lineStyle": {
                        "color": "source",
                        "curveness": 0.3
                    }
                }
            ]
            t = "ECharts"
        return {
            "spec": spec,
            "data": data,
            "type": t
        }
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization not found")
