/*
 * Custom function for Doorbell.io
 */

var OvhDoorbell = (function() {

    var $sendButton = $('#form button');

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

    var enableSend = function() {
        $sendButton.removeClass('disabled');
    }

    var disableSend = function() {
        $sendButton.addClass('disabled');
    }

    return {
        helpful: function() {
            hideInitialQuestion();
            showYesText();
            setSentiment('positive');
            enableSend();
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
        },
        disableSend: disableSend,
        enableSend: enableSend,
        getSentiment: getSentiment,
    }

})()

$(document).ready(function() {
    $('#form textarea').on('input', function() {
        if (OvhDoorbell.getSentiment() === 'negative') {
            $(this).val() ? OvhDoorbell.enableSend() : OvhDoorbell.disableSend();
        }
    });
});
