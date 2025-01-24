export default function (nexus, echarts) {
    return {
        plotOptions: {
            wordcloud: {
                maxFontSize: 55,
                minFontSize: 30
            }
        },
        series: [{
            type: 'wordcloud',
            data: Object.entries(nexus.series("works")).map(([key, value]) => ({name: key, weight: value.weight})),
            name: 'Occurrences',
        }],
        title: {
            text: '',
        },
        tooltip: {
            headerFormat: '<span style="font-size: 16px"><b>{point.name}</b>' +
                '</span><br>'
        }
    }
}
