/*
 * Custom function for Doorbell.io
 */
var helpful = function() {
  $('#question, #no ,#thanks').empty().hide();
  doorbell.setOption('sentiment', 'positive');
  doorbell.send('Positive feedback!', '', function() {
    $('#yes').fadeIn();
  }, function(error) {
    alert(error);
  });
}
var unhelpful = function() {
  doorbell.setOption('sentiment', 'negative');
  doorbell.send($('#no textarea').val(), '', function() {
    $('#no').empty().hide();
    $('#thanks').fadeIn();
  }, function(error) {
    alert(error);
  });
}

$(document).ready(function() {
  $('#no textarea').on('input', function() {
    $(this).val() ? $('#no button').removeClass('disabled') : $('#no button').addClass('disabled');
  });
});