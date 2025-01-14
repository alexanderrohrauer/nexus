export default function (nexus) {
    const categories = ["Level 0", "Level 1", "Level 2"]
    return {
        tooltip: {},
        legend: [
            {
                data: categories
            }
        ],
        series: [
           nexus.series("works",  {
               type: 'graph',
               legendHoverLink: false,
               layout: 'force',
               roam: true,
               categories: categories.map(c => ({name: c})),
               label: {
                   position: 'right',
                   formatter: '{b}'
               },
               lineStyle: {
                   color: 'source',
                   curveness: 0.3
               },
               emphasis: {
                   focus: 'adjacency',
                   lineStyle: {
                       width: 10
                   }
               },
               force: {
                   repulsion: 300,
                   edgeLength: 100,
               },
           })
        ]
    }
}
