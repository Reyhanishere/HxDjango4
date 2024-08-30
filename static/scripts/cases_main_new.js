let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
// function currentSlide(n) {
//   showSlides(slideIndex = n);
// }

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("demo");
  let captionText = document.getElementById("caption");
  let extendedCaptionText = document.getElementById("extended-caption");

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}

  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";

   // Array of captions for each image
   let captions = [
    "خار پاشنه",
    "اسکن تیروئید",
    "یک پیشنهاد",
    "اسکلرودرمی",
    "مایع جنب خونی",
    " ادرار پرتقالی چون اصلا نمی‌خواستم نجات پیدا کنم، ف"
  ];

  // Array of extended captions for each image
  let extendedCaptions = [
    "خار پاشنه در بیمار دیابتی",
    "اسکن تیروئید با جذب تکنسین در بیمار با Tsh پایین",
    "یک پیشنهاد گرفتن یک دراگ هیستوری دقیق خیلی وقت‌ها دشوار است. با این کار، زحمت همه کمتر می‌شود!",
    "اسکلرودرمی ندول کلسیفیه +دفورمیتی در DIPانگشتان",
    "مایع جنب خونی هموتوراکس چیه و تپ پلور چطوری انجام میشه؟",
    "این متن برای بررسی ماکسیمم تعداد حروف ممکن است. ادرار پرتقالی چه مزه ای میدهد؟ با ما همراه باشید . یا علی تموم نمیشه. به بهانۀ این رنگ ادرار، به مبحث تغییر رنگ ادرار پرداختم. از دست ندید! وا تموم نش ب"
  ];

  // Display the caption for the current slide
  captionText.innerHTML = captions[slideIndex-1];

  // Display the extended caption for the current slide
  extendedCaptionText.innerHTML = extendedCaptions[slideIndex-1];

  dots[slideIndex-1].className += " active";
}




