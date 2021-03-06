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
LOGINTEMPLATE = CURRENTLOCATION + 'signin.html'
MINDPAGETEMPLATE = CURRENTLOCATION + 'dashboard.html'
UPLOAD_DIR_3 = os.getcwd().replace("\\","/") + "/ingestion/frames/"

textFileTypes = ["json","txt", "ascii", "text"]

DOMAIN_ENDPOINT = 'http://67.169.94.129:3000'

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
                    #content_type="audio/" + determineSimpleFormat(foldername+fil) + ";"
                    content_type="audio/m4a"
                return FileResponse(open(foldername + fil, 'rb'),content_type=content_type)
    return HttpResponse(status=404)

@csrf_exempt
def downlinkFrameSliceData(request, frameid, sliceid):
    if frameid == None:
        return HttpResponse(status=400)
    possibleFrames = Frame.objects.filter(id=frameid)
    if possibleFrames == None:
        return HttpResponse(status=401)
    # is there a way to make this recursive? so its higher than 2
    filename = "session"+str(frameid)+"-part"+str(int(sliceid)*30)+".m4a"
    for frame in possibleFrames:
        foldername = frame.foldername
        return FileResponse(open(foldername + filename, 'rb'))
        # files = filesInFrame(foldername)
        # filesInFrameList = []
        # for fil in files:
        #     if fil == filename:
        #         approx_file_type = determineSimpleType(foldername+fil)
        #         content_type = ""
        #         if approx_file_type == "image":
        #             content_type="image/" + determineSimpleFormat(foldername+fil) + ";"
        #         elif approx_file_type == "sound":
        #             content_type="audio/" + determineSimpleFormat(foldername+fil) + ";"
        #         return FileResponse(open(foldername + fil, 'rb'),content_type=content_type)
    return HttpResponse(status=404)

def loginPage(request):
    request.session['username'] = ""
    return render(request, LOGINTEMPLATE, {'inputCode':200})

@csrf_exempt
def loginRequestExempt(request):
    try:
        inputEmail = request.POST['email']
        components = inputEmail.split('@')
        username = components[0]
    except:
        return HttpResponse(status=400)
    try:
        inputPassword = request.POST['password']
    except:
        return HttpResponse(status=400)
    if inputPassword == None:
        return HttpResponse(status=400)
    users = Mind.objects.filter(email=inputEmail)
    if len(users) == 0:
        newUser = Mind.objects.create(email=inputEmail,username=username, password=inputPassword, profile_picture="[]")
        newUser.save()
        newContext = Context.objects.create(text="Miscellaneous",mind=newUser)
        newContext.save()
    elif users[0].password != inputPassword:
        return HttpResponse(status=401)
    request.session['username'] = inputUsername
    return HttpResponse(status=200)

def loginRequest(request):
    try:
        inputEmail = request.POST['email']
        components = inputEmail.split('@')
        username = components[0]
    except:
        return render(request, LOGINTEMPLATE, {'inputCode':400})
    try:
        inputPassword = request.POST['password']
    except:
        return HttpResponse(status=400)
    users = Mind.objects.filter(username=username)
    if len(users) == 0:
        newUser = Mind.objects.create(email=inputEmail,username=username, password=inputPassword, profile_picture="[]")
        newUser.save()
        newContext = Context.objects.create(mind=newUser, text="Miscellaneous")
        newContext.save()
    elif users[0].password != inputPassword:
        return render(request, LOGINTEMPLATE, {'inputCode':401})
    request.session['username'] = username
    return redirect('/mind/'+username+'/')

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
    currentUser = ""
    try:
        currentUser = request.session['username']
    except:
        print "shit lmao"
    authed = True
    if currentUser != usernameInput:
        authed = False
        return redirect('/login/')
    framesMetadataList = framesOfUsername(usernameInput)
    return render(request, MINDPAGETEMPLATE, {'domain': DOMAIN_ENDPOINT, 'statuscode': 'recall', 'authed':authed, 'username':usernameInput, 'frames': framesMetadataList, "mode":"mind"})

def uploadPage(request):
    currentUser = ""
    try:
        currentUser = request.session['username']
    except:
        print "shit lmao"
        return redirect('/login/')
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return redirect('/login/')
    return render(request, UPLOADPAGETEMPLATE, {'domain': DOMAIN_ENDPOINT, 'statuscode': '200', 'username':usernameInput})

def createContext(request):
    try:
        currentUser = request.session['username']
        context = request.POST["context"]
    except:
        print "shit lmao"
        return HttpResponse(status=401)
    possibleMind = Mind.objects.get(username=currentUser)
    if possibleMind == None:
        return HttpResponse(status=403)
    newContext = Context.objects.create(mind=possibleMind, text=context)
    newContext.save()
    return HttpResponse(status=200)

def fetchAllContexts(usernameInput):
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return []
    contexts = Context.objects.all().filter(mind=possibleMind).order_by('-createdat')
    contextListJSON = []
    print str(len(contexts)) + " contexts for " + usernameInput
    for context in contexts:
        contextJSON = {
            "id":context.id,
            "text":context.text,
            "createdat_string":unicode(context.createdat)
        }
        contextListJSON.append(contextJSON)
    return contextListJSON


def contextPage(request, contextId):
    currentUser = ""
    try:
        currentUser = request.session['username']
    except:
        print "shit lmao"
        return redirect('/login/')
    authed = True
    possibleMind = Mind.objects.get(username=currentUser)
    if possibleMind == None:
        return HttpResponse(status=403)
    contexts = Context.objects.all().filter(id=contextId,mind=possibleMind)
    if len(contexts) == 0:
        return redirect('/mind/'+currentUser+'/')
    context = contexts[0]
    return render(request, MINDPAGETEMPLATE, {'domain': DOMAIN_ENDPOINT, 'statuscode': 'recall', 'authed':authed, 'context_name':context.text, "mode":"context"})

def contextPageAPI(contextId):
    try:
        currentUser = request.GET['context']
    except:
        print "shit lmao"
        return HttpResponse(status=401)
    possibleMind = Mind.objects.get(username=currentUser)
    if possibleMind == None:
        return {"status":"no user"}
    contexts = Context.objects.all().filter(id=contextId,mind=possibleMind)
    if len(contexts) == 0:
        return {"status":"no contexts"}
    context = contexts[0]
    contextJSON = {
        "id":context.id,
        "text":context.text,
        "createdat_string":unicode(context.createdat),
        "frames":framesOfContext(context)
    }
    return {"response":contextJSON,"status":"good"}

@csrf_exempt
def framesPageAPI(request,usernameInput):
    if usernameInput == None:
        return HttpResponse(status=403)
    contextMetadataList = fetchAllContexts(usernameInput)
    return  JsonResponse({"response":contextMetadataList,"secret_message":"osiris reigns"})

@csrf_exempt
def mindPageAPIV2(request, usernameInput):
    if usernameInput == None:
        return HttpResponse(status=403)
    framesMetadataList = framesOfUsername(usernameInput)
    return JsonResponse({"response":framesMetadataList,"secret_message":"suck a dick brody"})

@csrf_exempt
def termsPageAPIV1(request, usernameInput):
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return HttpResponse(status=401) # differing codes reveal to blackbox testing
    termSetEntries = TermSet.objects.filter(user_parent=possibleMind.id).order_by('-createdat')
    result = []
    for termSetEntry in termSetEntries:
        termDict = termSetEntry.toDictionary()
        result.append(termDict)
    return JsonResponse({"response":result,"secret_message":"suck a dick brody"})

def framesOfUsername(usernameInput):
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return HttpResponse(status=401) # differing codes reveal to blackbox testing
    possibleFrames = Frame.objects.filter(owner=possibleMind).order_by('-createdat')
    if possibleFrames == None:
        print usernameInput + " HAS NO FRAMES"
        return JsonResponse(json.dumps([])) # ;mao Im a god
    print "user " + usernameInput + " has " + str(len(possibleFrames)) + " frames"
    frameMetadata = {}
    framesMetadataList = []
    mdb_client = MongoClient('localhost', 27017)
    mdb_spitData = mdb_client.spitDataVZero
    for frame in possibleFrames:
        # determing main file shit
        main_file = frame.main_file
        main_file_metadata = {}
        type_complex = frame.type_complex
        type_simple = frame.type_simple
        format_simple = frame.format_simple
        context_id = frame.context.id
        contexts = Context.objects.all().filter(id=context_id,mind=possibleMind)
        context_name = ""
        if len(contexts) > 0:
            context_name = contexts[0].text
        print "main file " + main_file
        if main_file != "" and main_file != "NO_FILE": #fucking hell lol
            main_file_metadata = {'metadata':{'type':type_complex,'simpletype':type_simple}, "createdat_string":frame.createdat_string,'filename':main_file,'downlink_endpoint':"/downlink/"+str(frame.id)+"/"+main_file+"/"}
        else:
            continue
        frame_id = frame.id
        frameResults = vomitJSONAPIResultstoAPI(frame_id)
        finalRes = {"main_file_metadata":main_file_metadata, "notes":frame.notes, "context_id":context_id, "context_name":context_name, "notes":frame.notes, "parsed_info":frameResults, 'frame_id':frame.id, "slice_downlink_endpoint":"/slice-downlink/"}
        framesMetadataList.append(finalRes)
    return framesMetadataList

def framesOfContext(context):
    possibleFrames = Frame.objects.filter(context=context).order_by('-createdat')
    if possibleFrames == None:
        print context + " HAS NO FRAMES"
        return []
    print "context " + str(context.id) + " has " + str(len(possibleFrames)) + " frames"
    frameMetadata = {}
    framesMetadataList = []
    mdb_client = MongoClient('localhost', 27017)
    mdb_spitData = mdb_client.spitDataVZero
    for frame in possibleFrames:
        # determing main file shit
        main_file = frame.main_file
        main_file_metadata = {}
        type_complex = frame.type_complex
        type_simple = frame.type_simple
        format_simple = frame.format_simple
        context_id = frame.context.id
        contexts = Context.objects.all().filter(id=context_id,mind=possibleMind)
        context_name = ""
        if len(contexts) > 0:
            context_name = contexts[0].text
        print "main file " + main_file
        if main_file != "" and main_file != "NO_FILE": #fucking hell lol
            main_file_metadata = {'metadata':{'type':type_complex,'simpletype':type_simple}, "createdat_string":frame.createdat_string,'filename':main_file,'downlink_endpoint':"/downlink/"+str(frame.id)+"/"+main_file+"/"}
        else:
            continue
        frame_id = frame.id
        frameResults = vomitJSONAPIResultstoAPI(frame_id)
        finalRes = {"main_file_metadata":main_file_metadata, "notes":frame.notes, "context_id":context_id, "context_name":context_name, "notes":frame.notes, "parsed_info":frameResults, 'frame_id':frame.id, "slice_downlink_endpoint":"/slice-downlink/"}
        framesMetadataList.append(finalRes)
    return framesMetadataList

# this will be a way to force client alignment. They can access via SLUGS or POST
@csrf_exempt
def mindPageAPIPOST(request):
    try:
        usernameInput = request.POST['username']
    except:
        print "missing username"
        return HttpResponse(status=403)
    return mindPageAPI(request, usernameInput)

@csrf_exempt
def mindPageAPI(request, usernameInput):
    if usernameInput == None:
        return HttpResponse(status=403)
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return HttpResponse(status=401) # differing codes reveal to blackbox testing
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
def mindPageAPILongFormSET(request, usernameInput):
    if usernameInput == None:
        return HttpResponse(status=403)
    possibleMind = Mind.objects.get(username=usernameInput)
    if possibleMind == None:
        return HttpResponse(status=401) # differing codes reveal to blackbox testing
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
