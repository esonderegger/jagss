function shortenLongArticles(){
  $(".ebsActualText").each(function(index) {
    var subElements = $(this).children();
    var wordcount = 0;
    var articleTruncated = false;
    subElements.each(function() {
      wordcount += $(this).text().split(" ").length;
      if (wordcount > 175) {
        articleTruncated = true;
        $(this).hide();
      }
    });
    if (articleTruncated) {
      $(this).append('<p><a href="' + $(this).attr('data-permalink') + '">Read more...</a></p>');
    }
  });
}

$(window).resize(function() {
    var activeImg = $("#galleryModal").attr('data-id');
    if (activeImg) {
        makeGalleryModal(activeImg);
    }
});

function makeGalleryModal(photoID) {
    $("#galleryModal").attr('data-id', photoID);
    var photo = $("#" + photoID);
    var aspectRatio = photo.attr('data-width') / photo.attr('data-height');
    var modalWidth = photo.attr('data-width') / 2;
    var modalHeight = photo.attr('data-height') / 2;
    var offset = 60;
    if ($(window).width() < 768) {
        offset = 20;
    }
    if ($(window).width() - offset < modalWidth) {
        modalWidth = $(window).width() - offset;
        modalHeight = modalWidth / aspectRatio;
    }
    if ($(window).height() - offset < modalHeight) {
        modalHeight = $(window).height() - offset;
        modalWidth = modalHeight * aspectRatio;
    }
    var marginTop = ($(window).height() - modalHeight) / 2;
    $('#galleryModalDialog').css("width", modalWidth);
    $('#galleryModalDialog').css("height", modalHeight);
    $('#galleryModalContent').css("width", modalWidth);
    $('#galleryModalContent').css("height", modalHeight);
    $('#galleryModalDialog').css("margin-top", marginTop);
    $('#galleryModalContent').css("background-image", "url(" + photo.attr('data-root') + "/" + photoID + ".jpg)");
    $('#galleryModalContent').css("background-size", modalWidth);    
}

function moveLeft(){
    var activeModal = $("#galleryModal").attr('data-id');
    var prevImg = $("#" + activeModal).prev().attr('id');
    if (prevImg) {
        makeGalleryModal(prevImg);
    } else {
        var lastImg = $(".ebsGalleryThumbnail").last().attr('id');
        makeGalleryModal(lastImg);
    }
}
function moveRight(){
    var activeModal = $("#galleryModal").attr('data-id');
    var nextImg = $("#" + activeModal).next().attr('id');
    if (nextImg) {
        makeGalleryModal(nextImg);
    } else {
        var firstImg = $(".ebsGalleryThumbnail").first().attr('id');
        makeGalleryModal(firstImg);
    }
}

function checkKey(e) {
    e = e || window.event;
    if (e.keyCode == 37){
      moveLeft();
    } else if (e.keyCode == 39) {
      moveRight();
    }
}

document.onkeydown = checkKey;

// Here is some code for swipe gestures from scottgale.com
document.ontouchend = function() {
   //swipe left
   if( self.swipeLeft && self.swipe ) {
      self.moveTo(self.current-1);
      moveLeft();               
   //swipe right
   } else if(self.swipe) {
      self.moveTo(self.current+1);
      moveRight();
   }            
}
document.ontouchmove = function(e){
   //move only if you swipe across
   if( Math.abs(e.touches[0].pageX - self.startX) > 150 ) {
      if( (e.touches[0].pageX - self.startX) > 5 ) {
         self.swipeLeft = true
      } else {
         self.swipeLeft = false;
      }
      self.swipe = true;
   }
}
document.ontouchstart = function(e) {
   self.startX = e.touches[0].pageX;
   self.swipe = false;
}
