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

# Let the runtime-relationship define the models
# So in this case, TermSet is a key, that acts as the master reference
# for whats inside the AllTerms table.
def storeTerm(term_raw, referencing_frame, google_entity_id):
    termParent = TermSet.objects.filter(term_raw=term_raw)
    if termParent == None:
        termParent = TermSet.objects.create(term_raw=term_raw,google_entity_id=google_entity_id)
    noisyTerm = AllTerms.objects.create(term_raw=term_raw,term_set_parent=termParent,referencing_frame=referencing_frame)

def storeLongForm(transcript, referencing_frame):
    #this is the defined max count for long form as its current storage format
    if len(transcript) > 500:
        transcript = transcript[:500]
    longFormEntry = LongFormSet.objects.create(long_form_string=transcript, referencing_frame=referencing_frame)

# this will be the generic bucket store for the snowboy phrases if I manage to get that fucking
# shit working
def storePhrase(phrase_raw, referencing_frame, google_entity_id):
    phraseParent = PhraseSet.objects.filter(phrase_raw=phrase_raw)
    if phraseParent == None:
        phraseParent = PhraseSet.objects.create(phrase_raw=phrase_raw,google_entity_id=google_entity_id)
    noisyPhrase = AllPhrases.objects.create(phrase_raw=phrase_raw,phrase_set_parent=phraseParent,referencing_frame=referencing_frame)

def storeLabel(label_raw, referencing_frame, google_entity_id):
    labelParent = LabelSet.objects.filter(label_raw=label_raw)
    if labelParent == None:
        labelParent = LabelSet.objects.create(label_raw=label_raw,google_entity_id=google_entity_id)
    noisyLabel = AllLabels.objects.create(label_raw=label_raw,label_set_parent=labelParent,referencing_frame=referencing_frame)

"""
class WebSet(models.Model):
    web_raw = models.CharField(max_length=200)
    web_identity = models.CharField(max_length=200)
    web_url = models.CharField(max_length=200)
    google_entity_id = models.CharField(max_length=50)
    metadata = {}
class AllWeb(models.Model):
    web_raw = models.CharField(max_length=200)
    web_score = models.CharField(max_length=200)
    web_identity = models.CharField(max_length=200)
    web_url = models.CharField(max_length=200)
    web_set_parent = models.ForeignKey(PhraseSet, on_delete=models.CASCADE)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    metadata = {}
"""

def storeWeb(web_raw, web_score, web_identity, web_url, referencing_frame, google_entity_id):
    #complexity can be reduced because we assume function is called with default values, or not
    # maybe that will make future changes harder on the driver at the wheel
    if web_raw != None:
        webParent = WebSet.objects.filter(web_raw=web_raw)
        if webParent == None:
            webParent = WebSet.objects.create(web_raw=web_raw,web_identity=web_identity,web_url="",google_entity_id=google_entity_id)
        noisyWeb = AllWeb.objects.create(web_raw=web_raw,web_score=web_score,web_identity=web_identity,web_url="",web_set_parent=webParent,referencing_frame=referencing_frame)
    else:
        webParent = WebSet.objects.filter(web_url=web_url)
        if webParent == None:
            webParent = WebSet.objects.create(web_raw="",web_identity="",web_url=web_url,google_entity_id=google_entity_id)
        noisyWeb = AllWeb.objects.create(web_raw="",web_score="",web_identity="",web_url=web_url,web_set_parent=webParent,referencing_frame=referencing_frame)

def importFrameToDatabase(frameDictionary, filetype):
    if filetype == "audio":
        importAudioMetaToDatabase(frameDictionary)
    if filetype == "image":
        importImageMetaToDatabase(frameDictionary)

"""
class TermSet(models.Model):
    term_raw = models.CharField(max_length=100)
    google_entity_id = models.CharField(max_length=50)
    metadata = {}
class AllTerms(models.Model):
    term_raw = models.CharField(max_length=100)
    term_set_parent = models.ForeignKey(TermSet, on_delete=models.CASCADE)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    metadata = {}
"""
def importAudioMetaToDatabase(frameDictionary):
    filePath = frameDictionary["file"]
    parentFolder = frameDictionary["foldername"]
    filePathTranscript = parentFolder + filePath + "-transcript.json"
    referencing_frame = Frame.objects.get(id=frameDictionary['frameid'])
    with open(filePathTranscript, 'r') as cuckforce5:
        rawDat = cuckforce5.read()
        #[[{"confidence": "0.905990123749", "transcript": "standing on the running board ripping his Springfield"}]]
        transcriptJSON = json.loads(rawDat)
        if len(transcriptJSON) > 0:
            firstTranscription = transcriptJSON[0]
            if len(firstTranscription) > 0:
                firstResult = firstTranscription[0]
                confidence = firstResult["confidence"]
                transcript = firstResult["transcript"]
                storeLongForm(transcript, referencing_frame)
                nBroke = transcript.split(' ')
                for termSlug in nBroke:
                    # test is exist
                    storeTerm(termSlug, referencing_frame, "")

def importImageMetaToDatabase(frameDictionary):
    #importGoogleFacesToDatabase(frameDictionary) #this is useless, need to implement the amazon facial recognition libs
    importTextToDatabase(frameDictionary)
    importLabelToDatabase(frameDictionary)
    importLandmarksToDatabase(frameDictionary)
    importLogoToDatabase(frameDictionary)
    importDocumentToDatabase(frameDictionary)
    importWebToDatabase(frameDictionary)

def importGoogleFacesToDatabase(frameDictionary):
    filePath = frameDictionary["file"]
    filePathTranscript = filePath + "-detectfaces.json"
    referencing_frame = Frame.objects.get(id=frameDictionary['frameid'])
    with open(filePathTranscript, 'r') as cuckforce5:
        rawDat = cuckforce5.read()
        transcriptJSON = json.loads(rawDat)

"""
class TermSet(models.Model):
    term_raw = models.CharField(max_length=100)
    google_entity_id = models.CharField(max_length=50)
    metadata = {}
class AllTerms(models.Model):
    term_raw = models.CharField(max_length=100)
    term_set_parent = models.ForeignKey(TermSet, on_delete=models.CASCADE)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    metadata = {}
class PhraseSet(models.Model):
    phrase_raw = models.CharField(max_length=200)
    metadata = {}
class AllPhrases(models.Model):
    phrase_raw = models.CharField(max_length=200)
    phrase_set_parent = models.ForeignKey(PhraseSet, on_delete=models.CASCADE)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    metadata = {}
"""
def importTextToDatabase(frameDictionary):
    filePath = frameDictionary["file"]
    filePathResponse = filePath + "-text.json"
    referencing_frame = Frame.objects.get(id=frameDictionary['frameid'])
    with open(filePathResponse, 'r') as cuckforce5:
        rawDat = cuckforce5.read()
        textJSON = json.loads(rawDat)
        texts = textJSON["texts"]
        for textRaw in texts:
            splitText = textRaw.split('\n') # cause google nests results in same array it seems
            if splitText.length == 0:
                storeTerm(termSlug, referencing_frame, "")
            else:
                for textSlugRaw in splitText:
                    storePhrase(textSlugRaw, referencing_frame, "")

def importLabelToDatabase(frameDictionary):
    filePath = frameDictionary["file"]
    filePathResponse = filePath + "-labels.json"
    referencing_frame = Frame.objects.get(id=frameDictionary['frameid'])
    with open(filePathResponse, 'r') as cuckforce5:
        rawDat = cuckforce5.read()
        textJSON = json.loads(rawDat)

def importLandmarksToDatabase(frameDictionary):
    print "IMPORTLANDMARKS NOT IMPLEMENTED"

def importLogoToDatabase(frameDictionary):
    print "IMPORTLOGO NOT IMPLEMENTED"

def importDocumentToDatabase(frameDictionary):
    print "IMPORTDOCUMENT NOT IMPLEMENTED"

def importWebToDatabase(frameDictionary):
    print "IMPORT WEB NOT IMPLEMENTED"


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
