template: textPost.html
title: Inline stdout printing in Python
date: 09Apr2014
-*-*-*-
Because I always forget...

It is sometimes useful to print to stdout inline to simulate the feel of a progress bar. I use this in my script that generates waveform data from a PCM wav file (blog post on that coming soon), because otherwise it can appear to the user that the script is frozen. Here is my starter code that I then tweak to fit the specific use case:

    def print_inline():
        for i in range(20):
            sys.stdout.write("\r" + '-' * i)
            sys.stdout.flush()
            time.sleep(0.3)
        sys.stdout.write("\n")
        sys.stdout.flush()

Note the new line printed and flushed at the end, so the next print command happens on a new line.
