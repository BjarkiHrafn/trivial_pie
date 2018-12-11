import requests
import re
import json


from scrapewiki import findAGoodQuestion, quiz

class Controller(object):
    answer = ""

    def DeployQuestion(self):

        try:
            print(quiz())
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
        