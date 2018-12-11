from scrapewiki import QuestionMaker
from threading import Thread

class Controller(object):
    
    answer = ""
    goodQuestions = []
    #def __init__(self):
    #    self.answer = answer

    def DeployQuestion(self):

        try:
            consQuest = QuestionMaker()
            questionObject = consQuest.quiz()
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

con = Controller()
con.DeployQuestion()