import $ from 'jquery';
import ClipboardJS from 'clipboard';

// Clipboard
var clipboard = new ClipboardJS('.btn-copy', {
  target: function(trigger) {
    return $(trigger).siblings('.copy-target').get(0);
  }
});

clipboard.on('success', function(e) {
    e.clearSelection();
});
