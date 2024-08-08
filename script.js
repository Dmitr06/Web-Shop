$('.review-cards').slick({
  infinite: true,
  slidesToShow: 3,
  slidesToScroll: 3
});
$('.goods__card').hover(
  function() {
    $('.goods__card').css('border', 'solid grey')
  }, function() {
    $('.goods__card').removeAttr('style')
  }
);