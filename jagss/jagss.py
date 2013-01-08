#!/usr/bin/env python

import argparse
from jinja2 import Environment, FileSystemLoader
import markdown2
import os
import shutil
import SimpleHTTPServer
import SocketServer
import subprocess
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import yaml


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
                yamlAndMarkdown = rawFile.split('---\n')
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
    yamlAndMarkdown = rawFile.split('-*-*-\n')
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
    subCall = '/usr/local/share/npm/bin/lessc -x '
    subCall += lessFile + ' > ' + outputFile
    subprocess.call(subCall, shell=True)
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
    if not templatesDir:
        templatesDir = os.path.join(os.path.dirname(sourceDir), 'templates')
    renderSiteOuput(sourceDir, outputDir, templatesDir, siteData)
    if lessFile:
        renderLessFile(lessFile, outputDir)


class usmbServerThread(threading.Thread):
    def __init__(self, port, outputDir):
        threading.Thread.__init__(self)
        self.PORT = port
        self.outputDir = outputDir
        self.Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.httpd = SocketServer.TCPServer(("", self.PORT), self.Handler)

    def run(self):
        os.chdir(self.outputDir)
        print "serving at port", self.PORT
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()


class usmb_handler(FileSystemEventHandler):
    def __init__(self, configDict):
        FileSystemEventHandler.__init__(self)
        self.configDict = configDict

    def on_any_event(self, event):
        print 'rebuilding static site...'
        buildStaticSite(self.configDict['sourceDir'],
                        self.configDict['outputDir'],
                        self.configDict['templatesDir'],
                        self.configDict['lessFile'])
        print 'rebuild complete.\n'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="specify config file")
    parser.add_argument("--source", help="specify source directory")
    parser.add_argument("--output", help="specify output directory")
    parser.add_argument("--templates", help="specify template directory")
    parser.add_argument("--less", help="specify less css file")
    parser.add_argument("--server", help="run a server for testing")
    args = parser.parse_args()
    if args.config:
        configDict = yaml.load(file(args.config, 'r'))
    elif args.source and args.output:
        configDict = {'sourceDir': args.source, 'outputDir': args.output}
        configDict['templatesDir'] = args.templates
        configDict['lessFile'] = args.less
    else:
        configDict = {'error': 'input/outpu]t directories not specified.'}
    buildStaticSite(configDict['sourceDir'], configDict['outputDir'],
                    configDict['templatesDir'], configDict['lessFile'])
    if args.server:
        event_handler = usmb_handler(configDict)
        observer = Observer()
        masterDir = os.path.dirname(configDict['sourceDir'])
        observer.schedule(event_handler, path=masterDir, recursive=True)
        usmbHttpServer = usmbServerThread(8000, configDict['outputDir'])
        observer.start()
        usmbHttpServer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            usmbHttpServer.shutdown()
            print 'stopping testing server.\n'
        observer.join()
