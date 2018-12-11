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

    # adds a question to the goodQuestions collection
    # if question already exists only increments the
    # coodness value by 1

    def addToGoodQuestions(self, data):
        data['options'] = tuple(data['options'])
        #data['goodness'] += 1
        self.goodQuestions.find_one_and_update(
            data, {'$inc': {"goodness": 1}}, upsert=True)
        return "tibi"

    def findQuestionByTitle(self, title):
        question = self.goodQuestions.find_one({"title": title})
        return question


# test
# rep = repository()
# q = questionMaker.QuestionMaker()
# rep.addToGoodQuestions(q.quiz())
