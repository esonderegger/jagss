# JAGSS - Just another generator for static sites

This is my static site generator. There are many like it, but this one is mine.

I made this generator when I was working on a site that had a lot of
dictionary type data that I wanted to work into the templates.

Obviously there are already a ton of static site generators out there.
Making this one has been useful for me as I learn more about python,
but hopefully this will be useful to someone else.

## Installation

If you just want to use jagss, the simplest way is:

    pip install jagss


If you want to make changes to how jagss works:

    git clone git://github.com/esonderegger/jagss.git
    cd jagss
    mkvirtualenv --no-site-packages jagss
    python setup.py develop

### Dependencies

Performing the steps listed so far requires python, git, and pip.
If you want to want to use less for your css preprocessor, you also need to install
lessc. The easiest way to do that is with the Node Package Manager (npm).

    npm install -g less


## Usage

Jagss is called from the command line. First, to build a jagss project in the current
directory, type:

    jagss --create less

This will create a less folder and a file named folder-name.less inside it, which will
complie to /css/folder-name.css in the staticOutput folder. I recommend using one master
less file that uses @import statements to include other less and css files.

If you do not want to use less for your css, create your project with:

    jagss --create css

Next, a server that updates automatically can be run with:

    jagss --server 8080

Where 8080 is the port number the server will run on.

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
relative path for the file are available at a variable called 'page'. Hopefully the examples
can help explain the logic of this a little better.
