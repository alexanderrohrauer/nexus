export default function (nexus) {
    const x = nexus.series("researchers").map(r => r[0]).reverse();
    const y = nexus.series("researchers").map(r => r[1]).reverse();
    return {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {},
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
        },
        yAxis: {
            type: 'category',
            data: x,
            axisLabel: {
                interval: 0
            }
        },
        series: [
            {
                name: 'Works count',
                type: 'bar',
                data: y
            }
        ]
    }
}
