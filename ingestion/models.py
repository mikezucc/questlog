# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Mind(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    profile_picture = models.CharField(max_length=250)
    datejoined = models.DateTimeField(auto_now_add=True)

# this implies that there is a quantization to time domain
class Frame(models.Model):
    owner = models.ForeignKey(Mind, on_delete=models.CASCADE)
    foldername = models.CharField(max_length=50)
    createdat = models.DateTimeField(auto_now_add=True)
    metadata = {}
