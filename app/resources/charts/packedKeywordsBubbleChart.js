export default function (nexus) {
    const data = nexus.series("works")
    return {
        "chart": {
            "type": "packedbubble",
            "height": "100%"
        },
        "title": {
            "text": "",
        },
        "tooltip": {
            "useHTML": true,
            "pointFormat": "<b>{point.name}:</b> {point.value}"
        },
        "plotOptions": {
            "packedbubble": {
                "animation": false,
                "minSize": "20%",
                "maxSize": "100%",
                "zMin": 0,
                "zMax": 1000,
                "layoutAlgorithm": {
                    "gravitationalConstant": 0.05,
                    "splitSeries": true,
                    "seriesInteraction": false,
                    "dragBetweenSeries": true,
                    "parentNodeLimit": true
                },
                "dataLabels": {
                    "enabled": true,
                    "format": "{point.name}",
                    "filter": {
                        "property": "y",
                        "operator": ">",
                        "value": 250
                    }
                }
            },
            series: {
                animation: false
            }
        },
        "series": data.map(el => ({...el, animation: false}))
    }
}
