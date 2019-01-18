var ClickStatsCtx = $('#click_stats_id')
Chart(ClickStatsCtx, {
  type: 'line',
  data: {
    labels: click_stats['labels'],
    datasets: [{
      label: '# of Votes',
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
  }
})

var ReferalStatsCtx = $('#referal_stats_id')
Chart(ReferalStatsCtx, {
  type: 'pie',
  data: {
    labels: referal_stats['labels'],
    datasets: [{
      label: '# of Votes',
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
Chart(CountryStatsCtx, {
  type: 'pie',
  data: {
    labels: country_stats['labels'],
    datasets: [{
      label: '# of Votes',
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
Chart(BrowserStatsCtx, {
  type: 'horizontalBar',
  data: {
    labels: browser_stats['labels'],
    datasets: [{
      label: '# of Votes',
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
  }
})

var OSStatsCtx = $('#os_stats_id')
Chart(OSStatsCtx, {
  type: 'horizontalBar',
  data: {
    labels: os_stats['labels'],
    datasets: [{
      label: '# of Votes',
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
  }
})
