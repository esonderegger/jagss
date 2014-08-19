template: textPost.html
title: FFMPEG settings for PowerPoint Video Playback
date: 20Mar2014
-*-*-*-
If you need to play back video clips in a presentation with the highest possible confidence nothing will go wrong, use [PlaybackPro](http://dtvideolabs.com/PlaybackPro%20Plus.html).

If you can't use PlaybackPro, use Keynote.

If your only option, however, is PowerPoint running on a Windows laptop (as it was for me this week), most combinations of file formats and codecs won't work. This was the ffmpeg command that worked best:

    ffmpeg -i input-video.mp4 -q:a 2 -q:v 4 -vcodec wmv2 -acodec wmav2 output-video.avi

Note that even though the windows media codecs were used, I had the best luck with putting it all in an avi wrapper. Just for completeness, this was working in PowerPoint 2010 on Windows 7.
