
// Check if sentimentData, topicData, and dateData exist to avoid errors
const sentimentData = window.sentimentData || { labels: [], values: [] };
const topicData = window.topicData || { labels: [], values: [] };
const dateData = window.dateData || { labels: [], values: [] };

// Sentiment Chart (Pie)
const sentimentCtx = document.getElementById('sentimentChart').getContext('2d');
new Chart(sentimentCtx, {
    type: 'pie',
    data: {
        labels: sentimentData.labels,
        datasets: [{
            data: sentimentData.values,
            backgroundColor: ['#2ecc71', '#e74c3c', '#f1c40f'], // green, red, yellow
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Sentiment Distribution' }
        }
    }
});

// Topic Chart (Bar)
const topicCtx = document.getElementById('topicChart').getContext('2d');
new Chart(topicCtx, {
    type: 'bar',
    data: {
        labels: topicData.labels,
        datasets: [{
            label: 'Mentions',
            data: topicData.values,
            backgroundColor: '#3498db',
            borderRadius: 5
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            title: { display: true, text: 'Topic Frequency' }
        },
        scales: {
            x: {
                ticks: {
                    autoSkip: false,
                    maxRotation: 45,
                    minRotation: 0
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Count'
                }
            }
        }
    }
});

// Date Chart (Line)
const dateCtx = document.getElementById('dateChart').getContext('2d');
new Chart(dateCtx, {
    type: 'line',
    data: {
        labels: dateData.labels,
        datasets: [{
            label: 'Record Count',
            data: dateData.values,
            borderColor: '#8e44ad',
            backgroundColor: 'rgba(142, 68, 173, 0.2)',
            tension: 0.3,
            fill: true,
            pointRadius: 3,
            pointHoverRadius: 5
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'Mentions by Date' }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Mentions'
                }
            }
        }
    }
});

