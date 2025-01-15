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
                "minSize": "50%",
                "maxSize": "100%",
                "zMin": 10,
                "zMax": 100,
                "layoutAlgorithm": {
                    "gravitationalConstant": 0.08,
                    "splitSeries": true,
                    "seriesInteraction": false,
                    "dragBetweenSeries": true,
                    "parentNodeLimit": true
                },
                "dataLabels": {
                    "enabled": true,
                    "format": "{point.name}",
                }
            }
        },
        "series": data.map(el => ({...el, animation: false}))
    }
}
