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
    for frame in possibleFrames:

    return render(request, MINDPAGETEMPLATE, {'statuscode': 'transit', 'username':usernameInput, 'frames': possibleFrames})

def filesInFrame(frameName):
    fileList = []
    print "here 0"
    for filename in os.listdir(UPLOAD_DIR_3 + frameName + "/"):
        print "here 1 " + filename
        if filename!='.DS_Store':
            print "here 2 " + filename
            fileList.append(filename)
    return fileList
