# -*- coding: utf-8 -*-

import os


def create_new_site(location, css_type):
    print 'creating new jagss site...'
    site_name = os.path.split(location)[1]
    site_path = os.path.join(location, 'site')
    output_path = os.path.join(location, 'staticOutput')
    templates_path = os.path.join(location, 'templates')
    config_path = os.path.join(location, 'config.yaml')
    dirs_to_create = [site_path, output_path, templates_path]
    jinja_path = os.path.join(templates_path, 'default.html')
    index_path = os.path.join(site_path, 'index.md')
    if css_type == 'less':
        less_dir_path = os.path.join(location, 'less')
        css_file_path = os.path.join(less_dir_path, site_name + '.less')
        dirs_to_create.append(less_dir_path)
    elif css_type == 'sass':
        sass_dir_path = os.path.join(location, 'sass')
        css_file_path = os.path.join(sass_dir_path, site_name + '.scss')
        dirs_to_create.append(sass_dir_path)
    else:
        css_dir_path = os.path.join(site_path, 'css')
        css_file_path = os.path.join(css_dir_path, site_name + '.css')
        dirs_to_create.append(css_dir_path)
    for dir_path in dirs_to_create:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    if not os.path.exists(config_path):
        create_config_file(location, css_type)
    if not os.path.exists(css_file_path):
        create_css_file(css_file_path)
    if not os.path.exists(jinja_path):
        create_template_file(jinja_path, site_name)
    if not os.path.exists(index_path):
        create_markdown_file(index_path)


def create_config_file(cwd, css_type):
    """creates a config.yaml file with default values inside the cwd"""
    site_name = os.path.split(cwd)[1]
    conf = 'sourceDir: site\n'
    conf += 'outputDir: staticOutput\n'
    conf += 'templatesDir: templates\n'
    if css_type == 'less':
        conf += 'lessFile: less/' + site_name + '.less\n'
        conf += 'sassFile: False\n'
    elif css_type == 'sass':
        conf += 'lessFile: False\n'
        conf += 'sassFile: sass/' + site_name + '.scss\n'
    else:
        conf += 'lessFile: False\n'
        conf += 'sassFile: False\n'
    conf += '\n# deployment credentials go here:\n'
    conf += 'sftpAddress: none\n'
    conf += 'sftpUsername: none\n'
    conf += 'sftpPassword: none\n'
    conf += 'sftpDirectory: none\n'
    conf += 's3AccessKey: none\n'
    conf += 's3SecretKey: none\n'
    conf += 's3BucketName: none\n'
    with open(os.path.join(cwd, 'config.yaml'), 'w') as f:
        f.write(conf.encode('utf-8'))


def create_css_file(css_path):
    """creates a default css or less file at the specified path."""
    css = """body {
    width: 600px;
    margin: 150px auto;
    font-family: sans-serif;
    background-color: #008209;
    color: #eee;
}
"""
    with open(css_path, 'w') as f:
        f.write(css.encode('utf-8'))


def create_template_file(template_path, site_name):
    """creates a default jinja2 template at the specified path."""
    template = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ page.title }}</title>
        <link href="/css/%s.css" rel="stylesheet" />
    </head>
    <body>
        {{ page.html }}
    </body>
</html>
""" % (site_name)
    with open(template_path, 'w') as f:
        f.write(template.encode('utf-8'))


def create_markdown_file(markdown_path):
    """creates a default markdown file at the specified path."""
    md = """template: default.html
title: JAGSS!
-*-*-*-
# Welcome to JAGSS!

This is the default page for a new JAGSS project. Modify the template
and site files to get started.
"""
    with open(markdown_path, 'w') as f:
        f.write(md.encode('utf-8'))
