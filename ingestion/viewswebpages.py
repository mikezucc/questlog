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
from django.http import FileResponse
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

# fucking just take the int dude
def downlinkFrameData(request, frameid, filename):
    if frameid == None:
        return HttpResponse(status=400)
    possibleFrames = Frame.objects.filter(id=frameid)
    if possibleFrames == None:
        return HttpResponse(status=401)
    # is there a way to make this recursive? so its higher than 2
    for frame in possibleFrames:
        foldername = frame.foldername
        files = filesInFrame(foldername)
        filesInFrameList = []
        for fil in files:
            if fil == filename:
                return FileResponse(open(foldername + fil, 'rb'))
    return HttpResponse(status=500)

def loginPage(request):
    request.session['username'] = ""
    return render(request, LOGINTEMPLATE, {'inputCode':200})

def loginRequest(request):
    inputUsername = request.POST['username']
    inputPassword = request.POST['password']
    if inputPassword == None:
        return render(request, LOGINTEMPLATE, {'inputCode':400})
    users = Mind.objects.filter(username=inputUsername)
    if len(users) == 0:
        newUser = Mind.objects.create(username=inputUsername, password=inputPassword, profile_picture="[]")
        newUser.save()
    elif users[0].password != inputPassword:
        return render(request, LOGINTEMPLATE, {'inputCode':401})
    request.session['username'] = inputUsername
    return redirect('/mind/'+inputUsername+'/')

def ingestionPage(request):
    return render(request, INGESTIONPAGETEMPLATE, {'statuscode':'ok'})

def mindPageCurrentUser(request):
    currentUser = ""
    try:
        currentUser = request.session['username']
    except:
        print "shit lmao"
    if currentUser != "":
        return redirect('/mind/'+currentUser+'/')
    return redirect('/login/')

def mindPage(request, usernameInput):
    if usernameInput == None:
        return redirect('/login/')
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return redirect('/login/')
    possibleFrames = Frame.objects.filter(owner=possibleMind)
    if possibleFrames == None:
        return render(request, MINDPAGETEMPLATE, {'statuscode': 'genesis'})
    # is there a way to make this recursive? so its higher than 2
    for frame in possibleFrames:
        foldername = frame.foldername
        files = filesInFrame(foldername)
        filesInFrameList = []
        for fil in files:
            filebuffer = magic.from_buffer(open(foldername + fil, 'r').read(1024))
            thang = {'metadata':{'type':filebuffer,'simpletype':determineSimpleType(foldername + fil)},'filename':fil}
            filesInFrameList.append(thang)
        frame.metadata = {'content':filesInFrameList} # dictionary property
    return render(request, MINDPAGETEMPLATE, {'domain': 'http://192.168.1.163:3001', 'statuscode': 'transit', 'username':usernameInput, 'frames': possibleFrames})

imageFileTypes = ["jpeg", "jpg", "png"]
soundFileTypes = ["mp3", "wav", "flac", "raw", "m4a", "aac", "iso"]

def determineSimpleType(filepathURI):
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
                print "ISSA IMAGE BITCH HA HA"
                return "image"
        except:
            print "not an image"

        try:
            if soundFileTypes.index(slugFileType):
                print "ISSA SOUND BITCH HA HA"
                return "sound"
        except:
            print "not an soundfile"

        openFile.close()
    return "generic"

def filesInFrame(frameName):
    fileList = []
    print "here 0"
    for filename in os.listdir(frameName):
        print "here 1 " + filename
        if filename!='.DS_Store':
            print "here 2 " + filename
            fileList.append(filename)
    return fileList
