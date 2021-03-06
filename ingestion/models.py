# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Mind(models.Model):
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250,default="")
    password = models.CharField(max_length=250)
    profile_picture = models.CharField(max_length=250)
    datejoined = models.DateTimeField(auto_now_add=True)
    metadata = {}

class Context(models.Model):
    mind = models.ForeignKey(Mind, on_delete=models.CASCADE)
    text = models.CharField(max_length=250,default="")
    createdat = models.DateTimeField(auto_now_add=True)
    metadata = {}

# this implies that there is a quantization to time domain
class Frame(models.Model):
    owner = models.ForeignKey(Mind, on_delete=models.CASCADE)
    foldername = models.CharField(max_length=200)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    notes = models.CharField(max_length=2000)
    main_file = models.CharField(max_length=300, default="")
    createdat = models.DateTimeField(auto_now_add=True)
    createdat_string = models.CharField(max_length=300, default="")
    type_complex = models.CharField(max_length=300, default="")
    type_simple = models.CharField(max_length=300, default="")
    format_simple = models.CharField(max_length=300, default="")
    metadata = {}

# Keeps track of all unique identities related to a user
class Conversant(models.Model):
    owner = models.ForeignKey(Mind, on_delete=models.CASCADE)
    relative_mind = models.ForeignKey(Mind, on_delete=models.CASCADE, blank=True, null=True)
    human_name = models.CharField(max_length=200)

# Links
class ImportantConversationChunks(models.Model):
    owner = models.ForeignKey(Mind, on_delete=models.CASCADE)
    relative_mind = models.ForeignKey(Conversant, on_delete=models.CASCADE, blank=True, null=True)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, blank=True, null=True)

class Tag(models.Model):
    owner = models.ForeignKey(Mind, on_delete=models.CASCADE)
    term_raw = models.CharField(max_length=100)
    metadata = {}

    def toDictionary():
        return {"owner":owner,
                "term_raw":term_raw,
                "createdat":"{}".format(createdat)}

# these appear to be used with the audio transcription
class TermSet(models.Model):
    user_parent = models.ForeignKey(Mind, on_delete=models.CASCADE)
    term_raw = models.CharField(max_length=100)
    google_entity_id = models.CharField(max_length=50)
    rough_count = models.IntegerField()
    createdat = models.DateTimeField(auto_now_add=True)
    metadata = {}

    def toDictionary():
        return {"user_parent":user_parent,
                "term_raw":term_raw,
                "google_entity_id":google_entity_id,
                "rough_count":rough_count,
                "createdat":"{}".format(createdat)}

class AllTerms(models.Model):
    term_raw = models.CharField(max_length=100)
    start_time = models.IntegerField()
    user_parent = models.ForeignKey(Mind, on_delete=models.CASCADE)
    term_set_parent = models.ForeignKey(TermSet, on_delete=models.CASCADE)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    createdat = models.DateTimeField(auto_now_add=True)
    metadata = {}

    def toDictionary():
        return {"user_parent":user_parent,
                "term_raw":term_raw,
                "start_time":start_time,
                "term_set_parent":term_set_parent,
                "referencing_frame":referencing_frame,
                "createdat":"{}".format(createdat)}

class LongFormSet(models.Model):
    long_form_string = models.CharField(max_length=500)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)

class PhraseSet(models.Model):
    phrase_raw = models.CharField(max_length=200)
    metadata = {}

class AllPhrases(models.Model):
    phrase_raw = models.CharField(max_length=200)
    phrase_set_parent = models.ForeignKey(PhraseSet, on_delete=models.CASCADE)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    metadata = {}

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

class LabelSet(models.Model):
    label_raw = models.CharField(max_length=200)
    google_entity_id = models.CharField(max_length=50)
    metadata = {}

class AllLabels(models.Model):
    label_raw = models.CharField(max_length=300)
    label_set_parent = models.ForeignKey(LabelSet, on_delete=models.CASCADE)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    metadata = {}
