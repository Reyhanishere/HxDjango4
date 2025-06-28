const createBarMainChart = (all_zscores) => {
    return new Chart(document.getElementById('mainChart'), {
        type: 'bar',
        data: {
            labels: all_zscores.labels,
            datasets: [{
                label: 'Weight Z-Score',
                data: all_zscores.weight_z,
                backgroundColor: `#441752`,
                fill: false,
            }, {
                label: 'Height Z-Score Summary',
                data: all_zscores.height_z,
                backgroundColor: `#4dc9f6`,
                fill: false,
            }, {
                label: 'BMI Z-Score',
                data: all_zscores.bmi_z,
                backgroundColor: `#f564a9`,
                fill: false,
            }, {
                label: 'Head Circumference Z-Score',
                data: all_zscores.hc_z,
                backgroundColor: `#FCC201`,
                fill: false,
            }]
        },
    });
}
const createLineMainChart = (all_zscores) => {
    return new Chart(document.getElementById('mainChart'), {
        type: 'line',
        data: {
            labels: all_zscores.labels,
            datasets: [{
                label: 'Weight Z-Score',
                data: all_zscores.weight_z,
                //backgroundColor: `rgba(34, 197, 94, 0.8)`,
                fill: false,
            }, {
                label: 'Height Z-Score Summary',
                data: all_zscores.height_z,
                //backgroundColor: `rgba(197, 34, 94, 0.8)`,
                fill: false,
            }, {
                label: 'BMI Z-Score',
                data: all_zscores.bmi_z,
                //backgroundColor: `rgba(34, 94, 197, 0.8)`,
                fill: false,
            }, {
                label: 'Head Circumference Z-Score',
                data: all_zscores.hc_z,
                //backgroundColor: `rgba(34, 94, 197, 0.8)`,
                fill: false,
            }, {
                label: 'Weight for Length',
                data: all_zscores.wl_z,
                //backgroundColor: `rgba(34, 94, 197, 0.8)`,
                fill: false,
            }]
        },
    });
}
const createAltChart = (alt_chart, kidData) => {
    return new Chart(document.getElementById('altChart'), {
        type: 'bar',
        data: {
            labels: alt_chart.agemos,
            datasets: [{
                type: 'line',
                label: 'P3',
                data: alt_chart.p3,
                borderColor: `rgb(255, 99, 132)`,
                backgroundColor: `rgba(255, 99, 132, 0.2)`,
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'line',
                label: 'P5',
                data: alt_chart.p5,
                borderColor: 'rgb(255, 159, 64)',
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'line',
                label: 'P10',
                data: alt_chart.p10,
                borderColor: 'rgb(255, 205, 86)',
                backgroundColor: 'rgba(255, 205, 86, 0.2)',
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'line',
                label: 'P25',
                data: alt_chart.p25,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'line',
                label: 'P50',
                data: alt_chart.p50,
                borderColor: 'rgb(153, 102, 255)',
                backgroundColor: `rgba(153, 102, 255, 0.2)`,
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'line',
                label: 'P75',
                data: alt_chart.p75,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'line',

                label: 'P90',
                data: alt_chart.p90,
                borderColor: 'rgb(255, 205, 86)',
                backgroundColor: 'rgba(255, 205, 86, 0.2)',
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'line',
                label: 'P95',
                data: alt_chart.p95,
                borderColor: 'rgb(255, 159, 64)',
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'line',
                label: 'P97',
                data: alt_chart.p97,
                borderColor: `rgb(255, 99, 132)`,
                backgroundColor: `rgba(255, 99, 132, 0.2)`,
                fill: false,
                tension: 0.4,
                borderWidth: 1.5,
                pointStyle: false,
            }, {
                type: 'bar',
                label: 'Weight',
                data: kidData,
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: false,
                borderRadius: 50,
            }]
        },

        options: {
            scales: {
                y: {
                    beginAtZero: false,
                    offset: false
                },
                x: {
                    offset: true
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Based on CDC Weight Percentiles'
                }
            },
        }
    });
}
const createMiniChart = (ctxId, label, data, labels, color) => {
    //if (data.filter(item => item !== null).length < 2){
    if (data.filter(Boolean).length < 2) {
        miniType = 'bar'
        miniOpac = 0.8
    }
    return new Chart(document.getElementById(ctxId), {
        type: miniType,
        data: {
            labels: labels,
            datasets: [{
                label,
                data,
                borderColor: `rgba(${color}, 1)`,
                backgroundColor: `rgba(${color}, ${miniOpac})`,
                fill: true,
            }]
        },
        options: {
            scales: {
                y: {
                    offset: true
                },
                x: {
                    offset: true
                }
            }
        }
    });
};

const createWfLChart = (ctxId, data_one, data_two, labels) => {
    return new Chart(document.getElementById(ctxId), {
        type: 'bar',
        data: {
            labels: labels,

            datasets: [{
                    type: 'bar',
                    label: 'Kid Weight for Length',
                    data: data_one,

                    fill: true,
                    order: 2

                },
                {
                    type: 'line',
                    label: 'Weight P50 for Length',
                    data: data_two,

                    fill: true,
                    order: 1,
                },
            ]
        },
        options: {
            scales: {
                y: {
                    offset: true
                },
                x: {
                    offset: true
                }
            },
            plugins: {
                legend: {
                    labels: {
                        // This more specific font property overrides the global property
                        font: {
                            family: '',
                            weight: '600'
                        }
                    },

                }
            }
        }
    });
};