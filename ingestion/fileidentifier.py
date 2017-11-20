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
import magic

imageFileTypes = ["jpeg", "jpg", "png"]
soundFileTypes = ["mp3", "wav", "flac", "raw", "m4a", "aac", "iso"]
textFileTypes = ["json","txt", "ascii", "text"]

def determineSimpleType(filepathURI):
    # should find a safer solution to reading, buffer may be overflow
    with open(filepathURI, 'r') as openFile:
        openFile.seek(0)
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

def determineSimpleFormat(filepathURI):
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
                return slugFileType
        except:
            print "not an image"

        try:
            if soundFileTypes.index(slugFileType):
                print "ISSA SOUND BITCH HA HA"
                return slugFileType
        except:
            print "not an soundfile"

        openFile.close()
    return "generic"
