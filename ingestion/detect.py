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
from enum import Enum

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

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
    highlight_faces(path, faces, path[:-4] + '-detectfaces' + path[-4:])

    # jsonRes = MessageToJson(faces)
    # with open(path+"-faces.json", 'wb+') as jsonAPIResultsFile:
    #     print jsonRes
    #     jsonAPIResultsFile.write(jsonRes)
    #     jsonAPIResultsFile.close()
    #     return 200
    #  return 400
    return 200
    # [END migration_face_detection]
# [END def_detect_faces]

def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save(output_filename)


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
    highlight_faces(path, faces, path[:-4] + '-detectfaces' + path[-4:])

    # jsonRes = MessageToJson(faces)
    # with open(path+"-faces.json", 'wb+') as jsonAPIResultsFile:
    #     print jsonRes
    #     jsonAPIResultsFile.write(jsonRes)
    #     jsonAPIResultsFile.close()
    #     return 200
    #  return 400
    return 200
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

    labelsList = []
    for label in labels:
        labelsList.append(label.description)
    labelJSON = {"labels":labelsList}

    jsonRes = json.dumps(labelJSON)
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

    labelsList = []
    for label in labels:
        labelsList.append(label.description)
    labelJSON = {"labels":labelsList}

    jsonRes = json.dumps(labelJSON)
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

    landmarksList = []
    for landmark in landmarks:
        print(landmark.description)
        landmarksList.append(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude'.format(lat_lng.latitude))
            print('Longitude'.format(lat_lng.longitude))
    landmarksJSON = {"landmarks":landmarksList}
    jsonRes = json.dumps(landmarksJSON)
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

    landmarksList = []
    for landmark in landmarks:
        landmarksList.append(landmark.description)
        print(landmark.description)

    landmarksJSON = {"landmarks":landmarksList}
    jsonRes = json.dumps(landmarksJSON)
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

    logosList = []
    for logo in logos:
        logosList.append(logo.description)
        print(logo.description)

    logosJSON = {"logos":logosList}
    jsonRes = json.dumps(logosJSON)
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

    logosList = []
    for logo in logos:
        logosList.append(logo.description)
        print(logo.description)

    logosJSON = {"logos":logosList}
    jsonRes = json.dumps(logosJSON)
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

    textsList = []
    for text in texts:
        textsList.append(text.description)
        # print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    textsJSON = {"texts":textsList}
    jsonRes = json.dumps(textsJSON)
    with open(path+"-text.json", 'wb+') as jsonAPIResultsFile:
        # print jsonRes
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

    textsList = []
    for text in texts:
        textsList.append(text.description)
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    textsJSON = {"texts":textsList}
    jsonRes = json.dumps(textsJSON)
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

    colorsList = []
    for color in props.dominant_colors.colors:
        jsonFriendly = {"fraction":color.pixel_fraction,
        "red": (color.color.red if color.color.red != None else 0.0),
        "green":(color.color.green if color.color.green != None else 0.0),
        "alpha":(color.color.alpha if color.color.alpha != None else 0.0),
        "blue":(color.color.blue if color.color.blue != None else 0.0)}
        if jsonFriendly['alpha'] == None:
            jsonFriendly['alpha'] = 1.0
        elif len(str(jsonFriendly['alpha'])) < 2:
             jsonFriendly['alpha'] = 1.0
        colorsList.append(jsonFriendly)
        # print('\tr: {}'.format(color.color.red))
        # print('fraction: {}'.format(color.pixel_fraction))
        # print('\tg: {}'.format(color.color.green))
        # print('\tb: {}'.format(color.color.blue))
        # print('\ta: {}'.format(color.color.alpha))
    colorsJSON = {"colors":colorsList}
    print colorsJSON
    jsonRes = json.dumps(colorsJSON)
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

    colorsList = []
    for color in props.dominant_colors.colors:
        colorsList.append({"fraction":color.pixel_fraction,"red":color.color.red,"green":color.color.green,"blue":color.color.blue,"alpha":color.color.alpha})
        print('\tr: {}'.format(color.color.red))
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))
    colorsJSON = {"colors":colorsList}
    jsonRes = json.dumps(colorsJSON)
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

def draw_hint(image_file, vects, hintNumber):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_hint]

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)
    draw.polygon([
        vects[0].x, vects[0].y,
        vects[1].x, vects[1].y,
        vects[2].x, vects[2].y,
        vects[3].x, vects[3].y], None, 'red')
    im.save(image_file + "-" + str(hintNumber) + image_file[-4:])
    # [END draw_hint]
    return vects


def crop_to_hint(image_file, vects, hintNumber):
    """Crop the image using the hints in the vector list."""
    # [START crop_to_hint

    im = Image.open(image_file)
    im2 = im.crop([vects[0].x, vects[0].y,
                  vects[2].x - 1, vects[2].y - 1])
    im.save(image_file + "-" + str(hintNumber) + image_file[-4:])
    # [END crop_to_hint]
    return vects

# [START def_detect_crop_hints]
def detect_crop_hints(path):
    print "Detects crop hints in an image." + path
    client = vision.ImageAnnotatorClient()

    # [START migration_crop_hints]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    # worth looking at this bullshit constant right here
    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    cropHintsList = []
    count = 0
    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))
        crop_to_hint(path, hint.bounding_poly.vertices, count)
        count = count + 1
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))
        vertexes = []
        for vertex in hint.bounding_poly.vertices:
            vertexes.append({"x":vertex.x,"y":vertex.y})
        cropHintsList.append(vertexes)

    cropHintsJSON = {"crophints":cropHintsList}
    jsonRes = json.dumps(cropHintsJSON)
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

    cropHintsList = []
    count = 0
    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))
        crop_to_hint(path, hint.bounding_poly.vertices, count)
        count = count + 1
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))
        vertexes = []
        for vertex in hint.bounding_poly.vertices:
            vertexes.append({"x":vertex.x,"y":vertex.y})
        cropHintsList.append(vertexes)

    cropHintsJSON = {"crophints":cropHintsList}
    jsonRes = json.dumps(cropHintsJSON)
    with open(path+"-crophints.json", 'wb+') as jsonAPIResultsFile:
        print jsonRes
        jsonAPIResultsFile.write(jsonRes)
        jsonAPIResultsFile.close()
        return 200
    return 400
# [END def_detect_crop_hints_uri]

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_blocks]
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image
    # [END draw_blocks]

def get_document_bounds(document, feature):
    # [START detect_bounds]
    # Collect specified feature bounds by enumerating all document features
    bounds = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    # [END detect_bounds]
    return bounds

def render_doc_text(document, filein, fileout):
    # [START render_doc_text]
    image = Image.open(filein)
    bounds = get_document_bounds(document, FeatureType.PAGE)
    draw_boxes(image, bounds, 'blue')
    bounds = get_document_bounds(document, FeatureType.PARA)
    draw_boxes(image, bounds, 'red')
    bounds = get_document_bounds(document, FeatureType.WORD)
    draw_boxes(image, bounds, 'yellow')

    image.save(fileout)
    # [END render_doc_text]

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

    render_doc_text(document, path, path[:-4] + '-textboxes' + path[-4:])

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

            # print('Block Content: {}'.format(block_text))
            # print('Block Bounds:\n {}'.format(block.bounding_box))

    jsonRes = MessageToJson(response)
    with open(path+"-document.json", 'wb+') as jsonAPIResultsFile:
        # print jsonRes
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
        detect_document(path)
    except Exception as e:
        print traceback.format_exc()
