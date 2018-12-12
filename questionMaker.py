import re
import json
import getWiki


class QuestionMaker:

    def parseQuestion(self):
        r = getWiki.getRandomWikiQuestion()
        dir1 = json.loads(r.text) #parse json to python object
        dir2 = dir1['query']['pages']
        title = dir2[list(dir2.keys())[0]]['title'] #pageid in the dict is random so we use .keys to bypass it
        extract = dir2[list(dir2.keys())[0]]['extract']
        try:
            extract = re.search('.*?\.(?= )', extract).group() # regex for first sentnence 
            extract = re.compile(
                title.lower() + '(?= )').sub('*Bleep*', extract.lower()) #replace the key word with bleep
            extract = re.compile(
                title.lower() + '(?=\w)').sub('*Bleep*-', extract.lower()) #replace the key word with a dash so the connected chars arent lost, for comprehension sake
            extract.decode('ascii')
        except UnicodeDecodeError:
            print("it was not a ascii-encoded unicode string")
            return None
        except:
            pass
        if '*bleep*' in extract:
            return [title, extract]
        else:
            return None

    def findAGoodQuestion(self):
        ret = 0
        while True:
            ret = self.parseQuestion() #find a question were the extract contains *bleep* then it's considered a good question
            if ret != None:
                break
        return ret

    def quiz(self): #the question is a title and you need to match the correct extract
        question = self.findAGoodQuestion()
        options = set()
        options.add((question[1], True)) #add to set since it will hash and order them randomly so we dont need to randomly sort them
        dic = {'title': question[0], 'options': options, 'goodness': 0}
        for i in range(3):  #add 3 extracts from completely different articles, these are the wrong answers
            dic['options'].add(tuple([self.findAGoodQuestion()[1], False]))
        dic['options'] = list(dic['options']) 
        return dic
    
    def titleQuiz(self): #the question is an extract and you need to match the correct title
        question = self.findAGoodQuestion()
        options = set()
        options.add((question[0], True))
        dic = {'title': question[1], 'options': options, 'goodness': 0}
        for i in range(3):
            dic['options'].add(tuple([self.findAGoodQuestion()[0], False]))
        dic['options'] = list(dic['options']) 
        return dic
    
    def trueOrFalse(self): #A title and either the correct extract or a wrong extract 
        question = self.findAGoodQuestion()
        wrongQuestion = self.findAGoodQuestion()[1]
        options = set(((question[1], True), (wrongQuestion, False)))
        options.pop()
        options = options.pop()
        dic = {'title': question[0] + ": " + options[0], 'options': [('True', options[1]),('False', not options[1])], 'goodness': 0}
        return dic
