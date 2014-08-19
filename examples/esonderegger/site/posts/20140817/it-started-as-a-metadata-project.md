template: textPost.html
title: It Started as a Metadata Project...
date: 17Aug2014
-*-*-*-
This is the story of how the Marine Band Digital Archives Came into being. I really didn't mean for it to be my signature contribution to "The President's Own". It was just a project I kept working on that continued to grow.

When I joined the band in 2006, we had a pretty established routine for keeping the recordings we made of the band's public performances. We would record the concert using a variety of tools we had at our disposal (at the time, I believe we were using an Alesis Masterlink recording as 24/44.1), then edit that recording to remove excessive gaps, fade out applause, etc. using [SADiE](http://www.sadie.com/), and burn an "archival master" to CD-R. Several copies of this CD-R would be made, including ones for soloists and conductors. There were always at least three copies made: one that stayed in the recording lab office, one that went in the hallway by the directors' offices, and one that went in a filing cabinet in our library.

After editing the recording, we would catalog it in the library's database using Selago Design's [Mimsy XG](http://www.selagodesign.com/portfolio/mimsyxg.php). A CD would have an accession number like USMB-CD-11219 (numbers above 10000 indicated the recording was made by the band) and individual tracks would have accession numbers like USMB-CD-11219.5. The "CD" in that numbering scheme indicated the medium was compact disc, whereas "RR" was for reel to reel recordings, "DT" was for Digital Audio Tape cassettes, and "DB" was for audio stored on betamax cassettes. Because we could link to sheet music and event records already in the library's database, it took relatively little effort to associate extensive metadata with each audio track record.

In 2007, we got a pretty good scare when we noticed that some of the earliest CD-R recordings in our archives were starting to have trouble playing back. Even though most of these discs had been written to "archival gold" quality media, they were producing unrecoverable read errors at an alarming rate. We (At this point, I should recognize Karl Jackson, the Marine Band's chief recording engineer and my boss from 2006-2014. Any time I use the word "we" in this post, I'm referring to a joint effort between the two of us.) decided it was time to move as many of our recording as possible to spinning disk and consider the digital file to be our "master" copy. Karl took the lead on selecting the [Netgear ReadyNAS](http://www.readynas.com/) as our storage appliance, creating presets in Exact Audio Copy, and ripping the discs in our archives into wav files. There would be one folder per album, named for the album's accession number, and each track would be saved as a PCM wav file with a name like USMB-CD-11219_05.wav.

The ReadyNAS was placed on our local network, so we no longer had to grab a physical copy of a CD if we wanted to do anything with it, like make an excerpt of a track available as reference for someone. However, one thing that bothered me was that if the file was looked at in isolation, there was nothing about it that told us anything about the recording itself. We might not know the name of the piece, the composer, the date of the performance, the venue, etc. For that we would have to log into the library's database and do a search.

Unfortunately, in addition to being slow and frequently off-line, the library's database server on was on the ".mil" side of our network. This meant there was no way we'd be allowed to access the data directly. However, we had recently been taught a short class on how to use Crystal Reports with this data. I noticed Crystal Reports had an option to export a report as a .csv file and I saw my opening.

I should point out that at the time, our archives consisted of more than 20,000 audio track records and have grown considerably since then. Doing anything with this data manually or re-keying any metadata was out of the question. I thought it would be really cool if we could have iTunes libraries on a few key machines with all of our recordings in mp3 format on them. Sadly, I don't have a lot of information about when exactly milestones occurred. My best guess is this all started around the fall of 2008.

I had done some scripting with audio data while I was working at the Salem Radio Network. Fred Gleason, author of the [Rivendell Radio Automation System](http://www.rivendellaudio.org/) had shown me enough to learn how to automate the process of removing the silence from our show recordings (we were on a hard clock, so commercial breaks always happened at the same time every day) and convert them to mp3, so I could have old shows available to me as digital files. In addition, his development of Rivendell made an impression on me for how open source can fit well even at for-profit organizations. I naively thought creating a network share with all our recordings stored as mp3 files with relevant metadata in the files' ID3 tags would be a matter of writing a few shell scripts. Perhaps something along the lines of this:

    #!/bin/bash
    folders=/mnt/wavfiles/*
    for folder in $folders
    do
      files=/mnt/wavfiles/$folder/*
      for f in $files
      do
        title={some magic to get track title here}
        album={similar magic to get album title here}
        lame -V2 --tt $title --tl $album /mnt/wavfiles/$folder/$f /mnt/mp3files/$folder/${f%.*}.mp3
      done
    done

What I quickly learned was that our data was dirty. There were folders in "wavfolders" (I'm changing names out of an abundance of caution) that contained non-audio data. There were audio files that hadn't been cataloged in the library database. There were records in the database for audio that hadn't been digitized yet. There were audio files that didn't conform to our naming standards. There were instances where the track number on the CD, which became the track number in the file name, didn't match the track number in the database. I needed better exception handling than a long series of if/else statements.

I needed python. I just didn't know it yet.

In the above code snippet, I mentioned getting the track metadata involved some magic. After a few failed attempts at parsing the csv files generated by crystal reports inside of the bash script, I remembered that phpmyadmin had the option to import a csv file into a MySQL table. I had used phpmyadmin for setting up some Wordpress sites, but not for anything in depth. I was already using a recycled powermac G4 running Ubuntu server for the scripting, so setting up MySQL for this purpose wasn't crazy or difficult. The phpmyadmin/MySQL combination allowed me to avoid doing a of ton finding, parsing, and escaping data from text files - skills I didn't yet have.

It was around this time the "eureka!" moment happened. I knew people used php and MySQL to create database-driven websites. I had even built some, if you call tweaking Wordpress themes "building". It was mostly out of laziness that I thought "wouldn't it be cool if I could look up an audio record from a web browser on our LAN and then click on a link to the matching mp3 file?" I already had all the necessary ingredients: always-on linux server, a MySQL table with our entire catalog in rows and columns, all our audio encoded as mp3 sitting on a mounted file system. The first mock-up took only a few hours, after I had been spending weeks wrestling with all the edge cases of getting everything to encode properly.

From a user-experience perspective, I knew I wanted to stay as far away from power-user features as possible. For one thing, we already had about as powerful a search interface as one could ask for in MimsyXG with librarians and recording engineers trained in the use of wildcard symbols and boolean logic. If we wanted to find out how many recordings of Stars and Stripes Forever we had that were performed at George Mason University from 1990-1995, we already had the perfect tool for the job. A single search box and a dropdown for sorting seemed like the right compromise between simplicity and power. Deciding how to parse the string from the search box was another matter. I found this snippet of code, which I think was in production from around 2011 through 2013:

    function getQuerySearch($srch){
        $totalQuery = "";
        $searchTerms = explode(" ", $srch);
        for ($a = 0; $a < count($searchTerms); $a++){
            $wildsearch="%".$searchTerms[$a]."%";
            $search=mysql_real_escape_string($wildsearch);
            $subQuery = "(Access LIKE '$search' || Title LIKE '$search' || Album LIKE '$search' || Composer LIKE '$search' || Year LIKE '$search' || Soloist LIKE '$search')";
            $totalQuery = $totalQuery.$subQuery;
            if (($a + 1) < count($searchTerms)){
                $totalQuery = $totalQuery." && ";
            }
        }
        return $totalQuery;
    }

My best guess is that a real website began to take shape around the spring of 2010. At this time I should note that this was always a side-project that took a back seat to the everyday functions of recording concerts, rehearsals, and our annual recording sessions. Looking back, I'm amazed Karl let me spend so much time with my eyes glued to a text editor, without a truly clear picture of what exactly I was working on. Every now and then I'd pop up and say "wanna see something cool?" and show him some incomplete feature that had the potential to make our lives easier. Eventually it got to the point where I needed a beta tester who wasn't an engineer. Our three directors are by far the heaviest users of our archives. They need to listen to archived recordings when choosing what pieces to program on their concerts, what recordings to release to the public, and to know how their recent performances sounded. I first went to then-Major Jason Fettig, sheepishly asking "I've been building this website... I think you'll like it, but I've definitely still got some bugs to work out. Do you think you could try it for a few weeks and tell me how it breaks when it does?" I think it took about a day before Colonel Colburn approached me and asked "How can I get access to this site Major Fettig has been using?" At that point I knew I was on to something.

From then on, the updates were more incremental. We set up a domain name and configured our firewall so people could access the site from outside our LAN. I shamelessly copied Google's live updating of the search results as the user typed in the search box feature. Video search and playback was added. I learned python and replaced the bash scripts with cleaner python ones. I started using object relational mappers (first python-storm, then SQLAlchemy) instead of creating queries directly. A pared down version of the site was made for mobile phones. Eventually, the php code became too ungainly and I started fresh with a python back-end built using [Flask](http://flask.pocoo.org/). I stopped running the server on old recycled Macs and started running it inside VirtualBox VMs hosted on (slightly) more recent hardware. I replaced MySQL with PostgreSQL. We had been storing our passwords in plain text (not as bad as it sounds - we weren't keeping any personal information and users didn't pick their passwords. The worst thing an attacker could do with that data is download recordings we didn't want to be public.), so I built the new version using bcrypt to hash and salt passwords. In 2010, Flash was the primary way to embed audio or video in a web page; thankfully by the time the rewrite was ready, I only had to support html5. The live search function uses jQuery instead of plain javascript. The mobile version of the site was scrapped and the new site uses Bootstrap's mobile-responsive features. I wrote some code to create waveforms from the archived and display it in the browser's audio player with d3.js that I am super-proud of.

I could write blog posts on each of those updates about how and why certain decisions were made, but the fact that the whole thing exists at all still amazes me. I get to take a lot of the credit for having the creativity to conceive of a web-based search for our entire archives and the stubbornness to see it through. However it never could have happened if the Marine Band didn't have a long tradition of keeping its library well-organized (dating back to Sousa), or my boss didn't have the trust that I wasn't wasting my time, or the directors didn't provide encouragement and feedback, or the musicians weren't creating music that was worth preserving in the first place. I feel lucky to have been in the right place at the right time to build it, and to have found my new passion along the way.

Thanks for reading!
