from jinja2 import Environment, FileSystemLoader
import markdown2
import os
import shutil
import subprocess
import yaml
# import json  #just used for pretty-printing


def renderSiteOuput(sourceDir, outputBase, templatesDir, siteData):
    for root, dirs, files in os.walk(sourceDir):
        for file in files:
            outputDir = outputBase + root[len(sourceDir):]
            if file[:1] != '.':
                renderSiteFile(root, file, outputDir, templatesDir, siteData)


def populateSiteData(location):
    siteData = {'/': []}
    for root, dirs, files in os.walk(location):
        folderID = '/' + root[len(location) + 1:]
        siteData[folderID] = []
        for file in files:
            if os.path.splitext(file)[1] == '.md':
                rawFile = open(os.path.join(root, file)).read()
                yamlAndMarkdown = rawFile.split('-*-*-*-\n')
                yamlData = yaml.load(yamlAndMarkdown[0])
                htmlData = markdown2.markdown(yamlAndMarkdown[1])
                yamlData['url'] = folderID + '/'
                yamlData['url'] += os.path.splitext(file)[0] + '.html'
                yamlData['html'] = htmlData
                siteData[folderID].append(yamlData)
    return siteData


def renderMarkdownFile(sourceDir, file, newDir, templatesDir, siteData):
    newFilename = os.path.splitext(file)[0] + '.html'
    newPath = os.path.join(newDir, newFilename)
    rawFile = open(os.path.join(sourceDir, file)).read()
    yamlAndMarkdown = rawFile.split('-*-*-*-\n')
    if len(yamlAndMarkdown) == 2:
        yamlData = yaml.load(yamlAndMarkdown[0])
        htmlData = markdown2.markdown(yamlAndMarkdown[1])
        yamlData['content'] = htmlData
        if 'template' in yamlData:
            jinjaEnv = Environment(loader=FileSystemLoader([templatesDir]))
            template = jinjaEnv.get_template(yamlData['template'])
            output = template.render(page=yamlData, site=siteData)
            with open(newPath, 'w') as f:
                f.write(output.encode('utf-8'))
        else:
            with open(newPath, 'w') as f:
                f.write(htmlData.encode('utf-8'))
    else:
        htmlData = markdown2.markdown(rawFile)
        with open(newPath, 'w') as f:
            f.write(htmlData.encode('utf-8'))
    return newPath


def renderHtmlFile(sourceDir, file, newDir, templatesDir, siteData):
    newPath = os.path.join(newDir, file)
    jinjaEnv = Environment(
        loader=FileSystemLoader([templatesDir, sourceDir]))
    template = jinjaEnv.get_template(file)
    output = template.render(site=siteData)
    with open(newPath, 'w') as f:
        f.write(output.encode('utf-8'))
    return newPath


def renderSiteFile(sourceDir, file, outputDir, templatesDir, siteData):
    extension = os.path.splitext(file)[1]
    currentPath = os.path.join(sourceDir, file)
    source_length = len(sourceDir) + 1
    newDir = os.path.join(outputDir, sourceDir[source_length:])
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    if extension == '.html':
        newPath = renderHtmlFile(sourceDir, file, newDir,
                                 templatesDir, siteData)
    elif extension == '.md':
        newPath = renderMarkdownFile(sourceDir, file, newDir,
                                     templatesDir, siteData)
    else:
        newPath = os.path.join(newDir, file)
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


def deleteFolderContents(folder_path):
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)


def buildStaticSite(sourceDir, outputDir, templatesDir=False, lessFile=False):
    deleteFolderContents(outputDir)
    siteData = populateSiteData(sourceDir)
    # print json.dumps(siteData, sort_keys=True, indent=4)
    if not templatesDir:
        templatesDir = os.path.join(os.path.dirname(sourceDir), 'templates')
    renderSiteOuput(sourceDir, outputDir, templatesDir, siteData)
    if lessFile:
        renderLessFile(lessFile, outputDir)
