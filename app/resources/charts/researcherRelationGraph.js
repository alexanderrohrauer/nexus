export default function (nexus) {
    const categories = ["L0", "L1", "L2"]
    return {
        title: {
            text: 'Les Miserables',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right'
        },
        tooltip: {},
        legend: [
            {
                data: categories
            }
        ],
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
           nexus.series("works",  {
               name: 'Les Miserables',
               type: 'graph',
               legendHoverLink: false,
               layout: 'force',
               roam: true,
               categories,
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
                   edgeLength: 200,
               },
           })
        ]
    }
}
