export default function(nexus) {
    return {
        "title": {
            "text": "Researcher",
            "subtext": "Circular layout",
            "top": "bottom",
            "left": "right"
        },
        "series": [
            nexus.series("researchers", {
                "name": "Researcher",
                "type": "graph",
                "layout": "circular",
                "circular": {
                    "rotateLabel": true
                },
                "focusNodeAdjacency": true,
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
                "roam": true,
                "label": {
                    "position": "right",
                    "formatter": "{b}"
                },
                "lineStyle": {
                    "color": "source",
                    "curveness": 0.3
                }
            })
        ],
        "tooltip": {},
        "legend": [],
        "animationDurationUpdate": 1500,
        "animationEasingUpdate": "quinticInOut"
    }
}
