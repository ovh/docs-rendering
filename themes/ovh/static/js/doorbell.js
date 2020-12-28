/*
 * Custom function for Doorbell.io
 */

var OvhDoorbell = (function() {

    var hideInitialQuestion = function() {
        $('#question').empty().hide();
    }

    var showYesText = function() {
        $('#form, #form .yes').fadeIn();
    }

    var showNoText = function() {
        $('#form, #form .no').fadeIn();
    }

    var setSentiment = function(sentiment) {
        $('#form button').data('sentiment', sentiment);
    }

    var getSentiment = function() {
        return $('#form button').data('sentiment');
    }

    return {
        helpful: function() {
            hideInitialQuestion();
            showYesText();
            setSentiment('positive');
        },
        unhelpful: function() {
            hideInitialQuestion();
            showNoText();
            setSentiment('negative');
        },
        sendFeedback: function() {
            var sentiment = getSentiment();
            if (sentiment) {
                doorbell.setOption('sentiment', sentiment);
                doorbell.send(
                    $('#form textarea').val(),
                    '',
                    function() {
                        $('#form').empty().hide();
                        $('#thanks').fadeIn();
                    }, function(error) {
                        alert(error);
                    });
            }
        }
    }

})()

$(document).ready(function() {
    $('#form textarea').on('input', function() {
    $(this).val() ? $('#form button').removeClass('disabled') : $('#form button').addClass('disabled');
  });
});
