from bson.objectid import ObjectId
from pymongo import MongoClient, ReturnDocument
import pymongo

import json

import questionMaker


class repository(object):
    # connectionstring to a mongo database on mlab
    def __init__(self):
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
        print("data: ", data)
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
            "$inc": {"goodness": 1}}, return_document=ReturnDocument.AFTER)
        return updated

    def findQuestionByTitle(self, title):
        question = self.goodQuestions.find_one({"title": title})
        return question


# test
rep = repository()
q = questionMaker.QuestionMaker()

tibi = json.dumps(q.quiz())
print(tibi)

# rep.addToGoodQuestions()
