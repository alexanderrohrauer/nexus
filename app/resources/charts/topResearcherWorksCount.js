export default function (nexus) {
    const x = nexus.series("researchers").map(r => r[0])
    const y = nexus.series("researchers").map(r => r[1])
    return {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: [
            {
                type: 'category',
                data: x,
                axisLabel: { interval: 0, rotate: 30 }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                type: 'bar',
                name: "Works count",
                data: y
            }
        ]
    }
}
