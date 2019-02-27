/* global $, Chart, click_stats, referal_stats, country_stats, browser_stats, os_stats */
var ClickStatsCtx = $('#click_stats_id')
new Chart(ClickStatsCtx, {
  type: 'line',
  fill: true,
  data: {
    labels: click_stats['labels'],
    datasets: [{
      label: 'Clicks',
      data: click_stats['values'],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)'
      ],
      borderWidth: 0
    }]
  },
  options: {
    legend: {
      display: false,
    },
    responsive: true,
    scales: {
      xAxes: [{
        display: true,
        ticks: {
          callback: function(dataLabel, index) {
            // Hide the label of every 2nd dataset. return null to hide the grid line too
            return index % 2 === 0 ? dataLabel : '';
          }
        }
      }],
      yAxes: [{
        display: true,
        beginAtZero: false,
        ticks: {
          maxTicksLimit: 4
        }
      }]
    }
  }
})

var ReferalStatsCtx = $('#referal_stats_id')
new Chart(ReferalStatsCtx, {
  type: 'pie',
  data: {
    labels: referal_stats['labels'],
    datasets: [{
      label: 'Clicks',
      data: referal_stats['values'],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)'
      ],
      borderWidth: 0
    }]
  }
})

var CountryStatsCtx = $('#country_stats_id')
new Chart(CountryStatsCtx, {
  type: 'pie',
  data: {
    labels: country_stats['labels'],
    datasets: [{
      label: 'Clicks',
      data: country_stats['values'],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)'
      ],
      borderWidth: 0
    }]
  }
})

var BrowserStatsCtx = $('#browser_stats_id')
new Chart(BrowserStatsCtx, {
  type: 'horizontalBar',
  data: {
    labels: browser_stats['labels'],
    datasets: [{
      label: 'Clicks',
      data: browser_stats['values'],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)'
      ],
      borderWidth: 0
    }]
  },
  options: {
    legend: {
      display: false,
    },
    responsive: true,
    scales: {
      xAxes: [{
        display: true,
        beginAtZero: false,
        ticks: {
          maxTicksLimit: 5
        }
      }]
    }
  }
})

var OSStatsCtx = $('#os_stats_id')
new Chart(OSStatsCtx, {
  type: 'horizontalBar',
  data: {
    labels: os_stats['labels'],
    datasets: [{
      label: 'Clicks',
      data: os_stats['values'],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)'
      ],
      borderWidth: 0
    }]
  },
  options: {
    legend: {
      display: false,
    },
    responsive: true,
    scales: {
      xAxes: [{
        display: true,
        beginAtZero: false,
        ticks: {
          maxTicksLimit: 5
        }
      }]
    }
  }
})
