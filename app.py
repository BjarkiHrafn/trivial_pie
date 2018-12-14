from flask import Flask, render_template, request, url_for, redirect
from ControllerClass import Controller
import sys  # prints to console
import badWords

app = Flask(__name__)
app.debug = True
controllerClass = Controller()


@app.route('/', methods=['GET'])
def masterMenu():
    # return render_template('MasterView.html', msg="some messaage")
    return render_template('menuView.html')


@app.route('/menu', methods=['GET'])
# questions, create question etc...
def mainMenu():
    return render_template('menuView.html')


@app.route('/menu', methods=['POST'])
def menuRedirect():
    if 'quiz' in request.form:
        return redirect(url_for('quizMenu'))
    elif 'survival' in request.form:
        return redirect(url_for('redirectToSurvival'))
    elif 'menu' in request.form:
        return redirect(url_for('mainMenu'))
    elif 'highScore' in request.form:
        return redirect(url_for('getHighScores'))
    else:
        return redirect(url_for('page_not_found'))



def getQuestions(numberOfQuestions):
    return controllerClass.deployQuestion(numberOfQuestions)


@app.route('/newgame')
def redirectToSurvival():
    controllerClass.__init__()
    return redirect(url_for('survival'))


@app.route('/survival')
# Post the questions here
def survival():

    if len(controllerClass.listOFGoodQuestionsAlreadyAdded) == 0:
        controllerClass.listOFGoodQuestionsAlreadyAdded = getQuestions(10)
    questions = controllerClass.listOFGoodQuestionsAlreadyAdded[0]

    controllerClass.currentGameMode = "survival"
    return render_template('survivalView.html', lives=controllerClass.survivalModeLives, score=controllerClass.currentScoreSurvival, item=questions)


@app.route('/survival', methods=['POST'])
def processSurvivalQuestion():
    if 'submitChoice' in request.form:
        if len(controllerClass.listOFGoodQuestionsAlreadyAdded) != 0:
            controllerClass.listOFGoodQuestionsAlreadyAdded.pop(0)
        wholeForm = request.form
        addToGood = wholeForm.get('questionCheck')
        if addToGood:
            controllerClass.addToGoodQuestions(eval(addToGood))
        answer = wholeForm.get('choice')
        print(answer, file=sys.stderr)
        if answer and eval(answer):
            score = wholeForm.get('points')
            controllerClass.currentScoreSurvival += int(score)
        else:
            controllerClass.survivalModeLives -= 1
        if controllerClass.survivalModeLives < 1:
            return redirect(url_for('endGameGet'))
        return redirect(url_for('survival'))


@app.route('/results')
def resultMenu():
    return render_template('resultView.html', result=controllerClass.answer, goodQuestion=controllerClass.goodQuestions)


@app.route('/quiz', methods=['GET'])
def quizMenu():
    controllerClass.quizModeArray = getQuestions(controllerClass.numberOfQuestionsForQuiz)
    totalScore = 0
    for x in controllerClass.quizModeArray:
        totalScore += len(x['options'])
    controllerClass.currentGameMode = "quiz"
    return render_template('quizView.html', questions=controllerClass.quizModeArray, totalscore=totalScore)


@app.route('/quiz', methods=['POST'])
# Here you get what the player chose
def postAnswer():
    # When you answer the controllerClass.answer gets the value
    # and you are redirected to another question or to the menu
    if 'submitAns' in request.form:
        controllerClass.currentScoreQuiz = 0
        wholeForm = request.form
        totalScore = wholeForm.get('totalScore')
        # minus two because of submitans and totalscore
        for i in range(len(wholeForm) - 2):
        #if a key error occurs the goodness or answer was not checked so we just ignore it
            try:
                #this is whether the goodness was checked

                controllerClass.addToGoodQuestions(eval(wholeForm[str(i)]))
            except KeyError:
                pass
            try:
                #this is the answer the user chose
                answer = eval(wholeForm['question' + str(i)])
                if answer[0]:
                    print(type(answer[1]), file=sys.stderr)
                    print(type(controllerClass.currentScoreQuiz), file=sys.stderr)
                    controllerClass.currentScoreQuiz += answer[1]
            except KeyError:
                continue
        
        points = str(controllerClass.currentScoreQuiz) + '/' + totalScore
        grade = f'{eval(points) * 10:.2f}'
        controllerClass.currentScoreQuiz = [points, eval(grade)]

    return redirect(url_for('endGameGet'))

@app.route('/endgame')
def endGameGet():
    points = 0

    if type(controllerClass.currentScoreQuiz) is list:
        points = controllerClass.currentScoreQuiz[0]
        points += '  Your grade is: ' + str(controllerClass.currentScoreQuiz[1])
    elif controllerClass.currentScoreSurvival != 0:
        points = controllerClass.currentScoreSurvival


    return render_template('endGameMenu.html', score=points)


@app.route('/endgame', methods=['GET', 'POST'])
def endGamePost():
    if 'submitScore' in request.form :
        #no need for nicknames longer than 20
        nickname = request.form.get('nicknamePick')[:20] 
        if controllerClass.currentScoreQuiz == 0:
            score = controllerClass.currentScoreSurvival
        else:
            score = controllerClass.currentScoreQuiz
        print(score, file=sys.stderr)
        data = {"nickName": nickname, "score": score}
        if data["nickName"].lower() in badWords.bad:
            data["nickName"] = 'Vondurkall'
        if controllerClass.currentGameMode == "survival":
            controllerClass.addSurvivalHichScore(data)
        elif controllerClass.currentGameMode == "quiz":
            controllerClass.addQuizHighScore(data)
        controllerClass.__init__()
    return redirect(url_for('getHighScores'))


@app.route('/highscore', methods=['GET'])
def getHighScores():
    return render_template('highscore.html', quiz=controllerClass.getQuizHighScores(), survival=controllerClass.getSurvivalHighScores())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('menuView.html'), 404


if __name__ == '__main__':
    app.run()
