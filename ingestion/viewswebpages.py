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

# fucking just take the int dude
@csrf_exempt
def downlinkFrameData(request, frameid, filename):
    if frameid == None:
        return HttpResponse(status=400)
    possibleFrames = Frame.objects.filter(id=frameid)
    if possibleFrames == None:
        return HttpResponse(status=401)
    # is there a way to make this recursive? so its higher than 2
    for frame in possibleFrames:
        foldername = frame.foldername
        files = filesInFrame(foldername)
        filesInFrameList = []
        for fil in files:
            if fil == filename:
                approx_file_type = determineSimpleType(foldername+fil)
                content_type = ""
                if approx_file_type == "image":
                    content_type="image/" + determineSimpleFormat(foldername+fil) + ";"
                elif approx_file_type == "sound":
                    content_type="audio/" + determineSimpleFormat(foldername+fil) + ";"
                return FileResponse(open(foldername + fil, 'rb'),content_type=content_type)
    return HttpResponse(status=500)

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
    possibleFrames = Frame.objects.filter(owner=possibleMind).order_by("-createdat")
    if possibleFrames == None:
        return render(request, MINDPAGETEMPLATE, {'statuscode': 'genesis'})
    # is there a way to make this recursive? so its higher than 2
    for frame in possibleFrames:
        foldername = frame.foldername
        files = filesInFrame(foldername)
        filesInFrameList = []
        for fil in files:
            filebuffer = magic.from_buffer(open(foldername + fil, 'r').read(1024))
            thang = {'metadata':{'type':filebuffer,'simpletype':determineSimpleType(foldername + fil)},'filename':fil}
            filesInFrameList.append(thang)
        frame.metadata = {'content':filesInFrameList} # dictionary property
    return render(request, MINDPAGETEMPLATE, {'domain': 'http://192.168.1.163:3001', 'statuscode': 'transit', 'username':usernameInput, 'frames': possibleFrames})

# this will be a way to force client alignment. They can access via SLUGS or POST
@csrf_exempt
def mindPageAPIPOST(request):
    try:
        usernameInput = request.POST['username']
    except:
        print "missing username"
        return HttpResponse(code=403)
    return mindPageAPI(request, usernameInput)

@csrf_exempt
def mindPageAPI(request, usernameInput):
    if usernameInput == None:
        return HttpResponse(code=403)
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return HttpResponse(code=401) # differing codes reveal to blackbox testing
    possibleFrames = Frame.objects.filter(owner=possibleMind).order_by("-createdat")
    if possibleFrames == None:
        return JsonResponse(json.dumps([])) # ;mao Im a god
    # is there a way to make this recursive? so its higher than 2
    framesMetadataList = []
    for frame in possibleFrames:
        foldername = frame.foldername
        files = filesInFrame(foldername)
        filesInFrameList = []
        for fil in files:
            with open(foldername + fil, 'r') as resFile:
                filebuffer = magic.from_buffer(resFile.read(1024))
                thang = {'metadata':{'type':filebuffer,'simpletype':determineSimpleType(foldername + fil)},'filename':fil,'downlink_endpoint':"/downlink/"+str(frame.id)+"/"+fil+"/"}
                print filebuffer
                slugFileType = filebuffer.split(' ')[0].lower()
                print "JSON READ " + slugFileType
                fileOutput = ""
                try:
                    # FOR THE RECORD FUCK YOU IF YOU EVER USE ASSERTION FOR PRODUCTION OR EVER AT ALL HONESTLY
                    if textFileTypes.index(slugFileType) != None:
                        print "** JSON READ DETERMINED FILE TYPE"
                        resFile.seek(0)
                        fileOutput = resFile.read()
                        print "JSON READ ASCII FILE LENGTH" + fileOutput
                        thang['text'] = json.loads(fileOutput)
                except:
                    # print traceback.print_exc() # this will not be reliable among more than 3 people honestly
                    print "**** " + fileOutput + " ****"
                    print "JSON READ well couldnt fucking do that now could I and now I threw an error for that shit bullshit"
                resFile.close()
                filesInFrameList.append(thang)
        framesMetadataList.append({"frameid":frame.id,"files":filesInFrameList,"foldername":foldername}) # dictionary property
    return JsonResponse({"response":framesMetadataList,"secret_message":"suck a dick brody"})


@csrf_exempt
def mindPageAPIV2(request, usernameInput):
    if usernameInput == None:
        return HttpResponse(code=403)
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return HttpResponse(code=401) # differing codes reveal to blackbox testing
    possibleFrames = Frame.objects.filter(owner=possibleMind).order_by('-createdat')
    if possibleFrames == None:
        print usernameInput + " HAS NO FRAMES"
        return JsonResponse(json.dumps([])) # ;mao Im a god
    frameMetadata = {}
    framesMetadataList = []
    mdb_client = MongoClient('localhost', '27107')
    mdb_spitData = mdb_client.spitDataVZero
    for frame in possibleFrames:
        # determing main file shit
        main_file = frame.main_file
        main_file_metadata = {}
        type_complex = frame.type_complex
        type_simple = frame.type_simple
        format_simple = frame.format_simple
        print "main file " + main_file
        if main_file != "" and main_file != "NO_FILE": #fucking hell lol
            main_file_metadata = {'metadata':{'type':type_complex,'simpletype':type_simple},'filename':main_file,'downlink_endpoint':"/downlink/"+str(frame.id)+"/"+main_file+"/"}
        else:
            continue
        frame_id = frame.id:
        frameResults = mdb_spitData.find({"frame_id":frame_id})
        if len(frameResults) == 0:
            continue
        frameResultsPyList = []
        for resu in frameResults:
            frameResultsPyList.append(resu)
        finalRes = {"main_file_metadata":main_file_metadata, "parsed_info":frameResults}
    return JsonResponse({"response":framesMetadataList,"secret_message":"suck a dick brody"})

@csrf_exempt
def mindPageAPILongFormSET(request, usernameInput):
    if usernameInput == None:
        return HttpResponse(code=403)
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return HttpResponse(code=401) # differing codes reveal to blackbox testing
    possibleFrames = Frame.objects.filter(owner=possibleMind).order_by('-createdat')
    if possibleFrames == None:
        print usernameInput + " HAS NO FRAMES"
        return JsonResponse(json.dumps([])) # ;mao Im a god
    # is there a way to make this recursive? so its higher than 2
    # looking for frames
    frameMetadata = {}
    framesMetadataList = []
    for frame in possibleFrames:
        longFormSetQueryResults = LongFormSet.objects.filter(referencing_frame=frame)
        longFormSet = None
        if len(longFormSetQueryResults) > 0:
            longFormSet = longFormSetQueryResults[0]
        foldername = frame.foldername
        # determing main file shit
        main_file = frame.main_file
        main_file_metadata = {}
        print "main file " + main_file
        if main_file != "" and main_file != "NO_FILE": #fucking hell lol
            with open(foldername + main_file, 'r') as resFile:
                filebuffer = magic.from_buffer(resFile.read(1024))
                main_file_metadata = {'metadata':{'type':filebuffer,'simpletype':determineSimpleType(foldername + main_file)},'filename':main_file,'downlink_endpoint':"/downlink/"+str(frame.id)+"/"+main_file+"/"}
                resFile.close()
        else:
            continue
        # determining all dir file information, should probably mimic the file model
        foldername = frame.foldername
        files = filesInFrame(foldername)
        filesInFrameList = []
        for fil in files:
            with open(foldername + fil, 'r') as resFile:
                filebuffer = magic.from_buffer(resFile.read(1024))
                thang = {'metadata':{'type':filebuffer,'simpletype':determineSimpleType(foldername + fil)},'filename':fil,'downlink_endpoint':"/downlink/"+str(frame.id)+"/"+fil+"/"}
                print filebuffer
                slugFileType = filebuffer.split(' ')[0].lower()
                print "JSON READ " + slugFileType
                fileOutput = ""
                try:
                    # FOR THE RECORD FUCK YOU IF YOU EVER USE ASSERTION FOR PRODUCTION OR EVER AT ALL HONESTLY
                    if textFileTypes.index(slugFileType) != None:
                        print "** JSON READ DETERMINED FILE TYPE"
                        resFile.seek(0)
                        fileOutput = resFile.read()
                        print "JSON READ ASCII FILE LENGTH" + fileOutput
                        thang['text'] = json.loads(fileOutput)
                except:
                    # print traceback.print_exc() # this will not be reliable among more than 3 people honestly
                    print "**** " + fileOutput + " ****"
                    print "JSON READ well couldnt fucking do that now could I and now I threw an error for that shit bullshit"
                resFile.close()
                filesInFrameList.append(thang)
        frameMetadata = {"frameid":frame.id,"files":filesInFrameList,"foldername":foldername,"main_file":main_file, "main_file_metadata":main_file_metadata} # dictionary property
        framesMetadataList.append({"frameid":frame.id,"metadata":frameMetadata,"foldername":foldername}) # dictionary property
    return JsonResponse({"response":framesMetadataList,"secret_message":"suck a dick brody"})

def filesInFrame(frameName):
    fileList = []
    print "here 0"
    for filename in os.listdir(frameName):
        print "here 1 " + filename
        if filename!='.DS_Store':
            print "here 2 " + filename
            fileList.append(filename)
    return fileList
