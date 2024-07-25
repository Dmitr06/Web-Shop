$('.review-cards').slick({
  infinite: false,
  slidesToShow: 4,
  slidesToScroll: 1,
  responsive: [
    {
      breakpoint: 990,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 1,
        infinite: true,
        autoplay:true,
        autoplaySpeed:5000,
        arrows: false
      } 
    },
    {
      breakpoint: 768,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        autoplay:true,
        autoplaySpeed:5000,
        arrows: false
      }
    }     
  ]
});