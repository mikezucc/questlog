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
from viewsmapping import *

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
            frameDictionary = {"frame_id":frame.id,"filepathURI":(foldername+fil),"file":fil,"foldername":foldername, "user_id":possibleMind.id}
            startFileProcessingPipeline(frameDictionary)
    return HttpResponse(status=200)

def processFrame(frameId):
    possibleFrames = Frame.objects.filter(id=frameId)
    if possibleFrames == None:
        return
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
            frameDictionary = {"frame_id":frame.id, "user_id":frame.owner.id,"filepathURI":(foldername+fil),"file":fil,"foldername":foldername}
            startFileProcessingPipeline(frameDictionary)
    return HttpResponse(status=200)

def saveFileMetaInfo(fileTypeMagic):
    splitFileType = fileTypeMagic.split(',')
    fileMetadataJSON = {}
    firstRead = False
    for slugMetaSegment in splitFileType:
        if not firstRead:
            fileMetadataJSON['type'] = slugMetaSegment
            continue
        if "EXIF" in slugMetaSegment:
            fileMetadataJSON['EXIF'] = extractEXIF(slugMetaSegment)
        segmentSegments = slugMetaSegment.split(' ').lower()


# dictionary input {"frameid":<frame.id>, "file":<full path URI filename>}
# full path URI for network hosted files later on
def startFileProcessingPipeline(frameDictionary):
    frame_id = frameDictionary['frame_id']
    user_id = frameDictionary['user_id']
    filepathURI = frameDictionary['filepathURI']
    # should find a safer solution to reading, buffer may be overflow
    with open(filepathURI, 'r') as openFile:
        fileTypeMagic = magic.from_buffer(openFile.read(1024))

        splitFileType = fileTypeMagic.split(',')
        print splitFileType
        slugFileType = splitFileType[0].split(' ')[0].lower().strip()
        try:
            slugSecondaryType = splitFileType[1].split(' ')[1].lower().strip()
        except:
            slugSecondaryType = ""
        print slugFileType
        print slugSecondaryType

        saveFileMetaInfo(fileTypeMagic)

        try:
            print "checking " + slugFileType +  ", " + slugSecondaryType +" against "
            print imageFileTypes
            if slugFileType in imageFileTypes or slugSecondaryType in imageFileTypes:
                print "--------------------------------------------------------------------------"
                print "*** queue VISION process for  " + filepathURI
                try:
                    processImageFile(frameDictionary, frame_id, user_id)
                    #importFrameToDatabase(frameDictionary, "image")
                except Exception as e:
                    print traceback.format_exc()
                print "--------------------------------------------------------------------------"
        except:
            print "not an image"

        try:
            if slugFileType in soundFileTypes or slugSecondaryType in soundFileTypes:
                print "--------------------------------------------------------------------------"
                print "*** queue AUDIO process for " + filepathURI
                try:
                    processSoundFile(frameDictionary, frame_id, user_id)
                    # combSingleFrameForTerms(frame_id)
                    # importFrameToDatabase(frameDictionary, "audio")
                except Exception as e:
                    print traceback.format_exc()
                print "--------------------------------------------------------------------------"
        except:
            print "not an soundfile"

        openFile.close()

        # with open(filepathURI+'-processStatus.txt', 'w+') as statusFile:
        #     statusFile.write("finished")
        #     statusFile.close()

def processImageFile(frameDictionary, frame_id, user_id):
    print "processing image" + json.dumps(frameDictionary)
    frame_id = frameDictionary['frame_id']
    filepathURI = frameDictionary['filepathURI']
    # try faces, returns a list result of Face objects? not sure
    # if object or serialized thanks google for that shit
    runGoogleVisionSuite(filepathURI, frame_id, user_id)

def processSoundFile(frameDictionary, frame_id, user_id):
    frame_id = frameDictionary['frame_id']
    filepathURI = frameDictionary['filepathURI']
    # try faces, returns a list result of Face objects? not sure
    # if object or serialized thanks google for that shit
    runGoogleSpeechSuite(filepathURI, frame_id, user_id)
