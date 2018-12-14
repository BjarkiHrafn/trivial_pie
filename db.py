from bson.objectid import ObjectId
from pymongo import MongoClient, ReturnDocument
import pymongo
import questionMaker


class Repository(object):
    # connectionstring to a mongo database on mlab
    def __init__(self):
        MONGODB_URI = "mongodb://abc123:abc123@ds011422.mlab.com:11422/pie"
        client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
        self.db = client.get_database("pie")
        self.goodQuestions = self.db.goodQuestions
        self.survivalHighScore = self.db.survivalHighScore
        self.quizHighScore = self.db.quizHighScore

    def getAllGoodQuestionsInOrderOfBestQuestions(self):
        goodQuestionLis = []
        dictObject = {}
        for document in self.goodQuestions.find().sort('goodness', pymongo.DESCENDING):
            dictObject = {
                'options': [tuple(x) for x in document['options']],
                'title': document['title'],
                'goodness': document['goodness']
            }
            goodQuestionLis.append(dictObject)
        return goodQuestionLis

    ### --- Good Questions --- ###

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

    def findQuestionByTitle(self, title):
        question = self.goodQuestions.find_one({"title": title})
        return question

    ### --- Hich Score --- ###

    def getSurvivalHighscore(self):
        highScoreLis = []
        for document in self.survivalHighScore.find().sort('score', pymongo.DESCENDING):
            highScoreLis.append(document)
        return highScoreLis

    def addSurvivalHichScore(self, data):
        self.survivalHighScore.insert_one(data)
        return data

    def getQuizHighscore(self):
        highScoreLis = []

        for document in self.quizHighScore.find().sort('score.1', pymongo.DESCENDING):
            highScoreLis.append(document)
        return highScoreLis

    def addQuizHighScore(self, data):
        self.quizHighScore.insert_one(data)
        return data
