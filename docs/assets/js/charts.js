// Get bases values from REST API
$(document).ready(function () {
    $.ajax({
        url: "https://heig-park.herokuapp.com/stats"
    }).then(function (data) {
        $('.greeting-id').append(data.id);
        $('.greeting-content').append(data.content);

        // based on prepared DOM, initialize echarts instance
        var myChart = echarts.init(document.getElementById('ch-main'));

        console.log(data);

        // specify chart configuration item and data
        var option = {
            tooltip: {},
            dataset: {
                dimensions: ['date', 'nb_cars'],
                source: data
            },
            xAxis: {type: 'time'},
            yAxis: {},
            series: [{type: 'line'}],
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
                    gt: 0,
                    lte: 5,
                    color: '#096'
                }, {
                    gt: 5,
                    lte: 10,
                    color: '#ffde33'
                }, {
                    gt: 10,
                    lte: 15,
                    color: '#ff9933'
                }, {
                    gt: 15,
                    lte: 20,
                    color: '#cc0033'
                }, {
                    gt: 20,
                    lte: 25,
                    color: '#660099'
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
        myChart.setOption(option);
    });
});

