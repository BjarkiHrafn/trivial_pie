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
            {
                "title": data["title"],
                "options": data["options"]
            }, {'$inc': {"goodness": 1}}, upsert=True)
        return "tibi"

    def findQuestionByTitle(self, title):
        question = self.goodQuestions.find_one({"title": title})
        return question


# test
rep = repository()

data = {'title': 'Roderich Moessner', 'options': [("*bleep* is tracy chapman's seventh studio album and was released september 13, 2005.", False), ('*bleep* is acondensed matter physicist working on the physics of strong fluctuations in many-body systems due to frustration, competing degrees of freedom or quantum fluctuations.', True), (
    '*bleep* refers to pieces of broken glass (typically from a window) which become sharp missiles projected by the force which broke the glass, along with any strain energy due to tempering.', False), ('at 1,176.6 m above sea level (nhn) the *bleep* is the third highest mountain of the central black forest after the  kandel and the weißtannenhöhe.', False)], 'goodness': 0}


rep.addToGoodQuestions(data)
