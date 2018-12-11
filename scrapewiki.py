import requests
import re
import json

def getRandomWikiQuestion():
    r = requests.get('https://en.wikipedia.org/wiki/special:random')
    site = r.url.split('wiki/')[1]
    try:
        r = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles='+ site + '&fbclid=IwAR315Sqa4ZskYIewv8NOe6GRWB-TGwN1zLHTfcSqBH2WHf6MaJn3SLXEOEU')
    except:
        print('wiki entry not found')
    else:
        dir1 = json.loads(r.text)
        dir2 =  dir1['query']['pages']
        title = dir2[list(dir2.keys())[0]]['title']
        extract = dir2[list(dir2.keys())[0]]['extract']
        try:
            extract = re.search('.*?\.(?= )', extract).group()
            extract = re.compile(title.lower() + '(?= )').sub('*Bleep*', extract.lower())
            extract = re.compile(title.lower() + '(?=\w)').sub('*Bleep*-', extract.lower())
            extract.decode('ascii')
            print(extract)
        except UnicodeDecodeError:
            print("it was not a ascii-encoded unicode string")
            return None
        except:
            pass
        if '*bleep*' in extract:
            return [title, extract]
        else:
            return None

def findAGoodQuestion():
    ret = 0
    while True:
        ret = getRandomWikiQuestion()
        if ret != None:
            break
    return ret

def quiz():
    question = findAGoodQuestion()
    lis = [question[0], set([tuple([question[1], True])])]
    for i in range(3):
        lis[1].add(tuple([findAGoodQuestion()[1], False])) 
    return lis