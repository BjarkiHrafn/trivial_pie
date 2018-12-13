from questionMaker import QuestionMaker
from threading import Lock
from threading import Thread
from queue import Queue
import time
import random


class Controller(object):

    answer = ""
    goodQuestions = []
    survivalModeLives = 5
    survivalModeArray = []
    quizModeArray = []
    correctAnswerArray = []
    currentGameMode = ""
    numberOfQuestionsForQuiz = 5
    #self.answer = answer

    def DeployQuestion(self, numbOfQuest):

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

    def ProcessAnswer(self):
        print(self.answer)
