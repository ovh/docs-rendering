$(function () {
    var $deprecatedModal = $('.deprecated-modal');
    var $deprecatedBlock = $('.deprecated-block');
    var SESSION_ITEM_NAME = 'docs.ovh.com_deprecated_modal';

    var disableScroll = function() {
        document.body.style.position = 'fixed';
        document.body.style.width = '100%';
    };
    
    var enableScroll = function() {
        document.body.style.position = '';
        document.body.style.width = '';
    }

    var modal = function () {
        var close = function () {
            sessionStorage.setItem(SESSION_ITEM_NAME, true);
            block();
            $deprecatedModal.addClass('deprecated-hidden');
            enableScroll();
        }

        disableScroll();
        $deprecatedModal.removeClass('deprecated-hidden');
        $deprecatedModal
            .on('click', '.close', close)
            .on('click', '.deprecated-modal__background', close);
    }

    var block = function () {
        $deprecatedBlock.removeClass('deprecated-hidden');
    }

    sessionStorage.getItem(SESSION_ITEM_NAME) ? block() : modal();
})
