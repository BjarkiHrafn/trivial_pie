import pymongo
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId


class repository(object):
    # connectionstring to a mongo database on mlab
    def __init__(self, name):
        MONGODB_URI = "mongodb://abc123:abc123@ds011422.mlab.com:11422/pie"
        client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
        self.db = client.get_database("pie")
        self.goodQuestions = self.db.goodQuestions

    def getAllGoodQuestionsInOrderOfBestQuestions(self):
        testVals = []
        for document in self.goodQuestions.find().sort('points', pymongo.DESCENDING):
            testVals.append(document)
        return testVals

    def addToGoodQuestions(self, data):
        # TODO: create data on json format?
        # postData = {
        #     "points": data.poitns

        # }
        self.goodQuestions.insert_one(data)
        return data

    def raisGoodQuestionValueById(self, id):
        # TODO: is id on ObjectId format?
        #       if not ObjectId(id)
        #       should the fields name be points?
        updated = self.goodQuestions.find_one_and_update({"_id": id}, {
            "$inc": {"points": 1}}, return_document=ReturnDocument.AFTER)
        return updated
