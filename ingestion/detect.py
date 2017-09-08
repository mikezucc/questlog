#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations with the
Google Cloud Vision API.

Example Usage:
python detect.py text ./resources/wakeupcat.jpg
python detect.py labels ./resources/landmark.jpg
python detect.py web ./resources/landmark.jpg
python detect.py web-uri http://wheresgus.com/dog.JPG
python detect.py faces-uri gs://your-bucket/file.jpg

For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import io
import json
from google.protobuf.json_format import MessageToJson
import traceback

from google.cloud import vision
from google.cloud.vision import types

# [START def_detect_faces]
def detect_faces(path):
    print "Detects faces in an image." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_face_detection]
    # [START migration_image_file]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    # [END migration_image_file]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    jsonRes = MessageToJson(faces)
    with open(path+"-faces.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_face_detection]
# [END def_detect_faces]


# [START def_detect_faces_uri]
def detect_faces_uri(uri):
    print "Detects faces in the file located in Google Cloud Storage or the web." + uri
    client = vision.ImageAnnotatorClient()
    # [START migration_image_uri]
    image = types.Image()
    image.source.image_uri = uri
    # [END migration_image_uri]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
    jsonRes = MessageToJson(faces)
    with open(path+"-faces.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_faces_uri]


# [START def_detect_labels]
def detect_labels(path):
    print "Detects labels in the file." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

    jsonRes = MessageToJson(labels)
    with open(path+"-labels.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_label_detection]
# [END def_detect_labels]


# [START def_detect_labels_uri]
def detect_labels_uri(uri):
    print "Detects labels in the file located in Google Cloud Storage or on the Web." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

    jsonRes = MessageToJson(labels)
    with open(path+"-labels.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_labels_uri]


# [START def_detect_landmarks]
def detect_landmarks(path):
    print "Detects landmarks in the file." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_landmark_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude'.format(lat_lng.latitude))
            print('Longitude'.format(lat_lng.longitude))

    jsonRes = MessageToJson(landmarks)
    with open(path+"-landmarks.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_landmark_detection]
# [END def_detect_landmarks]


# [START def_detect_landmarks_uri]
def detect_landmarks_uri(uri):
    print "Detects landmarks in the file located in Google Cloud Storage or on the Web." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)

    jsonRes = MessageToJson(landmarks)
    with open(path+"-landmarks.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_landmarks_uri]


# [START def_detect_logos]
def detect_logos(path):
    print "Detects logos in the file." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_logo_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

    jsonRes = MessageToJson(logos)
    with open(path+"-logos.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_logo_detection]
# [END def_detect_logos]


# [START def_detect_logos_uri]
def detect_logos_uri(uri):
    print "Detects logos in the file located in Google Cloud Storage or on the Web." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

    jsonRes = MessageToJson(logos)
    with open(path+"-logos.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_logos_uri]


# [START def_detect_safe_search]
def detect_safe_search(path):
    print "Detects unsafe features in the file." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_safe_search_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search:')

    print('adult: {}'.format(likelihood_name[safe.adult]))
    print('medical: {}'.format(likelihood_name[safe.medical]))
    print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))


    # [END migration_safe_search_detection]
# [END def_detect_safe_search]


# [START def_detect_safe_search_uri]
def detect_safe_search_uri(uri):
    print "Detects unsafe features in the file located in Google Cloud Storage or on the Web." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search:')

    print('adult: {}'.format(likelihood_name[safe.adult]))
    print('medical: {}'.format(likelihood_name[safe.medical]))
    print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))
# [END def_detect_safe_search_uri]


# [START def_detect_text]
def detect_text(path):
    print "Detects text in the file." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    jsonRes = MessageToJson(texts)
    with open(path+"-text.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_text_detection]
# [END def_detect_text]


# [START def_detect_text_uri]
def detect_text_uri(uri):
    print "Detects text in the file located in Google Cloud Storage or on the Web." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    jsonRes = MessageToJson(texts)
    with open(path+"-text.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_text_uri]


# [START def_detect_properties]
def detect_properties(path):
    print "Detects image properties in the file." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_image_properties]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))

    jsonRes = MessageToJson(response)
    with open(path+"-properties.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_image_properties]
# [END def_detect_properties]


# [START def_detect_properties_uri]
def detect_properties_uri(uri):
    print "Detects image properties in the file located in Google Cloud Storage or on the Web." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('frac: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))

    jsonRes = MessageToJson(response)
    with open(path+"-properties.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_properties_uri]


# [START def_detect_web]
def detect_web(path):
    print "Detects web annotations given an image." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_web_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.web_detection(image=image)
    notes = response.web_detection

    if notes.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved')

        for page in notes.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if notes.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(notes.full_matching_images)))

        for image in notes.full_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(notes.partial_matching_images)))

        for image in notes.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.web_entities:
        print ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))

    jsonRes = MessageToJson(response)
    with open(path+"-web.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_web_detection]
# [END def_detect_web]


# [START def_detect_web_uri]
def detect_web_uri(uri):
    print "Detects web annotations in the file located in Google Cloud Storage." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.web_detection(image=image)
    notes = response.web_detection

    if notes.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved')

        for page in notes.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if notes.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(notes.full_matching_images)))

        for image in notes.full_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(notes.partial_matching_images)))

        for image in notes.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.web_entities:
        print ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))

    jsonRes = MessageToJson(response)
    with open(path+"-web.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_web_uri]


# [START def_detect_crop_hints]
def detect_crop_hints(path):
    print "Detects crop hints in an image." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_crop_hints]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    jsonRes = MessageToJson(response)
    with open(path+"-crophints.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_crop_hints]
# [END def_detect_crop_hints]


# [START def_detect_crop_hints_uri]
def detect_crop_hints_uri(uri):
    print "Detects crop hints in the file located in Google Cloud Storage." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    jsonRes = MessageToJson(response)
    with open(path+"-crophints.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_crop_hints_uri]


# [START def_detect_document]
def detect_document(path):
    print "Detects document features in an image." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_document_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            print('Block Content: {}'.format(block_text))
            print('Block Bounds:\n {}'.format(block.bounding_box))

    jsonRes = MessageToJson(response)
    with open(path+"-document.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
    # [END migration_document_text_detection]
# [END def_detect_document]


# [START def_detect_document_uri]
def detect_document_uri(uri):
    print "Detects document features in the file located in Google Cloud Storage." + uri
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            print('Block Content: {}'.format(block_text))
            print('Block Bounds:\n {}'.format(block.bounding_box))
    jsonRes = MessageToJson(response)
    with open(path+"-document.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_document_uri]

def runGoogleVisionSuite(path):
    try:
        detect_faces(path)
    except Exception as e:
        print traceback.format_exc()
    try:
        detect_labels(path)
    except Exception as e:
        print traceback.format_exc()
    try:
        detect_landmarks(path)
    except Exception as e:
        print traceback.format_exc()
    try:
        detect_logos(path)
    except Exception as e:
        print traceback.format_exc()
    try:
        detect_text(path)
    except Exception as e:
        print traceback.format_exc()
    try:
        detect_properties(path)
    except Exception as e:
        print traceback.format_exc()
    try:
        detect_web(path)
    except Exception as e:
        print traceback.format_exc()
    try:
        detect_crop_hints(path)
    except Exception as e:
        print traceback.format_exc()
    try:
        detect_document(path)(path)
    except Exception as e:
        print traceback.format_exc()
