import $ from 'jquery';
import ClipboardJS from 'clipboard';
import Chart from 'chart.js';

// Clipboard
var clipboard = new ClipboardJS('.btn-copy', {
  target: function(trigger) {
    return $(trigger).siblings('.copy-target').get(0);
  }
});

clipboard.on('success', function(e) {
    e.clearSelection();
});

var ctx = document.getElementById("click_stats_id");
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: click_stats['labels'],
        datasets: [{
            label: '# of Votes',
            data: click_stats['values'],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 0
        }]
    },
});

var ctx = document.getElementById("referal_stats_id");
var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: referal_stats['labels'],
        datasets: [{
            label: '# of Votes',
            data: referal_stats['values'],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 0
        }]
    },
});

var ctx = document.getElementById("country_stats_id");
var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: country_stats['labels'],
        datasets: [{
            label: '# of Votes',
            data: country_stats['values'],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 0
        }]
    },
});

var ctx = document.getElementById("browser_stats_id");
var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: browser_stats['labels'],
        datasets: [{
            label: '# of Votes',
            data: browser_stats['values'],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 0
        }]
    },
});

var ctx = document.getElementById("os_stats_id");
var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: os_stats['labels'],
        datasets: [{
            label: '# of Votes',
            data: os_stats['values'],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 0
        }]
    },
});