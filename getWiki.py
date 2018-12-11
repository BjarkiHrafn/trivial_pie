import requests


def getRandomWikiQuestion():
    r = requests.get('https://en.wikipedia.org/wiki/special:random')
    site = r.url.split('wiki/')[1]
    try:
        r = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles='+ site + '&fbclid=IwAR315Sqa4ZskYIewv8NOe6GRWB-TGwN1zLHTfcSqBH2WHf6MaJn3SLXEOEU')
    except:
        print('wiki entry not found')
    return r