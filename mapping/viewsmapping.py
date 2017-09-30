# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django import forms
from models import *
from django.utils import timezone
from django.http import HttpResponse
from django.template import RequestContext
#from constants import *
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
import zipfile
import StringIO
from django.forms import widgets
import shutil
import urllib2
import urllib
import json
import math
import boto
import string
import random
from django.template.loader import render_to_string
import re
import os.path
import mimetypes
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import magic

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# File Path used to reference the templates
CURRENTLOCATION = BASE_DIR + "/ingestion/templates/" # yeah whatever
#CURRENTLOCATION = os.getcwd().replace("\\","/")  + "/dojo/templates/"
INGESTIONPAGETEMPLATE = CURRENTLOCATION + 'ingestionmain.html'
LOGINTEMPLATE = CURRENTLOCATION + 'login.html'
MINDPAGETEMPLATE = CURRENTLOCATION + 'mind.html'
UPLOAD_DIR_3 = os.getcwd().replace("\\","/") + "/ingestion/frames/"

# these views
from . import *
from viewswebpages import *
from google.cloud import *
from pydub import AudioSegment

def linearDiffOrganize(usernameInput):
    if usernameInput == None:
        return 400
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return 404
    possibleFrames = Frame.objects.filter(owner=possibleMind).order_by('createdat')
    if possibleFrames == None:
        return 402
    frameDiffsLinear = linearTimeDiff(possibleFrames)

def linearTimeDiff(possibleFrames):
    lastFrameTime = None
    frameDiffsLinear = []
    for frame in possibleFrames:
        createdat = frame.createdat
        if lastFrameTime == None:
            frameDiffsLinear.append({"frame":frame.id,"diff":0})
        else:
            frameDiffsLinear.append({"frame":frame.id,"diff":(createdat-lastFrameTime).total_seconds()})
        lastFrameTime = createdat
    return frameDiffsLinear


def filesInFrame(frameName):
    fileList = []
    print "here 0"
    for filename in os.listdir(frameName):
        print "here 1 " + filename
        if filename!='.DS_Store':
            print "here 2 " + filename
            fileList.append(filename)
    return fileList
