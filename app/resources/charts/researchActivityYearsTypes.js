export default function(nexus, echarts) {
    const {years, data} = nexus.series("works")
    // const years = [2024, 2023]
    // const data = {email: [33, 22], union: [55, 66], video: [77, 88]}

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
                data: years
            }
        ],
        yAxis: [
            {
                type: 'value'
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
