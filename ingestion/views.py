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
from django.views.decorators.csrf import csrf_exempt
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

from multiprocessing import Pool
pool = Pool(processes=1)

# import the web page views
from . import *
from quanty import *

# These might be for OS X (?) <- ?
# UPLOAD_DIR_2 = os.getcwd().replace("\\","/")  + "/daily/uploads/"
# this shit is duped viewswebpages.py ok dont fuck this up
UPLOAD_DIR_3 = os.getcwd().replace("\\","/") + "/ingestion/frames/"

# Create your views here.

def processedSingleFrame():
    print "Finsished processing Single Frame"

# NO
@csrf_exempt
def ingestFiles(request, usernameInput):
    try:
        files = request.FILES
    except:
        print "portal >> 0 || bitch failed"
        return HttpResponse(status=400)

    users = Mind.objects.filter(username=usernameInput)
    if len(users) == 0:
        #maybe upload to a random fucking folder i dont know??
        print "well this is a hodge podge you see"
        return HttpResponse(status=403)
    mind = users[0]

    checkDirectoryForMind(mind)
    timestampstring = unicode(datetime.datetime.now())
    frameFolderName = UPLOAD_DIR_3 + mind.username + "/" + timestampstring + "/"
    status = createFrameWithFolder(frameFolderName)

    print 'uploadDataRequest > 1 || ' + str(len(files)) + ', post '
    if files != None and len(files) > 0:
        print 'uploadDataRequest > 1 || managing ' + str(len(files)) + ' of files'
        filnem = ""
        for f in files:
            print 'uploadDataRequest > 2 || queueing ' + files[f].name
            o = files[f]
            print 'uploadDataRequest > 2.1 || o as ' + str(len(o))
            print "handle_uploaded_file > 0 || "
            filenameDirty = o.name.replace(" ", "_") # per Model
            filnem = filenameDirty
            print "handle_uploaded_file > 1 || initiating system write" + filenameDirty
            with open(frameFolderName + filenameDirty, 'wb+') as destination:
                print "handle_uploaded_file > 2 || opening file " + filenameDirty
                chunkCount = len(o)
                counter = 0
                print "handle_uploaded_file > 3 || writing " + str(chunkCount) + " chunks for " + filenameDirty
                for chunk in o.chunks():
                    destination.write(chunk)
                    print "handle_uploaded_file > 4 || at " + str(counter) + ' out of ' + str(chunkCount) + ' for ' + filenameDirty
                    counter = counter + len(chunk)
                print "handle_uploaded_file > 5 || finished writing " + filenameDirty
        frameO = Frame.objects.create(owner=mind, foldername=frameFolderName, createdat=datetime.datetime.now(), createdat_string=timestampstring, main_file=filnem)
        result = pool.apply_async(processFrame, [frameO.id]) # Evaluate "f(10)" asynchronously calling callback when finished
        return HttpResponse(status=200)
    print("failed to do shit")
    return tryWithOneFileRead(request, usernameInput)

def tryWithOneFileRead(request, usernameInput):
    try:
        files = request.FILE
    except:
        print "portal >> 0 || bitch failed"
        return HttpResponse(status=400)

    users = Mind.objects.filter(username=usernameInput)
    if len(users) == 0:
        #maybe upload to a random fucking folder i dont know??
        print "well this is a hodge podge you see"
        return HttpResponse(status=403)
    mind = users[0]

    checkDirectoryForMind(mind)
    timestampstring = unicode(datetime.datetime.now())
    frameFolderName = UPLOAD_DIR_3 + mind.username + "/" + timestampstring + "/"
    status = createFrameWithFolder(frameFolderName)

    print 'tryWithOneFileRead > 1 || ' + files + ', post '
    if files != None:
        print 'tryWithOneFileRead > 2 || queueing ' + files.name
        o = files
        print 'tryWithOneFileRead > 2.1 || o as ' + str(len(o))
        print "tryWithOneFileReadhandle_uploaded_file > 0 || "
        filenameDirty = o.name.replace(" ", "_") # per Model
        print "tryWithOneFileReadhandle_uploaded_file > 1 || initiating system write" + filenameDirty
        with open(frameFolderName + filenameDirty, 'wb+') as destination:
            print "tryWithOneFileReadhandle_uploaded_file > 2 || opening file " + filenameDirty
            chunkCount = len(o)
            counter = 0
            print "tryWithOneFileReadhandle_uploaded_file > 3 || writing " + str(chunkCount) + " chunks for " + filenameDirty
            for chunk in o.chunks():
                destination.write(chunk)
                print "tryWithOneFileReadhandle_uploaded_file > 4 || at " + str(counter) + ' out of ' + str(chunkCount) + ' for ' + filenameDirty
                counter = counter + len(chunk)
            print "tryWithOneFileReadhandle_uploaded_file > 5 || finished writing " + filenameDirty
        frameO = Frame.objects.create(owner=mind, foldername=frameFolderName, createdat=datetime.datetime.now())
        return HttpResponse(status=200)
    print("failed to do shit")
    return HttpResponse(status=500)

def createFrameWithFolder(frameFolderName):
    print "createFrameForMind >> checking for " + frameFolderName
    if os.path.isdir(frameFolderName):
        print frameFolderName + " exists already"
        return False
    else:
        try:
            os.makedirs(frameFolderName)
            print "createFrameForMind >> successfully made user folder"
        except OSError as e:
            print "createFrameForMind >> exception trying to create user folder"
            if e.errno != errno.EEXIST:
                print "createFrameForMind >> unknown exception"
            return False
    print "createFrameForMind >> EOF"
    return True

def checkDirectoryForMind(mind):
    mindFolderName = UPLOAD_DIR_3 + mind.username + "/"
    print "checkDirectoryForMind >> checking for " + mindFolderName
    if os.path.isdir(mindFolderName):
        print mindFolderName + " exists already"
        return
    else:
        print "creating mind folder for " + mind.username
        try:
            os.makedirs(mindFolderName)
            print "checkDirectoryForMind >> successfully made user folder"
        except OSError as e:
            print "checkDirectoryForMind >> exception trying to create user folder"
            if e.errno != errno.EEXIST:
                print "checkDirectoryForMind >> unknown exception"
    print "checkDirectoryForMind >> EOF"
