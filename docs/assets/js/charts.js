let main = echarts.init(document.getElementById('ch-main'));
let parkText = document.getElementById('park-text')
let parkTextDate = document.getElementById('park-text-date')

$(document).ready(function () {
    $.ajax({
        url: "https://heig-park.herokuapp.com/"
    }).then(function (data) {
        // specify chart configuration item and data
        let option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            series: [
                {
                    type: 'pie',
                    data: [
                        { name: 'libres', value: data['free_place'], itemStyle: { color: '#096' } },
                        { name: 'occupés', value: data['num_cars'], itemStyle: { color: '#cc0033' } }
                    ],
                    name: 'Nombre de places'
                }
            ]
        };

        // use configuration item and data specified to show chart
        main.setOption(option);

        // Updating the text
        parkText.innerHTML = "Il y a actuellement <span class='text-error'>" + data['num_cars'] + "</span> voitures présentes sur le parking."
        console.log(Date.parse(data['date']))
        d = data['date'].replace(" ", "T")
        parkTextDate.innerText = new Date(Date.parse(d)).toLocaleString()
    });
});

setInterval(() => {
    $.ajax({
        url: "https://heig-park.herokuapp.com/"
    }).then(function (data) {
        // specify chart configuration item and data
        let option = {
            series: [
                {
                    data: [
                        { name: 'libres', value: data['free_place'], itemStyle: { color: '#096' } },
                        { name: 'occupés', value: data['num_cars'], itemStyle: { color: '#cc0033' } }
                    ]
                }
            ]
        };

        // use configuration item and data specified to show chart
        main.setOption(option);

        // Updating the text
        parkText.innerHTML = "Il y a actuellement <span class='text-error'>" + data['num_cars'] + "</span> voitures présentes sur le parking."
        d = data['date'].replace(" ", "T")
        parkTextDate.innerText = new Date(Date.parse(d)).toLocaleString()
    });
}, 15000)


let stats = echarts.init(document.getElementById('ch-stats'));
stats.showLoading()

let data_base = []
let data_zero = []

function load_stats() {
    $.ajax({
        url: "https://heig-park.herokuapp.com/stats",
        timeout: 10000
    }).then(function (data) {
        stats.hideLoading();

        // specify chart configuration item and data
        let option = {
            tooltip: {},
            dataset: {
                //dimensions: ['date', 'nb_cars', 'nb_cars'],
                source: data
            },
            xAxis: { type: 'time' },
            yAxis: { type: 'value' },
            series: [
                {
                    type: 'scatter',
                    encode: {
                        x: 'date',
                        y: 'nb_cars'
                    },
                    markPoint: {
                        data: [
                            { type: 'max', name: 'Max' },
                        ]
                    },
                    itemStyle: {
                    },
                    large: true,
                    barGap: '0%',
                    name: 'Nombre de voitures'
                }/*,
                {
                    type: 'scatter',
                    encode: {
                        x: 'date',
                        y: 'nb_cars'
                    }
                }*/
            ],
            dataZoom: [
                {   // this dataZoom component controls x-axis by dafault
                    type: 'slider', // this dataZoom component is dataZoom component of slider
                    start: 80,      // the left is located at 10%
                    end: 100         // the right is located at 60%
                }
            ],
            visualMap: {
                top: 10,
                right: 10,
                pieces: [{
                    gte: 0,
                    lte: 0,
                    color: ' #b3ffe6'
                }, {
                    gt: 0,
                    lte: 5,
                    color: '#096'
                }, {
                    gt: 5,
                    lte: 15,
                    color: '#ffde33'
                }, {
                    gt: 15,
                    lte: 20,
                    color: '#ff9933'
                }, {
                    gt: 20,
                    lte: 25,
                    color: '#cc0033'
                }, {
                    gt: 25,
                    color: '#7e0023'
                }],
                outOfRange: {
                    color: '#999'
                }
            }
        };

        // use configuration item and data specified to show chart
        stats.setOption(option);
    }).catch(function (e) {
        load_stats()
    });
}

// Get bases values from REST API
$(document).ready(function () {
    load_stats()
});

