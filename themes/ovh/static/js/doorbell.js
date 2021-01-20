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

    var sendDoorbell = function(sentiment, message, email, success, error) {
        if (sentiment) {
            doorbell.setOption('sentiment', sentiment);
            doorbell.send( message, email, success, error);
        }
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
        sendEmptyFeedback: function() {
            var sentiment = getSentiment();
            sendDoorbell(sentiment, '', '');
        },
        sendFeedback: function() {
            var sentiment = getSentiment();

            var success = function() {
                $('#form').empty().hide();
                $('#thanks').fadeIn();
            };

            var error = function() {
                console.log(error);
            };

            var messagePrefix = sentiment === 'positive' ?
                "[yes-comment] " : "";

            sendDoorbell(
                sentiment,
                messagePrefix + $('#form textarea').val(),
                '',
                success,
                error
            );
        },
        disableSend: disableSend,
        enableSend: enableSend,
        getSentiment: getSentiment,
    }

})()

$(document).ready(function() {
    $('#form textarea').on('input', function() {
        $(this).val() ? OvhDoorbell.enableSend() : OvhDoorbell.disableSend();
    });
});
