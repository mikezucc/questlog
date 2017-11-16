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

def runGoogleSpeechSuite(frameDictionary, frame_id, user_id):
    transcribe_file(frameDictionary, frame_id, user_id)

#
# contains the path to the converted file
#
def convertToL16(path):
    openedFile = AudioSegment.from_file(path)
    convertFilePath = path+"-L16convert.raw"
    #"-b:a", "16000""-b:a", "16000"
    openedFile.export(convertFilePath, format="s16le", parameters=["-b:a", "48000"])
    return convertFilePath

# [START def_transcribe_file]
def transcribe_file(filepathURI, frame_id, user_id):
    speech_file = filepathURI
    client = speech.SpeechClient()

    # [START migration_async_request]
    convertedFilePath = convertToL16(speech_file)
    with io.open(convertedFilePath, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code='en-US')

    # [START migration_async_response]
    operation = client.long_running_recognize(config, audio)
    # [END migration_async_request]

    print('Waiting for operation to complete...')
    result = operation.result(timeout=90)

    resultsJSONList = []
    for res in result.results:
        phrasonJSON = []
        for alternative in res.alternatives:
            scopeJSON = {"transcript":'{}'.format(alternative.transcript), "confidence":'{}'.format(alternative.confidence)}
            phrasonJSON.append(scopeJSON)
            print('Transcript: {}'.format(alternative.transcript))
            print('Confidence: {}'.format(alternative.confidence))
        resultsJSONList.append(phrasonJSON)

    spitJSONAPIResulttoMDB({"audio":resultsJSONList}, "audio_speech_google", frame_id, user_id)

    jsonRes = json.dumps(resultsJSONList)
    with open(filepathURI+"-transcript.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return
    return
    # [END migration_async_response]
# [END def_transcribe_file]


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
