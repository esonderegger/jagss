
$('.photoModal').each(function (i) { 
  var photoWidth = parseInt($(this).children('img').attr('width'));
  var photoHeight = parseInt($(this).children('img').attr('height'));
  var modalWidth = photoWidth + 40;
  var modalHeight = photoHeight + 50;
  var marginHo = modalWidth/-2;
  var marginVert = modalHeight/-2;
  $(this).css('width', modalWidth);
  $(this).css('height', modalHeight);
  $(this).css('margin-left', marginHo);
  $(this).css('margin-top', marginVert);
});

function moveLeft(){
  var activeModal = $("body").find(".photoModal").not(":hidden");
  if (activeModal.length){
    var prevLink = activeModal.find("a.photoPrev").attr("href");
    var prevModal = $("body").find(prevLink)
    activeModal.modal('hide');
    prevModal.modal('show');
  }
}
function moveRight(){
  var activeModal = $("body").find(".photoModal").not(":hidden");
  if (activeModal.length){
    var nextLink = activeModal.find("a.photoNext").attr("href");
    var nextModal = $("body").find(nextLink)
    activeModal.modal('hide');
    nextModal.modal('show');
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