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

# import the web page views
from . import *

# These might be for OS X (?)
UPLOAD_DIR_2 = os.getcwd().replace("\\","/")  + "/daily/uploads/"
UPLOAD_DIR_3 = os.getcwd().replace("\\","/") + "/daily/templates/"

# Create your views here.

# NO

def ingestAudio(request):
    return HttpResponse("We are out of the mild sauce senor.")

def ingestAudioList(request, username):
    return HttpResponse("List of user's bullshit here")

def ingestAudioReceiveUpload(request, username):
    try:
        files = request.FILES
    except:
        print "portal >> 0 || bitch failed"

    print 'ingestAudioReceiveUpload > 1 || ' + str(len(files)) + ', post '
    if files != None and len(files) > 0:
        print 'ingestAudioReceiveUpload > 1 || managing ' + str(len(files)) + ' of files'
        for f in files:
            print 'ingestAudioReceiveUpload > 2 || queueing ' + files[f].name
            o = files[f]
            print 'ingestAudioReceiveUpload > 2.1 || o as ' + str(len(o))
            print "handle_uploaded_file > 0 || "
            filenameDirty = o.name.replace(" ", "_") # per Model
            print "handle_uploaded_file > 1 || initiating system write" + filenameDirty
            with open(UPLOAD_DIR_3 + filenameDirty, 'wb+') as destination:
                print "handle_uploaded_file > 2 || opening file " + filenameDirty
                chunkCount = len(o)
                counter = 0
                print "handle_uploaded_file > 3 || writing " + str(chunkCount) + " chunks for " + filenameDirty
                for chunk in o.chunks():
                    destination.write(chunk)
                    print "handle_uploaded_file > 4 || at " + str(counter) + ' out of ' + str(chunkCount) + ' for ' + filenameDirty
                    counter = counter + len(chunk)
                print "handle_uploaded_file > 5 || finished writing " + filenameDirty

    return HttpResponse(status=200)
