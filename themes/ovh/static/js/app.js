$(function(){

  // Typogrify (WARNING: must be run *before* magellan)
  $('#page').find('h1, h2, h3, h4, h5, h6, li, p, dt, dd').add('.entry-title *').each(function(){
    _this = $(this); _this.html(typogr.typogrify(_this));
  });

  // Little helper for CSS styling
  $('#content > .section:last').addClass('last');

  // Avoid dead images in dev
  if (window.location.hostname == '127.0.0.1') {
    $('.main_logo img').attr('src', '/theme/img/logo.png');
    $('img[src="/fr/images/index/2014/jobs.jpg"]').attr('src', '/theme/img/jobs.jpg');
    $('img[src="/fr/images/index/eu.jpg"]').attr('src', '/theme/img/eu.jpg');
  }

  $('.carousel').slick({dots: true, centerMode: true});

  $('#cross').on('click', function() {
    $('#cookiesPop').remove();
  });

  $('.tabs').each(function(_, el) {
    new Foundation.Tabs($(el));
  });
});
