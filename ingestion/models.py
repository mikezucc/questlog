# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Mind(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    profile_picture = models.CharField(max_length=250)
    datejoined = models.DateTimeField(auto_now_add=True)
    metadata = {}

# this implies that there is a quantization to time domain
class Frame(models.Model):
    owner = models.ForeignKey(Mind, on_delete=models.CASCADE)
    foldername = models.CharField(max_length=50)
    createdat = models.DateTimeField(auto_now_add=True)
    metadata = {}

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

class WebSet(models.Model):
    web_raw = models.CharField(max_length=200)
    google_entity_id = models.CharField(max_length=50)
    metadata = {}

class AllWeb(models.Model):
    web_raw = models.CharField(max_length=300)
    web_set_parent = models.ForeignKey(PhraseSet, on_delete=models.CASCADE)
    referencing_frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
