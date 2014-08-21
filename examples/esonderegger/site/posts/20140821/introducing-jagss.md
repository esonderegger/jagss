template: textPost.html
title: Introducing JAGSS
date: 21Aug2014
-*-*-*-
I'm proud to to announce the release of my command line tool for generating static web sites, appropriately titled "Just Another Generator for Static Sites".

I've been using it for this site and the [SRT Labs](http://srtlabs.com) site for a while now, but I finally got around to uploading it to the [Python Package Index](https://pypi.python.org/pypi/jagss/0.0.1).

Full documentation is [here](http://jagss.rpy.xyz).

The source code is available [here](https://github.com/esonderegger/jagss).

The recommended procedure for installation and building a site is:

    sudo pip install jagss

And then to build a site

    mkdir mySite
    cd mySite
    jagss --create sass
    jagss --server 8080

Then edit the markdown, template, scss, etc. files to your heart's content.

Then edit the config.yaml file with your s3 access key, secret key, and bucket name.

Then, in the terminal window, hit ctrl-c to stop the testing server, and deploy with:

    jagss --deploy s3

Enjoy! And please let me know if you're using jagss and what you think about it.
