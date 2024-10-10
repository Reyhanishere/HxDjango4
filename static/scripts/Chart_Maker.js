// for create and update view
const beginAtZeroCheckbox = document.getElementById('id_zero');
const chartContainer = document.getElementById('chart-container');
const tableContainer = document.getElementById('table-container');
const canvas = document.getElementById('myChart');
const inputTextArea = document.getElementById('id_data');

function updateChart() {
    const inputData = inputTextArea.value.trim();
    if (inputData) {
        const lines = inputData.split('\n').filter(line => line.trim() !== '');
        const labels = [];
        const datasets = [];
        let maxDataPoints = 0;

        const tableBody = document.getElementById('data-table').querySelector('tbody');
        tableBody.innerHTML = ''; // Clear existing rows

        lines.forEach((line, index) => {
            const [label, values] = line.split(': ');
            const dataPoints = values.split(', ').map(val => val === '-' ? null : parseFloat(val.trim()));
            datasets.push({
                label: label.trim(),
                data: dataPoints,
                borderWidth: 2
            });

            // Add to table
            if (index === 0) {
                labels.push('');
                for (let i = 0; i < dataPoints.length; i++) {
                    labels.push((i + 1).toString());
                }
            }
            addToTable(label.trim(), dataPoints, tableBody);

            maxDataPoints = Math.max(maxDataPoints, dataPoints.length);
        });

        if (!maxDataPoints) return; // Exit if no data


        const beginAtZero = beginAtZeroCheckbox.checked;

        createChart(labels, datasets, beginAtZero);
    }
}

let myChart;

function createChart(labels, datasets, beginZero) {
    if (myChart) {
        myChart.destroy(); // Destroy previous chart instance
    }

    const ctx = canvas.getContext('2d');
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            scales: {
                y: {
                    beginAtZero: beginZero
                }
            }
        }
    });
}

function addToTable(label, dataPoints, tableBody) {
    const rowCount = tableBody.rows.length;

    if (rowCount === 0) {
        // Create header row
        const headerRow = tableBody.insertRow(-1);
        const labelHeader = headerRow.insertCell(0);
        labelHeader.textContent = 'Day:';
        for (let i = 0; i < dataPoints.length; i++) {
            const dataHeader = headerRow.insertCell(-1);
            dataHeader.textContent = 'D' + (i + 1).toString();
        }
    }

    // Insert label and data points
    const dataRow = tableBody.insertRow(-1);
    const labelCell = dataRow.insertCell(0);
    labelCell.textContent = label;
    for (let i = 0; i < dataPoints.length; i++) {
        const dataCell = dataRow.insertCell(-1);
        dataCell.textContent = dataPoints[i];
    }
}

function makeVis() {
    tableContainer.style.display = 'block'
    chartContainer.style.display = 'block'
}

const refreshButton = document.getElementById('refresh-btn');
refreshButton.addEventListener('click', makeVis);
refreshButton.addEventListener('click', updateChart);

beginAtZeroCheckbox.addEventListener('change', updateChart);
