export default function(nexus) {
    return {
        series: [
            {
                type: 'gauge',
                center: ['20%', '70%'],
                radius: "68%",
                color: "#16a34a",
                progress: {
                    show: true,
                    width: 14
                },
                max: 2000,
                axisLine: {
                    lineStyle: {
                        width: 14,
                    }
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    length: 12,
                    lineStyle: {
                        width: 2,
                        color: '#999'
                    }
                },
                axisLabel: {
                    distance: 25,
                    color: '#999',
                    fontSize: 16
                },
                anchor: {
                    show: true,
                    showAbove: true,
                    size: 20,
                    itemStyle: {
                        borderWidth: 8,
                        borderColor: "#16a34a"
                    }
                },
                title: {
                    show: true
                },
                detail: {
                    valueAnimation: true,
                    fontSize: 40,
                    offsetCenter: [0, '70%']
                },
                data: [
                    {
                        value: nexus.series("i10_index"),
                        name: "i10-Index"
                    }
                ]
            },
            {
                type: 'gauge',
                center: ['50%', '40%'],
                radius: "68%",
                color: "#0284c7",
                progress: {
                    show: true,
                    width: 14
                },
                max: 200,
                axisLine: {
                    lineStyle: {
                        width: 14
                    }
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    length: 12,
                    lineStyle: {
                        width: 2,
                        color: '#999'
                    }
                },
                axisLabel: {
                    distance: 25,
                    color: '#999',
                    fontSize: 16
                },
                anchor: {
                    show: true,
                    showAbove: true,
                    size: 20,
                    itemStyle: {
                        borderWidth: 8,
                        borderColor: "#0284c7"
                    }
                },
                title: {
                    show: true
                },
                detail: {
                    valueAnimation: true,
                    fontSize: 40,
                    offsetCenter: [0, '70%']
                },
                data: [
                    {
                        value: nexus.series("h_index"),
                        name: "h-Index"
                    }
                ]
            },
            {
                type: 'gauge',
                center: ['80%', '70%'],
                radius: "68%",
                color: "#ea580c",
                progress: {
                    show: true,
                    width: 14
                },
                max: 20,
                axisLine: {
                    lineStyle: {
                        width: 14
                    }
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    length: 12,
                    lineStyle: {
                        width: 2,
                        color: '#999'
                    }
                },
                axisLabel: {
                    distance: 25,
                    color: '#999',
                    fontSize: 16
                },
                anchor: {
                    show: true,
                    showAbove: true,
                    size: 20,
                    itemStyle: {
                        borderWidth: 8,
                        borderColor: "#ea580c"
                    }
                },
                title: {
                    show: true
                },
                detail: {
                    valueAnimation: true,
                    fontSize: 40,
                    offsetCenter: [0, '70%']
                },
                data: [
                    {
                        value: nexus.series("2yr_mean_citedness").toFixed(2),
                        name: "Impact factor (2yr)"
                    }
                ]
            },
        ]
    }
}
