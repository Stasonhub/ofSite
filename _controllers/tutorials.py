
import os
import re
import logging

import blogofile_bf as bf
import shutil
import sys

import argparse
import shutil
import glob

import sets

logger = logging.getLogger("blogofile.post")   

def stripFileLine(line):
    return  line.lstrip(' ').rstrip('\n').rstrip(' ')

class Article:
    def __init__(self,markdown):
        mdfile = open(markdown,'r')
        state = 'begin'
        self.file = os.path.basename(markdown[:markdown.find('.markdown')]) + '.html'
        self.date = ''
        self.title = ''
        self.summary = ''
        self.author = ''
        self.author_site = ''
        self.body = ''
        for line in mdfile:
            line = line.decode('utf-8','replace')
            if state=='begin' and stripFileLine(line) =='---':
                state='header'
                continue
            if state=='header' and line.find('date:')==0:
                self.date = stripFileLine(line[line.find(':')+1:])
                continue
            if state=='header' and line.find('title:')==0:
                self.title = stripFileLine(line[line.find(':')+1:])
                continue
            if state=='header' and line.find('summary:')==0:
                self.summary = stripFileLine(line[line.find(':')+1:])
                continue
            if state=='header' and line.find('author:')==0:
                self.author = stripFileLine(line[line.find(':')+1:])
                continue
            if state=='header' and line.find('author_site:')==0:
                self.author_site = stripFileLine(line[line.find(':')+1:])
                continue
            if state=='header' and stripFileLine(line)=='---':
                state = 'body'
                continue     
            if state=='body':
                self.body = self.body + line       
            

def run():
    classes = []
    directory = "_tutorials"
    documentation = bf.config.controllers.tutorials
    
    categories = []

    dirs = os.listdir(directory)
    dirs.sort()
    for category in dirs:
        if os.path.isdir(os.path.join(directory,category)) and len(os.listdir(os.path.join(directory,category)))>0:
            categories.append(category[category.find("_")+1:])
    
    bf.writer.materialize_template("tutorials.mako", ('tutorials',"index.html"), {'categories':categories} )
    
    for catfolder in os.listdir(directory):
        if not os.path.isdir(os.path.join(directory,catfolder)):
            continue
        articles = []
        category = catfolder[catfolder.find("_")+1:]
        articlesfiles = os.listdir(os.path.join(directory,catfolder));
        articlesfiles.sort()
        for article in articlesfiles:
            file_split = os.path.splitext(article)
            if file_split[1]=='.markdown':
                articleobj = Article(os.path.join(directory,catfolder,article))
                bf.writer.materialize_template("tutorial.mako", (os.path.join('tutorials',category),articleobj.file), {'categories':categories,'article':articleobj} )
                articles.append(articleobj)
            if os.path.isdir(os.path.join(directory,catfolder,article)):
                shutil.copytree(os.path.join(directory,catfolder,article),os.path.join('_site','tutorials',category,article))
        bf.writer.materialize_template("tutorials_category.mako", (os.path.join('tutorials',category),"index.html"), {'categories':categories,'category':category,'articles':articles} )