from questionMaker import QuestionMaker
from threading import Thread
import random

class Controller(object):
    
    answer = ""
    goodQuestions = []
    survivalModeLives = 1
    survivalModeArray = []
    #def __init__(self):
    #    self.answer = answer

    def DeployQuestion(self):
        
        try:
            q = QuestionMaker()
            options = [q.quiz, q.titleQuiz, q.trueOrFalse]
            questionObject = random.choice(options)()
            '''
            threads = []    
            questions = {}
            for i in range(5):
                process = Thread(target=questionObject.quiz, args=(questions))
                
                process.start()
                threads.append(process)
            
            for process in threads:
               
                process.join()
            print(questions)
            for q in questions:
                print(q)
            '''

            return questionObject

        except ValueError:
            return "Something went wrong"
        

    def ProcessAnswer(self):
        print(self.answer)
