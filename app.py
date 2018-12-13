from flask import Flask, render_template, request, url_for, redirect
from ControllerClass import Controller
from db import repository
import sys
import re
import badWords

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
    return controllerClass.DeployQuestion(numberOfQuestions)

@app.route('/quiz')

def QuizMenu():
    q = getQuestions(2)
    controllerClass.currentGameMode = "quiz"
    return render_template('QuizView.html', questions = q)


@app.route('/survival')
# Post the questions here
def QuestionMenu():
    q = getQuestions(1)
    controllerClass.currentGameMode = "survival"
    return render_template('QuestionView.html', msg= q, lives = controllerClass.survivalModeLives)

@app.route('/survival', methods=['POST'])

def ProcessSurvivalQuestion():
    if 'submitAns'in request.form:
        outcome = eval(request.form.get("ans"))
        checkbox = request.form.get('questionCheck')
        print(checkbox, file = sys.stderr)
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
                if eval(question[str(key+1)])[1]:
                    controllerClass.quizModeArray.append(question[str(key+1)])
        
            #controllerClass.answer = question 
            return redirect(url_for('EndGameGet'))
        elif 'menu' in request.form:
            return redirect(url_for('MainMenu'))

    except:
        return "Something went wrong.."

@app.route('/higscore')

def EndGameGet():
    return render_template('EndGameMenu.html')

@app.route('/higscore', methods = ['GET', 'POST'])

def EndGamePost():
    if 'submitScore' in request.form:
        nickname = request.form.get('nicknamePick')

        if controllerClass.currentGameMode == "survival":    
            print("nickname: ", nickname, file=sys.stderr)
            score = len(controllerClass.survivalModeArray)
            data = {"nickName": nickname, "score": score}
            if data["nickName"].lower() in badWords.bad:
                data["nickName"] = 'Vondurkall'
            database.addSurvivalHichScore(data)
            controllerClass.survivalModeArray = []
        elif controllerClass.currentGameMode == "quiz":
            score = len(controllerClass.quizModeArray)
            data = {"nickName": nickname, "score": score}
            database.addQuizHighScore(data)
            controllerClass.quizModeArray = []
    return redirect(url_for('MainMenu'))

@app.route('/highscore')
def getHighScores():
    return render_template('highscore.html', quiz = controllerClass.getQuizHighScores(), survival = controllerClass.getSurvivalHighScores())


if __name__ == '__main__':
    app.run()

