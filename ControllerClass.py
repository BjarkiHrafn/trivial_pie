from questionMaker import QuestionMaker
from threading import Lock, Thread
from queue import Queue
import time
import random
import db


class Controller(object):


    def __init__(self):
        self.answer = ""
        self.goodQuestions = []
        self.survivalModeLives = 5
        self.survivalModeArray = []
        self.quizModeArray = []
        self.correctAnswerArray = []
        self.currentGameMode = ""
        self.numberOfQuestionsForQuiz = 10
        self.currentScoreSurvival = 0
        self.currentScoreQuiz = 0
        self.listOFGoodQuestionsAlreadyAdded = self.deployGoodQuestion()

    def deployQuestion(self, numbOfQuest):

        questions = []
        getLock = Lock()
        q = QuestionMaker()
        options = [q.quiz, q.titleQuiz, q.trueOrFalse]

        def addToQuestions():
            questionObject = random.choice(options)()
            with getLock:
                questions.append(questionObject)

        for i in range(numbOfQuest):
            process = Thread(target=addToQuestions)
            # thread dies when main thread dies
            process.daemon = True
            process.start()

        process.join()

        # wait for all the questions to arrive
        while True:
            if len(questions) == numbOfQuest:
                break

        return questions
    def deployGoodQuestion(self):
        return db.Repository().getAllGoodQuestionsInOrderOfBestQuestions()

    def addSurvivalHichScore(self, data):
        db.Repository().addSurvivalHichScore(data)

    def addQuizHighScore(self, data):
        db.Repository().addQuizHighScore(data)

    def addToGoodQuestions(self, data):
        db.Repository().addToGoodQuestions(data)

    def getQuizHighScores(self):
        return db.Repository().getQuizHighscore()

    def getSurvivalHighScores(self):
        return db.Repository().getSurvivalHighscore()

