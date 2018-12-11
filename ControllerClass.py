from scrapewiki import findAGoodQuestion, quiz


class Controller(object):
    answer = ""
    def __init__(self):
        self.answer = []

    def DeployQuestion(self):

        try:
            questionObject = quiz()
            optionDictionary = {}
            question = questionObject[0]

            for x, y in questionObject[1]:
                optionDictionary[x] = y
            print(optionDictionary)
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


con = Controller()
con.DeployQuestion()