from flask import Flask, render_template, request, url_for, redirect
from ControllerClass import Controller
import sys  # prints to console
import badWords

app = Flask(__name__)
app.debug = True
controllerClass = Controller()


@app.route('/', methods=['GET'])
def MasterMenu():
    # return render_template('MasterView.html', msg="some messaage")
    return render_template('MenuView.html')


@app.route('/menu', methods=['GET'])
# questions, create question etc...
def MainMenu():
    return render_template('MenuView.html')


@app.route('/menu', methods=['POST'])
def MenuRedirect():
    if 'quiz' in request.form:
        return redirect(url_for('QuizMenu'))
    elif 'survival' in request.form:
        return redirect(url_for('RedirectToSurvival'))
    elif 'menu' in request.form:
        return redirect(url_for('MainMenu'))
    elif 'highScore' in request.form:
        return redirect(url_for('getHighScores'))
    else:
        return redirect(url_for('page_not_found'))



def getQuestions(numberOfQuestions):
    return controllerClass.DeployQuestion(numberOfQuestions)


@app.route('/newgame')
def RedirectToSurvival():
    controllerClass.__init__()
    return redirect(url_for('survival'))


@app.route('/survival')
# Post the questions here
def survival():

    if len(controllerClass.listOFGoodQuestionsAlreadyAdded) == 0:
        controllerClass.listOFGoodQuestionsAlreadyAdded = getQuestions(10)
    questions = controllerClass.listOFGoodQuestionsAlreadyAdded[0]

    controllerClass.currentGameMode = "survival"
    return render_template('SurvivalView.html', lives=controllerClass.survivalModeLives, score=controllerClass.currentScoreSurvival, item=questions)


@app.route('/survival', methods=['POST'])
def ProcessSurvivalQuestion():
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
            return redirect(url_for('EndGameGet'))
        return redirect(url_for('survival'))


@app.route('/results')
def ResultMenu():
    return render_template('ResultView.html', result=controllerClass.answer, goodQuestion=controllerClass.goodQuestions)


@app.route('/quiz', methods=['GET'])
def QuizMenu():
    #controllerClass.quizModeArray = controllerClass.listOFGoodQuestionsAlreadyAdded[:3]
    controllerClass.quizModeArray = getQuestions(controllerClass.numberOfQuestionsForQuiz)
    totalScore = 0
    for x in controllerClass.quizModeArray:
        totalScore += len(x['options'])
    controllerClass.currentGameMode = "quiz"
    return render_template('QuizView.html', questions=controllerClass.quizModeArray, totalscore=totalScore)


@app.route('/quiz', methods=['POST'])
# Here you get what the player chose
def PostAnswer():
    # When you answer the controllerClass.answer gets the value
    # and you are redirected to another question or to the menu
    if 'submitAns' in request.form:
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
                    controllerClass.currentScoreQuiz += answer[1]
            except KeyError:
                pass
            points = str(controllerClass.currentScoreQuiz) + '/' + str(totalScore)
            grade = f'{eval(points) * 10:.2f}'
        controllerClass.currentScoreQuiz = [points, eval(grade)]
    return redirect(url_for('EndGameGet'))

@app.route('/endgame')
def EndGameGet():
    points = 0
    if controllerClass.currentScoreQuiz:
        points = controllerClass.currentScoreQuiz[0]
        points += '  Your grade is: ' + str(controllerClass.currentScoreQuiz[1])
        
    if controllerClass.currentScoreSurvival:
        points = controllerClass.currentScoreSurvival

    return render_template('EndGameMenu.html', score=points)


@app.route('/endgame', methods=['GET', 'POST'])
def EndGamePost():
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
    return render_template('MenuView.html'), 404


if __name__ == '__main__':
    app.run()
