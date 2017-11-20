from pymongo import MongoClient
from bson.json_util import dumps

# ok so heres the basic idea with this. we want to design the core technology in such a way where
# the actual data stores and tables can be very easily switched to different service providers.
# we can remain independent and very amacable towards liftandshifts
# say amazon or google were to acquire us, we would have very minimal effort
# trying to align the outputs from our architecture into their services

# the following code sort of assumes that the database should be able to receiver
# some sort of serialized model-as-a-document
# Each table will depict a feature

# maybe there should be some sort of simple keypath mapping to the document names
# these use the MessageToJson serializing gRPC. Kind of odd that now wwwwwwwwwwe go baaaaaaaaack to json
#passing                  binary through the internet lol also my bkeyboar is having trouble
# with the bluetooth on ubuntu. open source? lol still very very good job         boyss

def spitJSONAPIResulttoMDB(json, featureName, frame_id, user_id):
    # form new db connection each time to allow better engine threading
    mdb_client = MongoClient('localhost', 27017)
    mdb_spitData = mdb_client.spitDataVZero
    json["frame_id"] = frame_id
    json["user_id"] = user_id
    if featureName == "audio_speech_google":
        documents = mdb_spitData.audio_speech_google
    elif featureName == "text_ocr_google":
        documents = mdb_spitData.text_ocr_google
    elif featureName == "labels_ocr_google":
        documents = mdb_spitData.labels_ocr_google
    elif featureName == "web_ocr_google":
        documents = mdb_spitData.web_ocr_google
    elif featureName == "document_ocr_google":
        documents = mdb_spitData.document_ocr_google
    else:
        return
    res = documents.insert_one(json)
    print "Saved to database " + "{}".format(res.inserted_id)


def vomitJSONAPIResultstoAPI(frame_id):
    mdb_client = MongoClient('localhost', 27017)
    mdb_spitData = mdb_client.spitDataVZero
    mappedRes = {}
    for res in mdb_spitData.audio_speech_google.find({"frame_id":frame_id}):
        res['_id'] = ""
        mappedRes["speech"] = res
    for res in mdb_spitData.text_ocr_google.find({"frame_id":frame_id}):
        res['_id'] = ""
        mappedRes["ocr_text"] = res
    for res in mdb_spitData.labels_ocr_google.find({"frame_id":frame_id}):
        res['_id'] = ""
        mappedRes["ocr_label"] = res
    for res in mdb_spitData.web_ocr_google.find({"frame_id":frame_id}):
        res['_id'] = ""
        mappedRes["ocr_web"] = res
    for res in mdb_spitData.document_ocr_google.find({"frame_id":frame_id}):
        res['_id'] = ""
        mappedRes["ocr_document"] = res
    return mappedRes
