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
        questions = getQuestions(1)
    else:
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
    controllerClass.quizModeArray = controllerClass.listOFGoodQuestionsAlreadyAdded[:3]
    #controllerClass.quizModeArray = getQuestions(controllerClass.numberOfQuestionsForQuiz)
    controllerClass.currentGameMode = "quiz"
    return render_template('QuizView.html', questions=controllerClass.quizModeArray)


@app.route('/quiz', methods=['POST'])
# Here you get what the player chose
def PostAnswer():
    # When you answer the controllerClass.answer gets the value
    # and you are redirected to another question or to the menu
    if 'submitAns' in request.form:
        wholeForm = request.form
        print(wholeForm, file=sys.stderr)
        print(type(wholeForm), file=sys.stderr)
        print(len(wholeForm), file=sys.stderr)

        # for i in range(controllerClass.numberOfQuestionsForQuiz):
        #     question = request.form.get(str(i))
        #     print(question, file=sys.stderr)
        #     if question:
        #         answer = eval(question)[1]
        #         if answer:
        #             if outcome[0] == 'True' or outcome[0] == 'False':
        #                 controllerClass.currentScoreQuiz += 2  
        #             else:
        #                 controllerClass.currentScoreQuiz += 4
        #                 controllerClass.correctAnswerArray.append(
        #                 controllerClass.quizModeArray[i])

        #     checkbox = request.form.get('questionCheck' + str(i))
        #     if checkbox == '':
        #         controllerClass.addToGoodQuestions(
        #             controllerClass.quizModeArray[i])

        return redirect(url_for('EndGameGet'))

@app.route('/endgame')
def EndGameGet():
    return render_template('EndGameMenu.html')


@app.route('/endgame', methods=['GET', 'POST'])
def EndGamePost():
    if 'submitScore' in request.form:
        if controllerClass.currentGameMode == "survival":
            nickname = request.form.get('nicknamePick')
            score = controllerClass.currentScoreSurvival
            data = {"nickName": nickname, "score": score}
            if data["nickName"].lower() in badWords.bad:
                data["nickName"] = 'Vondurkall'
            controllerClass.addSurvivalHichScore(data)
        elif controllerClass.currentGameMode == "quiz":
            nickname = request.form.get('nicknamePick')
            score = controllerClass.currentScoreQuiz
            data = {"nickName": nickname, "score": score}
            if data["nickName"].lower() in badWords.bad:
                data["nickName"] = 'Vondurkall'
            controllerClass.addQuizHighScore(data)
        controllerClass.__init__()
    return redirect(url_for('getHighScores'))


@app.route('/highscore')
def getHighScores():
    return render_template('highscore.html', quiz=controllerClass.getQuizHighScores(), survival=controllerClass.getSurvivalHighScores())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('MenuView.html'), 404


if __name__ == '__main__':
    app.run()
