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
import io

# these views
from . import *
from viewswebpages import *
from google.cloud import *
from pydub import AudioSegment

# Transcribe the given audio file asynchronously.
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from jsondbimport import *

INGESTION_DIR = os.getcwd().replace("\\","/") + "/ingestion/"

def readStopWordList():
    with open(INGESTION_DIR+'en_stopwords.txt', 'r') as stopwords_file:
        return stopwords_file.read().splitlines()

kSTOPWORDS_LIST = readStopWordList()

#       if ms is not None:
#           return ms * (self.frame_rate / 1000.0)

    # @property
    # def duration_seconds(self):
    #     return self.frame_rate and self.frame_count() / self.frame_rate or 0.0

kAUDIO_TIME_SLICE_WINDOW = 30

def runGoogleSpeechSuite(frameDictionary, frame_id, user_id):
    transcribe_file(frameDictionary, frame_id, user_id)

#
# contains the path to the converted file
# return (convertFilePath, needsSlice, sliceCount)
#
def convertToL16(path, frameid):
    curdirlist = path.split("/")
    curdirlist.pop()
    curdir = "/".join(curdirlist) + "/"
    openedFile = AudioSegment.from_file(path)
    sample_rate = openedFile.frame_rate
    print "::::: ** ORIGINAL ** :::: SAMPLE RATE: " + str(sample_rate) + " sp/s"
    needsSlice = False
    fifteenSeconds = kAUDIO_TIME_SLICE_WINDOW # SIKE HAHA
    soundFiles = []
    cursor = 0
    print "::::::::" + str(fifteenSeconds) + " AUDIO FILE DURATION: " + str(openedFile.duration_seconds)
    if openedFile.duration_seconds >= kAUDIO_TIME_SLICE_WINDOW:
        needsSlice = True
        while cursor < openedFile.duration_seconds:
            print ":::::::: PROCESSING SLICE: " + str(cursor) + "/" + str(openedFile.duration_seconds)
            interval = None
            if cursor+fifteenSeconds < openedFile.duration_seconds:
                interval = openedFile[(cursor*1000):(cursor+fifteenSeconds)*1000]
            else:
                interval = openedFile[(cursor*1000):]
            if interval != None:
                convertFilePath = path + str(cursor) + "-L16convert.raw"
                convertFilePathMP3 = curdir + "session" + str(frameid) + "-part" + str(cursor) + ".m4a"
                #"-b:a", "16000""-b:a", "16000"
                interval.export(convertFilePath, format="s16le")
                interval.export(convertFilePathMP3, format="mp3")
                soundFiles.append(convertFilePath)
            cursor = cursor + fifteenSeconds
    else:
        #"-b:a", "16000""-b:a", "16000"
        convertFilePath = path+"-L16convert.raw"
        openedFile.export(convertFilePath, format="s16le")
        soundFiles = [convertFilePath]
    return (soundFiles, needsSlice, sample_rate)

# [START def_transcribe_file]
def transcribe_file(filepathURI, frame_id, user_id):
    speech_file = filepathURI
    client = speech.SpeechClient()

    # [START migration_async_request]
    resultsJSONList = []
    (soundFiles, needsSlice, sample_rate) = convertToL16(speech_file, frame_id)
    mark_time_offset_counter = 0
    for convertedFilePath in soundFiles:
        try:
            with io.open(convertedFilePath, 'rb') as audio_file:
                content = audio_file.read()

            print ":::::::::::::: AUDIO SLICE: " + str(len(content)) + " @ " + str(sample_rate) + " sp/s"
            audio = types.RecognitionAudio(content=content)
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate,
                language_code='en-US',
                enable_word_time_offsets=True,
                speech_contexts=[types.SpeechContext(phrases=["token", "hype", "coin", "hype coin", "wallet", "crypto"])])

            # [START migration_async_response]
            operation = client.long_running_recognize(config, audio)
            # [END migration_async_request]

            print('Waiting for operation to complete...')
            result = operation.result(timeout=1000)

            for res in result.results:
                phrasonJSON = []
                for alternative in res.alternatives:
                    word_marks = []
                    for word_info in alternative.words:
                        if word_info.word.lower() in kSTOPWORDS_LIST:
                            continue
                        start_time_DB_format = "{}".format(mark_time_offset_counter+word_info.start_time.seconds)
                        word_mark = {"word":word_info.word, "start":start_time_DB_format, "frameid":frame_id, "userid":user_id}
                        word_marks.append(word_mark)
                        storeToTermMapSQL(word_info.word, start_time_DB_format, frame_id, user_id)
                    scopeJSON = {"transcript":'{}'.format(alternative.transcript), "confidence":'{}'.format(alternative.confidence), "words":word_marks}
                    phrasonJSON.append(scopeJSON)
                    print('Transcript: {}'.format(alternative.transcript))
                    print('Confidence: {}'.format(alternative.confidence))
                resultsJSONList.append(phrasonJSON)
            mark_time_offset_counter = mark_time_offset_counter + kAUDIO_TIME_SLICE_WINDOW
        except:
            print "GOOGLE TOOK A SHIT"

    audioJSON = {"audio":resultsJSONList}
    spitJSONAPIResulttoMDB(audioJSON, "audio_speech_google", frame_id, user_id)

    # [END migration_async_response]
# [END def_transcribe_file]

def storeToTermMapSQL(word, start_time, frame_id, user_id):
    users = Mind.objects.filter(id=user_id)
    if len(users) == 0:
        return
    mind = users[0]
    frames = Frame.objects.filter(id=frame_id)
    if len(frames) == 0:
        return
    frame = frames[0]
    termSetEntries = TermSet.objects.filter(term_raw=word,user_parent=mind)
    if len(termSetEntries) == 0:
        termSetEntry = TermSet.objects.create(term_raw=word,user_parent=mind,google_entity_id="",rough_count=0,createdat=datetime.datetime.now())
    else:
        termSetEntry = termSetEntries[0]
        termSetEntry.rough_count = termSetEntry.rough_count + 1
        termSetEntry.save()
    AllTerms.objects.create(term_raw=word,user_parent=mind,term_set_parent=termSetEntry,referencing_frame=frame,createdat=datetime.datetime.now(),start_time=start_time)

# [START def_transcribe_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=90)

    alternatives = result.results[0].alternatives
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))
# [END def_transcribe_gcs]


def convertToM4a(path):
    openedFile = AudioSegment.from_file(path)

    needsSlice = False
    fifteenSeconds = kAUDIO_TIME_SLICE_WINDOW # SIKE HAHA
    soundFiles = []
    cursor = 0
    print "::::::::" + str(fifteenSeconds) + " AUDIO FILE DURATION: " + str(openedFile.duration_seconds)
    if openedFile.duration_seconds >= kAUDIO_TIME_SLICE_WINDOW:
        needsSlice = True
        while cursor < openedFile.duration_seconds:
            print ":::::::: PROCESSING SLICE: " + str(cursor) + "/" + str(openedFile.duration_seconds)
            interval = None
            if cursor+fifteenSeconds < openedFile.duration_seconds:
                interval = openedFile[(cursor*1000):(cursor+fifteenSeconds)*1000]
            else:
                interval = openedFile[(cursor*1000):]
            if interval != None:
                convertFilePath = path + str(cursor) + "-m4adownsample.m4a"
                #"-b:a", "16000""-b:a", "16000"
                interval.export(convertFilePath, format="m4a", parameters=["-b:a", "44100"])
                soundFiles.append(convertFilePath)
            cursor = cursor + fifteenSeconds
    else:
        #"-b:a", "16000""-b:a", "16000"
        convertFilePath = path+"-m4adownsample.m4q"
        openedFile.export(convertFilePath, format="m4a", parameters=["-b:a", "44100"])
        soundFiles = [convertFilePath]
    return (soundFiles, needsSlice)
