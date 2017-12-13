# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django import forms
from models import *
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse
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
from django.views.decorators.csrf import csrf_exempt
import traceback
import sys
from pymongo import MongoClient
from fileidentifier import *
from jsondbimport import *

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# File Path used to reference the templates
CURRENTLOCATION = BASE_DIR + "/ingestion/templates/" # yeah whatever
#CURRENTLOCATION = os.getcwd().replace("\\","/")  + "/dojo/templates/"
INGESTIONPAGETEMPLATE = CURRENTLOCATION + 'ingestionmain.html'
LOGINTEMPLATE = CURRENTLOCATION + 'login.html'
MINDPAGETEMPLATE = CURRENTLOCATION + 'mind.html'
UPLOAD_DIR_3 = os.getcwd().replace("\\","/") + "/ingestion/frames/"

textFileTypes = ["json","txt", "ascii", "text"]

"""
mappedRes = {}
for res in mdb_spitData.audio_speech_google.find({"frame_id":frame_id}):
    res['_id'] = ""
    mappedRes["speech"] = res
for res in mdb_spitData.text_ocr_google.find({"frame_id":frame_id}):
    res['_id'] = ""
    mappedRes["ocr_text"] = res
for res in mdb_spitData.labels_ocr_google.find({"frame_id":frame_id}):
    res['_id'] = ""
    mappedRes["ocr_label"] = res
for res in mdb_spitData.web_ocr_google.find({"frame_id":frame_id}):
    res['_id'] = ""
    mappedRes["ocr_web"] = res
for res in mdb_spitData.document_ocr_google.find({"frame_id":frame_id}):
    res['_id'] = ""
    mappedRes["ocr_document"] = res
return mappedRes
"""

"""
NSDictionary *speech = parsedInfo[@"speech"];
if (speech) {
    NSArray *audio = speech[@"audio"];
    NSMutableArray <Speech_TranscriptionAPIUtteranceModel *>*transcriptionModels = (NSMutableArray <Speech_TranscriptionAPIUtteranceModel *>*)[NSMutableArray new];
    if (audio && [audio count]) {
        NSArray *transcriptionResults = [audio firstObject];
        if ([transcriptionResults count]) {
            for (NSDictionary *transcriptionModel in transcriptionResults) {
                Speech_TranscriptionAPIUtteranceModel *utterance = [Speech_TranscriptionAPIUtteranceModel new];
                NSString *confidence = transcriptionModel[@"confidence"];
                if (confidence) {
                    utterance.confidence = confidence;
                }
                NSString *transcript = transcriptionModel[@"transcript"];
                if (transcript) {
                    utterance.transcription = transcript;
                }
                [transcriptionModels addObject:utterance];
            }
        }
    }
    speechModel.transcriptionResults = [transcriptionModels copy];
}
"""

def readFromStopWordsFile(lan):
    if lan == "en":
        stopwords_file = open("en-stopwords.json", 'r')
        stopwords_list = stopwords_file.read().split(",")
        stopwords_file.close()
        return stopwords_list
    return []

stopwords_en_list = readFromStopWordsFile("en")

# frame object
# mapped in mongodb as frame_id
def extractTermsFromFrame(mongo_frame):
    if "speech" in mongo_frame:
        speech_res = mongo_frame["speech"]
        if "audio" in speech_res:
            audio_res = speech_res["audio"]
            if len(audio_res) > 0:
                transcription_results = audio_res[0]
                for transcription_model  in transcription_results:
                    if "transcript" in transcription_model:
                        transcript_text_tokens = transcription_model["transcript"].split(' ')
                        clean_text_tokens = [token for token in tokens if token not in stopwords_en_list]
                        return [clean_text_tokens]
    return []

def combAllFramesForTerms(usernameInput):
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return HttpResponse(code=401) # differing codes reveal to blackbox testing
    possibleFrames = Frame.objects.filter(owner=possibleMind).order_by('-createdat')
    if possibleFrames == None:
        print usernameInput + " HAS NO FRAMES"
        return JsonResponse(json.dumps([])) # ;mao Im a god
    print "user " + usernameInput + " has " + str(len(possibleFrames)) + " frames"
    frameMetadata = {}
    framesMetadataList = []
    for frame in possibleFrames:
        combSingleFrameForTerms(frame.id)
    return HttpResponse(status=200)

def combSingleFrameForTerms(frame_id):
    possibleFrames = Frame.objects.filter(id=frame_id)
    if possibleFrames == None:
        print "Could not find frame to comb"
        return
    # determing main file shit
    main_file = frame.main_file
    if main_file != "" and main_file != "NO_FILE": #fucking hell lol
        print "valid file"
    else:
        continue
    frame_id = frame.id
    frameResults = vomitJSONAPIResultstoAPI(frame_id)
    for mongo_frame in frameResults:
        frame_term_lists = extractTermsFromFrame(mongo_frame)
        for term_list in frame_term_lists:
            spitTermListToMongo(frame_id, term_list)
