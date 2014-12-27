template: default.html
title: JAGSS!
-*-*-*-
This is my static site generator. There are many like it, but this one is mine.

Jagss creates html from [markdown](http://daringfireball.net/projects/markdown/)
and [yaml](http://www.yaml.org/) data and uses the [less](http://lesscss.org/)
or [sass](http://sass-lang.com/) preprocessors to create css. Data from the whole
site is available to html files with [Jinja2](http://jinja.pocoo.org) templating
syntax. Jagss can run an http testing server, watching the source files for changes
and updating the site accordingly. Jagss can then deploy the static site via sftp
or to an [Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html)
bucket, only updating those files that have been changed.

I made this generator when I was working on a site that had a lot of
dictionary type data that I wanted to work into the templates.

The source code is available [on github](https://github.com/esonderegger/jagss).

Obviously there are already a ton of static site generators out there.
Making this one has been useful for me as I learn more about python,
but hopefully this will be useful to someone else.

## Installation

If you just want to use jagss, the simplest way is:

    pip install jagss


If you want to make changes to how jagss works:

    git clone git://github.com/esonderegger/jagss.git
    cd jagss
    virtualenv jagss_env
    . jagss_env/bin/activate
    python setup.py develop

### Preprocessors

If you want to use jagss with a css preprocessor (and you should - they're awesome!),
you will need to install the preprocessor of your choice.

To install less, the easiest way is to use the
[Node Package Manager](https://www.npmjs.org/) (npm):

    npm install -g less

To install sass, install it via its ruby gem:

    gem install sass

## Usage

Jagss is called from the command line. First, to build a new jagss project, make
a new folder and cd into it:

    mkdir projectname
    cd projectname

Then, to create your project structure, type:

    jagss --create less

Or, if you prefer to use sass:

    jagss --create sass

Or, if you don't want to use a css preprocessor:

    jagss --create css

If you choose to go the preprocessor route, this will create a less or a sass 
folder and a file named folder-name.less/scss inside it, which will compile to
/css/folder-name.css in the staticOutput folder. I recommend using one master
file that uses @import statements to include other less and css files.

Next, a server that updates automatically can be run with:

    jagss --server 8080

Where 8080 is the port number the server will run on.

Then, point your browser at [http://localhost:8080](http://localhost:8080), edit your
site, and click 'refresh' to see your changes. To stop the server, hit ctrl + c.

When you are happy with the state of your static site, jagss can deploy to either sFTP
or to an Amazon S3 bucket. To do this, enter the appropriate values in the config.yaml
file and run

    jagss --deploy sftp

or

    jagss --deploy s3

## Quirks

It's important to know a bit about how jagss works in order to use some of the
power that's included and to avoid using one of the (few) magic variable names.

Markdown files can include metadata in the yaml format at the beginning of the file.

To separate the yaml content from the markdown content, include a line with this text:

    -*-*-*-

Each Jinja2 template file is rendered with a magic variarble called 'site'.

This variable is created when the generator does a first pass of the source folder looking
for markdown files with yaml front matter as well as yaml files.

Individual markdown files are also rendered to html according to the 'template' value in the yaml
content at the top of the file. The yaml data from that file, as well as values for the url and
relative path for the file are available at a variable called 'page'. For markdown files, the
rendered html is available at page.html. There is also a reserved variable named 'type', which
will be used in future updates.

For a very basic example, you might have a jagss project organized like this:

    jagsstest/
        sass/
            jagsstest.scss
        site/
            index.html
            stuff/
                thing1.md
                thing2.md
                thing3.md
        staticOutput/
        templates/
            default.html

default.html could be as simple as:

    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>{{ page.title }}</title>
        </head>
        <body>
            {{ page.html }}
        </body>
    </html>

The thing1.md, thing2.md, and thing3.md could look something like:

    template: default.html
    title: Thing Number 1
    -*-*-*-
    # Thing Number 1

    Some more in depth content about the first thing would go here.

Then, for index.html to link to all the things in the stuff folder, it would be:

    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>A Very Basic Site</title>
        </head>
        <body>
            <h1>Some things:</h1>
            {% for thing in site['/stuff'] %}
            <p><a href="{{ thing.url }}">{{ thing.title }}</a></p>
            {% endfor %}
        </body>
    </html>

Note that the naming of the "stuff" folder and all the variables in the yaml content
(except for 'html', 'name', 'relativePath', 'type', and 'url') can be whatever you
want them to be.

Hopefully the full site examples can help explain the logic of this a little better.

Enjoy! Please get [get in touch](https://rpy.xyz/contact.html) with any comments
or suggestions for improvements.
