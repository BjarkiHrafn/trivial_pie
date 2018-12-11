import re
import json
import getWiki


class QuestionMaker:


    def parseQuestion(self):
        
        r = getWiki.getRandomWikiQuestion()
        dir1 = json.loads(r.text)
        dir2 =  dir1['query']['pages']
        title = dir2[list(dir2.keys())[0]]['title']
        extract = dir2[list(dir2.keys())[0]]['extract']
        try:
            extract = re.search('.*?\.(?= )', extract).group()
            extract = re.compile(title.lower() + '(?= )').sub('*Bleep*', extract.lower())
            extract = re.compile(title.lower() + '(?=\w)').sub('*Bleep*-', extract.lower())
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
            ret = self.parseQuestion()
            if ret != None:
                break
        return ret

    def quiz(self):
        question = self.findAGoodQuestion()
        options = set()
        options.add((question[1], True))
        dic = {'title': question[0], 'options': options, 'goodness':0}
        for i in range(3):
            dic['options'].add(tuple([self.findAGoodQuestion()[1], False])) 
        return dic
