export default function(nexus, echarts) {
    const {years, data} = nexus.series("works")

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
        xAxis: [
            {
                type: 'category',
                data: years,
                axisLabel: {
                    interval: 0,
                    rotate: 90
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: "Publications",
                nameLocation: 'middle',
                nameRotate: 90,
            }
        ],
        series: Object.entries(data).map(([key, value]) => ({
            name: key,
            type: 'bar',
            stack: 'type',
            emphasis: {
                focus: 'series'
            },
            data: value
        }))
    }
}
