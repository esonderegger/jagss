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
function zeroPad(n, p, c) {
    var pad_char = typeof c !== 'undefined' ? c : '0';
    var pad = new Array(1 + p).join(pad_char);
    return (pad + n).slice(-pad.length);
}
function getBaseLog(x, y) {
    return Math.log(y) / Math.log(x);
}
function dbFromFloat(floatVal) {
    return getBaseLog(10, floatVal) * 20;
}
function prettyTime(floatSeconds) {
    var outStr = '';
    var hours = Math.floor(floatSeconds / 3600);
    floatSeconds -= hours * 3600;
    var minutes = Math.floor(floatSeconds / 60);
    floatSeconds -= minutes * 60;
    if (hours > 0) {
        outStr += hours + ':' + zeroPad(minutes, 2) + ':';
    } else {
        outStr += minutes + ':';
    }
    outStr += zeroPad(Math.round(floatSeconds), 2);
    return outStr;
}
function makeSvgVideoControls() {
  d3.selectAll('.svgVideoControls').each(function(){
    var containerDiv = d3.select(this);
    var vidElement = d3.select(this).select('video');
    var thissvg = d3.select(this).append('svg');
    thissvg.attr('width', '640');
    thissvg.attr('height', '40');
    thissvg.style('margin-top', "320px")
    thissvg.append('rect').attr("x", 0).attr("y", 0).attr("width", 640).attr("height", 40)
      .style("fill", "rgba(0, 0, 0, 0.5)");
    var thiscounter = thissvg.append('text').attr("x", 110)
      .attr("y", 25).attr("class", "videoCounterText")
      .attr("text-anchor", "end").style("opacity", 0.7)
      .text(prettyTime(0.0));
    thissvg.append('line').attr("x1", 125).attr("x2", 475)
      .attr("y1", 20).attr("y2", 20)
      .style("stroke", "#888").style("stroke-width", "1")
      .style("opacity", 0.7);
    var sliderdrag = d3.behavior.drag()
      .on("dragstart", function(d) {
        d3.select(this).attr("data-dragging", "true");
      })
      .on("drag", function(d) {
        if (125 < d3.event.x && d3.event.x < 475) {
          d3.select(this).attr("cx", d3.event.x);
        } else if (125 >= d3.event.x) {
          d3.select(this).attr("cx", 125);
        } else if (475 <= d3.event.x) {
          d3.select(this).attr("cx", 475);
        }
      })
      .on("dragend", function(d) {
        d3.select(this).attr("data-dragging", "false");
        var playedRatio = (d3.select(this).attr("cx") - 125) / 350;
        vidElement[0][0].currentTime = vidElement.attr("data-duration") * playedRatio;
      });
    var thisslider = thissvg.append('circle').attr("cx", 125).attr("cy", 20).attr("r", 5)
      .style("stroke-width", "3")
      .style("stroke", "#ddd").style("fill", "#aaa")
      .on('mouseover', function(d){
        d3.select(this).transition().style("stroke", "#fff").style("fill", "#ccc");
      })
      .on('mouseout', function(d){
        d3.select(this).transition().style("stroke", "#ddd").style("fill", "#aaa");
      })
      .attr("data-dragging", "false").call(sliderdrag);
    thissvg.append('text').attr("x", 545).attr("y", 25).attr("class", "videoCounterText")
      .attr("text-anchor", "end").style("opacity", 0.7)
      .text(prettyTime(vidElement.attr("data-duration")));
    var playpause = thissvg.append('image').attr("x", 20).attr("y", 5)
      .attr("width", 30).attr("height", 30)
      .style("opacity", 0.7)
      .attr("xlink:href", "//assets.rpy.xyz/svg/play.svg")
      .on("click", function() {
        if (d3.select(this).attr("xlink:href") == "//assets.rpy.xyz/svg/play.svg") {
          d3.select(this).attr("xlink:href", "//assets.rpy.xyz/svg/pause.svg");
          vidElement[0][0].play();
        } else {
          d3.select(this).attr("xlink:href", "//assets.rpy.xyz/svg/play.svg");
          vidElement[0][0].pause();
        }
      })
      .on('mouseover', function(d){
        d3.select(this).transition().style("opacity", 1.0);
      })
      .on('mouseout', function(d){
        d3.select(this).transition().style("opacity", 0.7);
      });
    thissvg.append('image').attr("x", 560).attr("y", 5)
      .attr("width", 30).attr("height", 30)
      .style("opacity", 0.7)
      .attr("xlink:href", "//assets.rpy.xyz/svg/volume-up.svg")
      .on('mouseover', function(d){
        d3.select(this).transition().style("opacity", 1.0);
      })
      .on('mouseout', function(d){
        d3.select(this).transition().style("opacity", 0.7);
      })
      .on("click", function() {
        if (d3.select(this).attr("xlink:href") == "//assets.rpy.xyz/svg/volume-up.svg") {
          d3.select(this).attr("xlink:href", "//assets.rpy.xyz/svg/volume-off.svg");
          vidElement[0][0].volume = 0.0;
        } else {
          d3.select(this).attr("xlink:href", "//assets.rpy.xyz/svg/volume-up.svg");
          vidElement[0][0].volume = 1.0;
        }
      });
    thissvg.append('image').attr("x", 605).attr("y", 5)
      .attr("width", 30).attr("height", 30)
      .style("opacity", 0.7)
      .attr("xlink:href", "//assets.rpy.xyz/svg/arrows-alt.svg")
      .on('mouseover', function(d){
        d3.select(this).transition().style("opacity", 1.0);
      })
      .on('mouseout', function(d){
        d3.select(this).transition().style("opacity", 0.7);
      })
      .on("click", function() {
        if (!document.fullscreenElement &&    // alternative standard method
            !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {  // current working methods
          if (containerDiv[0][0].requestFullscreen) {
            containerDiv[0][0].requestFullscreen();
          } else if (document.documentElement.msRequestFullscreen) {
            containerDiv[0][0].msRequestFullscreen();
          } else if (document.documentElement.mozRequestFullScreen) {
            containerDiv[0][0].mozRequestFullScreen();
          } else if (document.documentElement.webkitRequestFullscreen) {
            containerDiv[0][0].webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
          }
          // enterFullScreen(vidElement, thissvg);
          vidElement.attr("class", "videoIsFullscreen");
          vidElement[0][0].setAttribute("width", window.outerWidth);
          vidElement[0][0].setAttribute("height", window.outerHeight);
          thissvg.style("margin-top", window.outerHeight - 40 + "px");
          thissvg.style("margin-left", window.outerWidth / 2 - 320 + "px");
        } else {
          if (document.exitFullscreen) {
            document.exitFullscreen();
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
          } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
          } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
          }
        }
      });
    vidElement[0][0].addEventListener("timeupdate", function() {
        var playedRatio = vidElement[0][0].currentTime / vidElement.attr("data-duration");
        thiscounter.text(prettyTime(vidElement[0][0].currentTime));
        if (thisslider.attr("data-dragging") == "false") {
          thisslider.attr("cx", (playedRatio * 350) + 125);
        }
    });
    vidElement[0][0].addEventListener("ended", function() {
        playpause.attr("xlink:href", "//assets.rpy.xyz/svg/play.svg");
    });
  });
}
function enterFullScreen(vidSelection, svgSelection) {
  vidSelection.attr("class", "videoIsFullscreen");
  vidSelection[0][0].setAttribute("width", window.outerWidth);
  vidSelection[0][0].setAttribute("height", window.outerHeight);
  svgSelection.style("margin-top", window.outerHeight - 40 + "px");
  svgSelection.style("margin-left", window.outerWidth / 2 - 320 + "px");
}
function ejectFullScreen() {
  d3.selectAll('.svgVideoControls').each(function(){
    var vidSelection = d3.select(this).select('video');
    var svgSelection = d3.select(this).select('svg');
    vidSelection.attr("class", "");
    vidSelection[0][0].setAttribute("width", 640 + "px");
    vidSelection[0][0].setAttribute("height", 360 + "px");
    svgSelection.style("margin-top", 320 + "px");
    svgSelection.style("margin-left", 0 + "px");
  });
}
document.addEventListener("fullscreenchange", function () {
    if (!document.fullscreen) {
      ejectFullScreen();
    }
}, false);
 
document.addEventListener("mozfullscreenchange", function () {
    if (!document.mozFullScreen){
      ejectFullScreen();
    }
}, false);
 
document.addEventListener("webkitfullscreenchange", function () {
    if (!document.webkitIsFullScreen) {
      ejectFullScreen();
    }
}, false);
 
document.addEventListener("msfullscreenchange", function () {
    if (!document.msFullscreenElement) {
      ejectFullScreen();
    }
}, false);

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
