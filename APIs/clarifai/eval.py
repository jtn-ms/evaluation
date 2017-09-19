# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 23:29:16 2017

@author: Frank

api-key "acec626c1ccb45efab8748fd4bb4db05kjy"
"""

import os
import sys
import platform
from pprint import pprint
from configparser import ConfigParser
from builtins import input
from subprocess import call

from clarifai.rest import ClarifaiApp

from argparse import ArgumentParser

from gooey import Gooey

def setup(api_key):
    '''
    write back CLARIFAI_API_KEY to config file
    config file is at ~/.clarifai/config
    '''

    os.environ['CLARIFAI_API_KEY'] = api_key
    homedir = os.environ['HOMEPATH'] if platform.system() == 'Windows' else os.environ['HOME']
    CONF_DIR=os.path.join(homedir, '.clarifai')
    CONF_DIR="C:" + CONF_DIR#frank-todo
    
    if not os.path.exists(CONF_DIR):
        os.mkdir(CONF_DIR)
    elif not os.path.isdir(CONF_DIR):
        raise Exception('%s should be a directory for configurations' % CONF_DIR)

    CONF_FILE=os.path.join(CONF_DIR, 'config')

    parser = ConfigParser()
    parser.optionxform = str

    if os.path.exists(CONF_FILE):
        parser.readfp(open(CONF_FILE, 'r'))

    if not parser.has_section('clarifai'):
        parser.add_section('clarifai')

    # remove CLARIFAI_APP_ID
    if parser.has_option('clarifai', 'CLARIFAI_APP_ID'):
        parser.remove_option('clarifai', 'CLARIFAI_APP_ID')

    # remove CLARIFAI_APP_SECRET
    if parser.has_option('clarifai', 'CLARIFAI_APP_SECRET'):
        parser.remove_option('clarifai', 'CLARIFAI_APP_SECRET')

    parser.set('clarifai', 'CLARIFAI_API_KEY', api_key)

    with open(CONF_FILE, 'w') as fdw:
        parser.write(fdw)

def process_url(Url):
    setup('acec626c1ccb45efab8748fd4bb4db05')
    app = ClarifaiApp()
    model = app.models.get('general-v1.3')
    response = model.predict_by_url(url=Url)

    concepts = response['outputs'][0]['data']['concepts']
    for concept in concepts:
        print(concept['name'], concept['value'])

def process_image(fullpath):
    setup('acec626c1ccb45efab8748fd4bb4db05')
    app = ClarifaiApp()
    model = app.models.get('general-v1.3')
    response = model.predict_by_filename(filename=fullpath)

    concepts = response['outputs'][0]['data']['concepts']
    for concept in concepts:
        print(concept['name'], concept['value'])
        
@Gooey(language='english')
def main():
    parser  = ArgumentParser(description='Process an image or a video.')
    parser.add_argument("-u", "--url", default= "https://samples.clarifai.com/metro-north.jpg", help="")
    parser.add_argument("-i", "--image", default= 'I:\\freelancing\\portfolio\\1.jpg', help="")
    args = parser.parse_args()
    if vars(args).get('help'):
        exit(0)
    #process_url(args.url)
    process_image(args.image)
    
if __name__ == '__main__':
    #main()
    process_image('I:\\freelancing\\portfolio\\1.jpg')
    
