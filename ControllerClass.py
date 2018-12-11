from scrapewiki import QuestionMaker


class Controller(object):
    
    answer = ""
    goodQuestions = []
    #def __init__(self):
    #    self.answer = answer

    def DeployQuestion(self):

        try:
            questionObject = QuestionMaker()
            questionObject = questionObject.quiz()
            
            return questionObject
        except ValueError:
            return "Something went wrong"
        '''
        someList = [{"Question" :["skr skrr",
                    "ey mang",
                    "Shit mang , that shit is wack mang uashd soajdo sao odoo dso od oasas ddo aos doa ods odsd do do",
                    "brrRRaah"]}]
        '''
        

    def ProcessAnswer(self):
        print(self.answer)

#con = Controller()
#con.DeployQuestion()