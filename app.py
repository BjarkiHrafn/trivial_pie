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
    return controllerClass.DeployQuestion(numberOfQuestions)

@app.route('/quiz')

def QuizMenu():
    controllerClass.quizModeArray = getQuestions(controllerClass.numberOfQuestionsForQuiz)
    controllerClass.currentGameMode = "quiz"
    return render_template('QuizView.html', questions = controllerClass.quizModeArray)


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

        if checkbox:
            controllerClass.goodQuestions.append(outcome[0])
        
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
            
            questionArr = []
            #everything = request.form
            score = 0
            #print("all: ", everything,  file = sys.stderr)
            
           
                 
                question = request.form.get(str(i))
                if question:
                    answer = eval(question)[1]
                    if answer:
                        controllerClass.correctAnswerArray.append(controllerClass.quizModeArray[i])
                
                
                checkbox = request.form.get('questionCheck'+ str(i))
                
                if checkbox == '':
                    print("checkbox was clicked",  file = sys.stderr)
                    print("checkbox: ", controllerClass.quizModeArray[i],  file = sys.stderr)
                    database.addToGoodQuestions(controllerClass.quizModeArray[i])
                
            
            #print('score:'+ score, file = sys.stderr)
            
            
            
            
            '''
            try:
                question = request.form
                question = dict(question)
                question.pop('submitAns')
            except KeyError:
                pass

            print("all: ", question,  file = sys.stderr)
            #if checkbox:
            #    print("checkbox selected, question: ", question , file=sys.stderr)
            
            for key in range(len(question)):
                if eval(question[str(key+1)])[1]:
                    #controllerClass.quizModeArray.append(question[str(key+1)])

                    print("question: " + str(key+1), eval(question[str(key+1)]),  file = sys.stderr)
                    #print("buttonChecked: ", question['questionCheck'+str(key+1)],  file = sys.stderr)

            '''
            #controllerClass.answer = question 
            
            return redirect(url_for('EndGameGet'))
        elif 'menu' in request.form:
            return redirect(url_for('MainMenu'))

    except:
        return "Something went wrong.."

@app.route('/endgame')
def EndGameGet():
    return render_template('EndGameMenu.html')

@app.route('/endgame', methods = ['GET', 'POST'])

def EndGamePost():
    if 'submitScore' in request.form:
        nickname = request.form.get('nicknamePick')

        if controllerClass.currentGameMode == "survival":    
            print("nickname: ", nickname, file=sys.stderr)
            score = len(controllerClass.survivalModeArray)
            data = {"nickName": nickname, "score": score}
            database.addSurvivalHichScore(data)
            controllerClass.survivalModeArray = []
        elif controllerClass.currentGameMode == "quiz":
            score = len(controllerClass.correctAnswerArray)
            data = {"nickName": nickname, "score": score}
            database.addQuizHighScore(data)
            controllerClass.correctAnswerArray = []
    return redirect(url_for('MainMenu'))

@app.route('/highscore')
def getHighScores():
    return render_template('highscore.html', quiz = controllerClass.getQuizHighScores(), survival = controllerClass.getSurvivalHighScores())


if __name__ == '__main__':
    app.run()

