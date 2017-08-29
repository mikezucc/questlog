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

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# File Path used to reference the templates
CURRENTLOCATION = BASE_DIR + "/ingestion/templates/" # yeah whatever
#CURRENTLOCATION = os.getcwd().replace("\\","/")  + "/dojo/templates/"
INGESTIONPAGETEMPLATE = CURRENTLOCATION + 'ingestionmain.html'
LOGINTEMPLATE = CURRENTLOCATION + 'login.html'
UPLOAD_DIR_3 = os.getcwd().replace("\\","/") + "/ingestion/frames/"

def login(request):
    currentUser = request.session['username']
    if currentUser != None:
        return redirect('/mind/'+currentUser)

    return render(request, LOGINTEMPLATE, {})

def ingestionPage(request):
    return render(request, INGESTIONPAGETEMPLATE, {})

def mindPage(request, usernameInput):
    if usernameInput == None:
        return redirect('/login/')

    possibleUser = Minds.objects.get(username=usernameInput)
    if possibleUser == None:
        return redirect('/login')

def filesInFrame(frameName):
    fileList = []
    print "here 0"
    for filename in os.listdir(UPLOAD_DIR_3 + frameName + "/"):
        print "here 1 " + filename
        if filename!='.DS_Store':
            print "here 2 " + filename
            fileList.append(filename[:-5])
    return fileList
