# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import markdown2
import os
import shutil
import subprocess
import yaml
import json


def renderSiteOuput(sourceDir, outputBase, templatesDir, siteData):
    for root, dirs, files in os.walk(sourceDir):
        for f in files:
            folderID = root[len(sourceDir):]
            outputDir = outputBase + folderID
            if f[:1] != '.':
                renderSiteFile(root, f, outputDir, templatesDir, siteData,
                               folderID)


def populateSiteData(location):
    siteData = {'/': []}
    for root, dirs, files in os.walk(location):
        folderID = '/' + root[len(location) + 1:]
        siteData[folderID] = []
        for f in files:
            if os.path.splitext(f)[1] == '.md':
                mdData = dictFromMarkdown(os.path.join(root, f), folderID)
                siteData[folderID].append(mdData)
            if os.path.splitext(f)[1] == '.yaml':
                ymlData = dictFromYaml(os.path.join(root, f), folderID)
                siteData[folderID].append(ymlData)
        for folder in dirs:
            yamlData = {'relativePath': folderID}
            yamlData['type'] = 'folder'
            yamlData['name'] = folder
            siteData[folderID].append(yamlData)
    return siteData


def dictFromMarkdown(markdownPath, folderID):
    separator = '-*-*-*-\n'
    rawFile = open(markdownPath).read()
    separatorIndex = rawFile.find(separator)
    if separatorIndex > -1:
        yamlData = yaml.load(rawFile[:separatorIndex])
        mdData = rawFile[separatorIndex + len(separator):]
        htmlData = markdown2.markdown(mdData)
        yamlData['html'] = htmlData
        yamlData['type'] = 'yaml+markdown'
    else:
        yamlData = {'html': markdown2.markdown(rawFile)}
        yamlData['type'] = 'markdown'
    yamlData['relativePath'] = folderID
    yamlData['url'] = folderID + '/'
    filename = os.path.basename(markdownPath)
    yamlData['url'] += os.path.splitext(filename)[0] + '.html'
    return yamlData


def dictFromYaml(yamlPath, folderID):
    yamlData = yaml.load(open(yamlPath).read())
    yamlData['relativePath'] = folderID
    yamlData['type'] = 'yaml'
    if 'template' in yamlData:
        yamlData['url'] = folderID + '/'
        filename = os.path.basename(yamlPath)
        yamlData['url'] += os.path.splitext(filename)[0] + '.html'
    return yamlData


def renderMarkdownFile(sourceDir, filename, newDir, templatesDir, siteData,
                       folderID):
    newFilename = os.path.splitext(filename)[0] + '.html'
    newPath = os.path.join(newDir, newFilename)
    mdData = dictFromMarkdown(os.path.join(sourceDir, filename), folderID)
    if 'template' in mdData:
        jinjaEnv = Environment(loader=FileSystemLoader([templatesDir]))
        template = jinjaEnv.get_template(mdData['template'])
        output = template.render(page=mdData, site=siteData)
        with open(newPath, 'w') as f:
            f.write(output.encode('utf-8'))
    else:
        with open(newPath, 'w') as f:
            f.write(mdData['html'].encode('utf-8'))
    return newPath


def renderYamlFile(sourceDir, filename, newDir, templatesDir, siteData,
                   folderID):
    newFilename = os.path.splitext(filename)[0] + '.html'
    newPath = os.path.join(newDir, newFilename)
    yamlData = dictFromYaml(os.path.join(sourceDir, filename), folderID)
    if 'template' in yamlData:
        jinjaEnv = Environment(loader=FileSystemLoader([templatesDir]))
        template = jinjaEnv.get_template(yamlData['template'])
        output = template.render(page=yamlData, site=siteData)
        with open(newPath, 'w') as f:
            f.write(output.encode('utf-8'))
    else:
        return False
    return newPath


def renderHtmlFile(sourceDir, filename, newDir, templatesDir, siteData,
                   folderID):
    newPath = os.path.join(newDir, filename)
    jinjaFLS = FileSystemLoader([templatesDir, sourceDir])
    jinjaEnv = Environment(loader=jinjaFLS)
    template = jinjaEnv.get_template(filename)
    output = template.render(site=siteData)
    with open(newPath, 'w') as f:
        f.write(output.encode('utf-8'))
    return newPath


def renderSiteFile(sourceDir, filename, outputDir, templatesDir, siteData,
                   folderID):
    extension = os.path.splitext(filename)[1]
    currentPath = os.path.join(sourceDir, filename)
    source_length = len(sourceDir) + 1
    newDir = os.path.join(outputDir, sourceDir[source_length:])
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    if extension == '.html':
        newPath = renderHtmlFile(sourceDir, filename, newDir,
                                 templatesDir, siteData, folderID)
    elif extension == '.md':
        newPath = renderMarkdownFile(sourceDir, filename, newDir,
                                     templatesDir, siteData, folderID)
    elif extension == '.yaml':
        newPath = renderYamlFile(sourceDir, filename, newDir,
                                 templatesDir, siteData, folderID)
    else:
        newPath = os.path.join(newDir, filename)
        shutil.copy2(currentPath, newDir)
    return newPath


def renderLessFile(lessFile, outputDir):
    basename = os.path.basename(lessFile)
    cssDir = os.path.join(outputDir, 'css')
    if not os.path.exists(cssDir):
        os.makedirs(cssDir)
    cssFile = os.path.splitext(basename)[0] + '.css'
    outputFile = os.path.join(cssDir, cssFile)
    subCall = ['lessc', '-x', lessFile, outputFile]
    subprocess.call(subCall)
    return outputFile


def renderSassFile(sassFile, outputDir):
    basename = os.path.basename(sassFile)
    cssDir = os.path.join(outputDir, 'css')
    if not os.path.exists(cssDir):
        os.makedirs(cssDir)
    cssFile = os.path.splitext(basename)[0] + '.css'
    outputFile = os.path.join(cssDir, cssFile)
    subCall = ['sass', '--style', 'compressed', sassFile, outputFile]
    subprocess.call(subCall)
    return outputFile


def deleteFolderContents(folder_path):
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)


def buildStaticSite(sourceDir, outputDir, templatesDir=False, lessFile=False,
                    sassFile=False, printSiteData=False):
    deleteFolderContents(outputDir)
    siteData = populateSiteData(sourceDir)
    if printSiteData:
        print json.dumps(siteData, sort_keys=True, indent=4)
    if not templatesDir:
        templatesDir = os.path.join(os.path.dirname(sourceDir), 'templates')
    renderSiteOuput(sourceDir, outputDir, templatesDir, siteData)
    if lessFile:
        renderLessFile(lessFile, outputDir)
    if sassFile:
        renderSassFile(sassFile, outputDir)
