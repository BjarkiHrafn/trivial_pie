from flask import Flask, render_template, request, url_for, redirect
from ControllerClass import Controller
from db import repository
import sys
import re

app = Flask(__name__)
controllerClass = Controller()
database = repository()




app.debug = True


@app.route('/')
def MasterMenu():
    return render_template('MasterView.html', msg="some messaage")


@app.route('/menu')
# questions, create question etc...
def MainMenu():
    return render_template('MenuView.html')

@app.route('/menu', methods = ['GET', 'POST'])

def MenuRedirect():
    
    if 'quiz' in request.form:
        return redirect(url_for('QuizMenu'))
    elif 'survival' in request.form:
        return redirect(url_for('QuestionMenu'))


def getQuestions(numberOfQuestions):
    quizmode = []
    for i in range(numberOfQuestions):
        quizmode.append(controllerClass.DeployQuestion())
    return quizmode

@app.route('/quiz')

def QuizMenu():
    q = getQuestions(2)
    return render_template('QuizView.html', questions = q)


@app.route('/survival')
# Post the questions here
def QuestionMenu():
    q = getQuestions(1)
    return render_template('QuestionView.html', msg= q, lives = controllerClass.survivalModeLives)

@app.route('/survival', methods=['POST'])

def ProcessSurvivalQuestion():
    if 'submitAns'in request.form:
        outcome = eval(request.form.get("ans"))
        if not outcome[1]:
            controllerClass.survivalModeLives -=  1
            print("outcome: ", outcome, "...You're wrong sukkah!", file=sys.stderr)
            if controllerClass.survivalModeLives == 0:
                return redirect(url_for('EndGameGet'))
        controllerClass.survivalModeArray.append(outcome)
        return redirect(url_for('QuestionMenu'))
    elif 'menu' in request.form:
            return redirect(url_for('MainMenu'))
        

@app.route('/results')

def ResultMenu():
    return render_template('ResultView.html', result = controllerClass.answer, goodQuestion = controllerClass.goodQuestions)


@app.route('/questions', methods=['GET', 'POST'])
# Here you get what the player chose
def PostAnswer():
    try:
        # When you answer the controllerClass.answer gets the value
        # and you are redirected to another question or to the menu
        if 'submitAns' in request.form:
            #ans = request.form.get("ans")
            question = request.form
            question = dict(question)
            question.pop('submitAns')
            for key in range(len(question)):
                print("x: ", eval(question[str(key+1)])[1], file=sys.stderr)
            controllerClass.answer = question 
            
            return redirect(url_for('ResultMenu'))
        elif 'menu' in request.form:
            return redirect(url_for('MainMenu'))

    except:
        return "Something went wrong.."

@app.route('/highscore')

def EndGameGet():
    return render_template('EndGameMenu.html')

@app.route('/highscore', methods = ['GET', 'POST'])

def EndGamePost():
    if 'submitScore' in request.form:
        nickname = request.form.get('nicknamePick')
        
        print("nickname: ", nickname, file=sys.stderr)
        score = len(controllerClass.survivalModeArray)
        data = {"nickName": nickname, "score": score}
        database.addSurvivalHichScore(data)
        controllerClass.survivalModeArray = []
    return redirect(url_for('MainMenu'))

if __name__ == '__main__':
    app.run()
