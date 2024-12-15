const data =  {
    name: 'Les Miserables',
    type: 'graph',
    layout: 'circular',
    circular: {
        rotateLabel: true
    },
    roam: true,
    label: {
        position: 'right',
        formatter: '{b}'
    },
    lineStyle: {
        color: 'source',
        curveness: 0.3
    }
}
console.log(JSON.stringify(data, null, 4))
