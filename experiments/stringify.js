const data = {
    accessibility: {
        screenReaderSection: {
            beforeChartFormat: '<h5>{chartTitle}</h5>' +
                '<div>{chartSubtitle}</div>' +
                '<div>{chartLongdesc}</div>' +
                '<div>{viewTableButton}</div>'
        }
    },
    series: [{
        type: 'wordcloud',
        data: [
            {
                "name": "Chapter",
                "weight": 1
            },
            {
                "name": "Down",
                "weight": 1
            },
            {
                "name": "the",
                "weight": 8
            },
            {
                "name": "Rabbit-Hole",
                "weight": 1
            },
            {
                "name": "Alice",
                "weight": 2
            },
            {
                "name": "was",
                "weight": 3
            },
            {
                "name": "beginning",
                "weight": 1
            },
            {
                "name": "to",
                "weight": 2
            },
            {
                "name": "get",
                "weight": 1
            },
            {
                "name": "very",
                "weight": 2
            },
            {
                "name": "tired",
                "weight": 1
            },
            {
                "name": "of",
                "weight": 5
            },
            {
                "name": "sitting",
                "weight": 1
            },
            {
                "name": "by",
                "weight": 2
            },
            {
                "name": "her",
                "weight": 5
            },
            {
                "name": "sister",
                "weight": 2
            },
            {
                "name": "on",
                "weight": 1
            },
            {
                "name": "bank",
                "weight": 1
            },
            {
                "name": "and",
                "weight": 4
            },
            {
                "name": "having",
                "weight": 1
            },
            {
                "name": "nothing",
                "weight": 1
            },
            {
                "name": "do",
                "weight": 1
            },
            {
                "name": "once",
                "weight": 1
            },
            {
                "name": "or",
                "weight": 3
            },
            {
                "name": "twice",
                "weight": 1
            },
            {
                "name": "she",
                "weight": 3
            },
            {
                "name": "had",
                "weight": 2
            },
            {
                "name": "peeped",
                "weight": 1
            },
            {
                "name": "into",
                "weight": 1
            },
            {
                "name": "book",
                "weight": 2
            },
            {
                "name": "reading",
                "weight": 1
            },
            {
                "name": "but",
                "weight": 1
            },
            {
                "name": "it",
                "weight": 2
            },
            {
                "name": "no",
                "weight": 1
            },
            {
                "name": "pictures",
                "weight": 2
            },
            {
                "name": "conversations",
                "weight": 1
            },
            {
                "name": "in",
                "weight": 2
            },
            {
                "name": "what",
                "weight": 1
            },
            {
                "name": "is",
                "weight": 1
            },
            {
                "name": "use",
                "weight": 1
            },
            {
                "name": "a",
                "weight": 3
            },
            {
                "name": "thought",
                "weight": 1
            },
            {
                "name": "without",
                "weight": 1
            },
            {
                "name": "conversationSo",
                "weight": 1
            },
            {
                "name": "considering",
                "weight": 1
            },
            {
                "name": "own",
                "weight": 1
            },
            {
                "name": "mind",
                "weight": 1
            },
            {
                "name": "as",
                "weight": 2
            },
            {
                "name": "well",
                "weight": 1
            },
            {
                "name": "could",
                "weight": 1
            },
            {
                "name": "for",
                "weight": 1
            },
            {
                "name": "hot",
                "weight": 1
            },
            {
                "name": "day",
                "weight": 1
            },
            {
                "name": "made",
                "weight": 1
            },
            {
                "name": "feel",
                "weight": 1
            },
            {
                "name": "sleepy",
                "weight": 1
            },
            {
                "name": "stupid",
                "weight": 1
            },
            {
                "name": "whether",
                "weight": 1
            },
            {
                "name": "pleasure",
                "weight": 1
            },
            {
                "name": "making",
                "weight": 1
            },
            {
                "name": "daisy-chain",
                "weight": 1
            },
            {
                "name": "would",
                "weight": 1
            },
            {
                "name": "be",
                "weight": 1
            },
            {
                "name": "worth",
                "weight": 1
            },
            {
                "name": "trouble",
                "weight": 1
            },
            {
                "name": "getting",
                "weight": 1
            },
            {
                "name": "up",
                "weight": 1
            },
            {
                "name": "picking",
                "weight": 1
            },
            {
                "name": "daisies",
                "weight": 1
            },
            {
                "name": "when",
                "weight": 1
            },
            {
                "name": "suddenly",
                "weight": 1
            },
            {
                "name": "White",
                "weight": 1
            },
            {
                "name": "Rabbit",
                "weight": 1
            },
            {
                "name": "with",
                "weight": 1
            },
            {
                "name": "pink",
                "weight": 1
            },
            {
                "name": "eyes",
                "weight": 1
            },
            {
                "name": "ran",
                "weight": 1
            },
            {
                "name": "close",
                "weight": 1
            },
            {
                "name": "",
                "weight": 1
            }
        ],
        name: 'Occurrences'
    }],
    title: {
        text: 'Wordcloud of Alice\'s Adventures in Wonderland',
        align: 'left'
    },
    subtitle: {
        text: 'An excerpt from chapter 1: Down the Rabbit-Hole',
        align: 'left'
    },
    tooltip: {
        headerFormat: '<span style="font-size: 16px"><b>{point.name}</b>' +
            '</span><br>'
    }
}

console.log(JSON.stringify(data, null, 4))
