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
import datetime
import json
import traceback

# these views
from . import *
from viewswebpages import *
from detectvision import *
from detectaudio import *

imageFileTypes = ["jpeg", "jpg", "png"]
soundFileTypes = ["mp3", "wav", "flac", "raw", "m4a", "aac", "iso"]

def processMind(request, usernameInput):
    print 'for fucks sake'
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return redirect('/login/')
    possibleFrames = Frame.objects.filter(owner=possibleMind)
    if possibleFrames == None:
        return render(request, MINDPAGETEMPLATE, {'statuscode': 'genesis'})
    # is there a way to make this recursive? so its higher than 2
    for frame in possibleFrames:
        print "frame " + str(frame.id)
        foldername = frame.foldername
        files = filesInFrame(foldername)
        filesInFrameList = []
        print files
        if len(files) > 1:
            print "\t**\n\tFrame Already processing\n\t**"
            continue
        for fil in files:
            # try:
            #     if fil.index("-processStatus.txt"):
            #         continue
            #     print fil + "-processStatus.txt"
            #     files.index(fil + "-processStatus.txt")
            #     continue
            # except:
            #     # maybe this can be done by the file level
            #     print "never processed this directory"
            startFileProcessingPipeline({"frameid":frame.id,"filepathURI":(foldername+fil)})
    return HttpResponse(status=200)

# dictionary input {"frameid":<frame.id>, "file":<full path URI filename>}
# full path URI for network hosted files later on
def startFileProcessingPipeline(frameDictionary):
    frameid = frameDictionary['frameid']
    filepathURI = frameDictionary['filepathURI']
    # should find a safer solution to reading, buffer may be overflow
    with open(filepathURI, 'r') as openFile:
        fileTypeMagic = magic.from_buffer(openFile.read(1024))

        splitFileType = fileTypeMagic.split(',')
        print splitFileType
        slugFileType = splitFileType[0].split(' ')[0].lower()
        print slugFileType

        try:
            print "checking " + slugFileType + " against "
            print imageFileTypes
            if imageFileTypes.index(slugFileType) != None:
                print "--------------------------------------------------------------------------"
                print "*** queue VISION process for  " + filepathURI
                try:
                    processImageFile(frameDictionary)
                except Exception as e:
                    print traceback.format_exc()
                print "--------------------------------------------------------------------------"
        except:
            print "not an image"

        try:
            if soundFileTypes.index(slugFileType):
                print "--------------------------------------------------------------------------"
                print "*** queue AUDIO process for " + filepathURI
                try:
                    processSoundFile(frameDictionary)
                except Exception as e:
                    print traceback.format_exc()
                print "--------------------------------------------------------------------------"
        except:
            print "not an soundfile"

        openFile.close()

        # with open(filepathURI+'-processStatus.txt', 'w+') as statusFile:
        #     statusFile.write("finished")
        #     statusFile.close()

def processImageFile(frameDictionary):
    print "processing image" + json.dumps(frameDictionary)
    frameid = frameDictionary['frameid']
    filepathURI = frameDictionary['filepathURI']
    # try faces, returns a list result of Face objects? not sure
    # if object or serialized thanks google for that shit
    runGoogleVisionSuite(filepathURI)

def processSoundFile(frameDictionary):
    frameid = frameDictionary['frameid']
    filepathURI = frameDictionary['filepathURI']
    # try faces, returns a list result of Face objects? not sure
    # if object or serialized thanks google for that shit
    runGoogleSpeechSuite(filepathURI)
