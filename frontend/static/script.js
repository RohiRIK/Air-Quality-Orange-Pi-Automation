document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('data-chart').getContext('2d');

    const dataChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: [],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderWidth: 1,
                    yAxisID: 'y',
                },
                {
                    label: 'Humidity (%)',
                    data: [],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderWidth: 1,
                    yAxisID: 'y1',
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: {
                        drawOnChartArea: false, 
                    },
                },
            }
        }
    });

    function addData(chart, label, data) {
        chart.data.labels.push(label);
        chart.data.datasets.forEach((dataset, index) => {
            dataset.data.push(data[index]);
        });
        // Limit the number of data points to 30
        if (chart.data.labels.length > 30) {
            chart.data.labels.shift();
            chart.data.datasets.forEach((dataset) => {
                dataset.data.shift();
            });
        }
        chart.update();
    }

    async function fetchData() {
        try {
            const response = await fetch('/api/data');
            const data = await response.json();

            if (data) {
                document.getElementById('temperature').textContent = data.temperature_c || '--';
                document.getElementById('humidity').textContent = data.humidity_rh || '--';
                document.getElementById('pressure').textContent = data.pressure_hpa || '--';
                document.getElementById('aqi').textContent = data.air_quality_score || '--';
                document.getElementById('explanation').textContent = data.explanation || '--';

                if (data.timestamp) {
                    const timestamp = new Date(data.timestamp);
                    addData(dataChart, timestamp, [data.temperature_c, data.humidity_rh]);
                }
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    setInterval(fetchData, 2000);
    fetchData(); // Initial fetch
});
