# JAGSS - Just another generator for static sites

I made this generator when I was working on a site that had a lot of
dictionary type data that I wanted to work into the templates.

Obviously there are already a ton of static site generators out there.
Making this one has been useful for me as I learn more about python,
but hopefully this will be useful to someone else.

## Installation

Once I have a stable 0.1 release, it will be:

    pip install jagss

## Usage

Jagss can be invoked using the command line as follows:

    jagss --source /path/to/source --output /path/to/output

If you wish to use less for css, add an argument for your less file:

    --less /path/to/style.less

Optionally, configuration can be stored in a yaml file:

    jagss --config /path/to/config.yaml

Finally, a server that updates automatically can be run with:

    --server

## Quirks

It's important to know a bit about how jagss works in order to use some of the
power that's included and to avoid using one of the (few) magic variable names.

Markdown files can include metadata in the yaml format at the beginning of the file.

To separate the yaml content from the markdown content, include a line with this text:

    -*-*-*-

Each Jinja2 template file is rendered with a magic variarble called 'site'.

This variable is created when the generator does a first pass of the source folder looking
for markdown files with yaml front matter.