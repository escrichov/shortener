/* global $, ClipboardJS */

$('.btn-copy').tooltip({
  trigger: 'click',
  placement: 'right'
})

function setTooltip (e, message) {
  e.tooltip('hide')
    .attr('data-original-title', message)
    .tooltip('show')
}

function hideTooltip (e) {
  setTimeout(function () {
    e.tooltip('hide')
  }, 800)
}

// Clipboard
var clipboard = new ClipboardJS('.btn-copy', {
  target: function (trigger) {
    return $(trigger).siblings('.copy-target').get(0)
  }
})

clipboard.on('success', function (e) {
  console.log(e)
  e.clearSelection()
  setTooltip($(e.trigger), 'Copied!')
  hideTooltip($(e.trigger))
})

clipboard.on('error', function (e) {
  setTooltip($(e.trigger), 'Failed!')
  hideTooltip($(e.trigger))
})
