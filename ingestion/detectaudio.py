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

kAUDIO_TIME_SLICE_WINDOW = 15

def runGoogleSpeechSuite(frameDictionary, frame_id, user_id):
    transcribe_file(frameDictionary, frame_id, user_id)

#
# contains the path to the converted file
# return (convertFilePath, needsSlice, sliceCount)
#
def convertToL16(path):
    openedFile = AudioSegment.from_file(path)

    needsSlice = False
    fifteenSeconds = kAUDIO_TIME_SLICE_WINDOW * 1000
    soundFiles = []
    cursor = 0 * 1000
    if openedFile.duration_seconds >= fifteenSeconds:
        needsSlice = True
        while cursor < openedFile.duration_seconds:
            interval = None
            if cursor+fifteenSeconds < openedFile.duration_seconds:
                interval = openedFile[cursor:cursor+fifteenSeconds]
            else:
                interval = openedFile[cursor:]
            if interval != None:
                convertFilePath = path + str(cursor) + "-L16convert.raw"
                #"-b:a", "16000""-b:a", "16000"
                openedFile.export(convertFilePath, format="s16le", parameters=["-b:a", "16000"])
                soundFiles.append(convertFilePath)
            cursor = cursor + fifteenSeconds
    else:
        #"-b:a", "16000""-b:a", "16000"
        openedFile.export(convertFilePath, format="s16le", parameters=["-b:a", "16000"])
        convertFilePath = path+"-L16convert.raw"
        soundFiles = [convertFilePath]
    return (soundFiles, needsSlice, sliceCount)

# [START def_transcribe_file]
def transcribe_file(filepathURI, frame_id, user_id):
    speech_file = filepathURI
    client = speech.SpeechClient()

    # [START migration_async_request]
    resultsJSONList = []
    (soundFiles, needsSlice, sliceCount) = convertToL16(speech_file)
    mark_time_offset_counter = 0
    for convertedFilePath in soundFiles:
        with io.open(convertedFilePath, 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
            enable_word_time_offsets=True)

        # [START migration_async_response]
        operation = client.long_running_recognize(config, audio)
        # [END migration_async_request]

        print('Waiting for operation to complete...')
        result = operation.result(timeout=1000)

        for res in result.results:
            for alternative in res.alternatives:
                word_marks = []
                for word_info in alternative.words:
                    word_mark = {"word":word_info.word, "start":mark_time_offset_counter+word_info.start_time.seconds}
                    word_marks.append(word_mark)
                    storeToTermMapSQL(word_info.word, word_info.start_time, frame_id, user_id)
                scopeJSON = {"transcript":'{}'.format(alternative.transcript), "confidence":'{}'.format(alternative.confidence), "words":word_marks}
                phrasonJSON.append(scopeJSON)
                print('Transcript: {}'.format(alternative.transcript))
                print('Confidence: {}'.format(alternative.confidence))
            resultsJSONList.append(phrasonJSON)
        mark_time_offset_counter = mark_time_offset_counter + kAUDIO_TIME_SLICE_WINDOW

    audioJSON = {"audio":resultsJSONList}
    spitJSONAPIResulttoMDB(audioJSON, "audio_speech_google", frame_id, user_id)

    # [END migration_async_response]
# [END def_transcribe_file]

def storeToTermMapSQL(word, start_time, frame_id, user_id):
    termSetEntry = TermSet.objects.get(term_raw=word,user_parent=user_id)
    if termSetEntry == None:
        termSetEntry = TermSet.objects.create(term_raw=word,user_parent=user_id,google_entity_id="",rough_count=0,createdat=datetime.datetime.now())
    else:
        termSetEntry.rough_count = termSetEntry.rough_count + 1
        termSetEntry.save()
    AllTerms.objects.create(term_raw=word,user_parent=user_id,term_set_parent=termSetEntry,referencing_frame=frame_id,createdat=datetime.datetime.now(),start_time=start_time)

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
