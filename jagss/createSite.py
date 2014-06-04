# -*- coding: utf-8 -*-

import os


def createNewSite(location, cssType):
    print 'creating new jagss site...'
    siteName = os.path.split(location)[1]
    sitePath = os.path.join(location, 'site')
    outputPath = os.path.join(location, 'staticOutput')
    templatesPath = os.path.join(location, 'templates')
    configPath = os.path.join(location, 'config.yaml')
    dirsToCreate = [sitePath, outputPath, templatesPath]
    jinjaPath = os.path.join(templatesPath, 'default.html')
    indexPath = os.path.join(sitePath, 'index.md')
    if cssType == 'less':
        lessDirPath = os.path.join(location, 'less')
        cssFilePath = os.path.join(lessDirPath, siteName + '.less')
        dirsToCreate.append(lessDirPath)
    elif cssType == 'sass':
        sassDirPath = os.path.join(location, 'sass')
        cssFilePath = os.path.join(sassDirPath, siteName + '.scss')
        dirsToCreate.append(sassDirPath)
    else:
        cssDirPath = os.path.join(sitePath, 'css')
        cssFilePath = os.path.join(cssDirPath, siteName + '.css')
        dirsToCreate.append(cssDirPath)
    for dirPath in dirsToCreate:
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
    if not os.path.exists(configPath):
        createConfigFile(location, cssType)
    if not os.path.exists(cssFilePath):
        createCssFile(cssFilePath)
    if not os.path.exists(jinjaPath):
        createTemplateFile(jinjaPath, siteName)
    if not os.path.exists(indexPath):
        createMarkdownFile(indexPath)


def createConfigFile(cwd, cssType):
    """creates a config.yaml file with default values inside the cwd"""
    siteName = os.path.split(cwd)[1]
    conf = 'sourceDir: ' + os.path.join(cwd, 'site') + '\n'
    conf += 'outputDir: ' + os.path.join(cwd, 'staticOutput') + '\n'
    conf += 'templatesDir: ' + os.path.join(cwd, 'templates') + '\n'
    if cssType == 'less':
        lessPath = os.path.join(cwd, 'less')
        conf += 'lessFile: ' + os.path.join(lessPath, siteName + '.less')
        conf += '\n'
        conf += 'sassFile: False\n'
    elif cssType == 'sass':
        conf += 'lessFile: False\n'
        sassPath = os.path.join(cwd, 'sass')
        conf += 'sassFile: ' + os.path.join(sassPath, siteName + '.scss')
        conf += '\n'
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


def createCssFile(cssPath):
    """creates a default css or less file at the specified path."""
    css = """body {
    width: 600px;
    margin: 150px auto;
    font-family: sans-serif;
    background-color: #008209;
    color: #eee;
}
"""
    with open(cssPath, 'w') as f:
        f.write(css.encode('utf-8'))


def createTemplateFile(templatePath, siteName):
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
""" % (siteName)
    with open(templatePath, 'w') as f:
        f.write(template.encode('utf-8'))


def createMarkdownFile(markdownPath):
    """creates a default markdown file at the specified path."""
    md = """template: default.html
title: JAGSS!
-*-*-*-
# Welcome to JAGSS!

This is the default page for a new JAGSS project. Modify the template
and site files to get started.
"""
    with open(markdownPath, 'w') as f:
        f.write(md.encode('utf-8'))
