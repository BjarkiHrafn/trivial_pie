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
        return redirect(url_for('QuestionMenu'))
    elif 'menu' in request.form:
        return redirect(url_for('MainMenu'))


def getQuestions(numberOfQuestions):
    return controllerClass.DeployQuestion(numberOfQuestions)


@app.route('/survival')
# Post the questions here
def QuestionMenu():

    if len(controllerClass.listOFGoodQuestionsAlreadyAdded) == 0:
        questions = getQuestions(1)
    else:
        questions = controllerClass.listOFGoodQuestionsAlreadyAdded[0]
    if len(controllerClass.listOFGoodQuestionsAlreadyAdded) != 0:
        controllerClass.listOFGoodQuestionsAlreadyAdded.pop(0)
    controllerClass.currentGameMode = "survival"
    return render_template('SurvivalView.html', lives=controllerClass.survivalModeLives, score=controllerClass.currentScoreSurvival, item=questions)


@app.route('/survival', methods=['POST'])
def ProcessSurvivalQuestion():
    if 'submitAns'in request.form:
        outcome = eval(request.form.get("ans"))
        checkbox = request.form.get('questionCheck')
        if checkbox:
            controllerClass.goodQuestions.append(outcome[0])
        if not outcome[1]:
            controllerClass.survivalModeLives -= 1
            if controllerClass.survivalModeLives == 0:
                return redirect(url_for('EndGameGet'))
        else:
            if outcome[0] == 'True' or outcome[0] == 'False':
                controllerClass.currentScoreSurvival += 2
            else:
                controllerClass.currentScoreSurvival += 4
        controllerClass.survivalModeArray.append(outcome)
        return redirect(url_for('QuestionMenu'))


@app.route('/results')
def ResultMenu():
    return render_template('ResultView.html', result=controllerClass.answer, goodQuestion=controllerClass.goodQuestions)


@app.route('/quiz', methods=['GET'])
def QuizMenu():
    controllerClass.quizModeArray = getQuestions(
        controllerClass.numberOfQuestionsForQuiz)
    controllerClass.currentGameMode = "quiz"
    return render_template('QuizView.html', questions=controllerClass.quizModeArray)


@app.route('/quiz', methods=['POST'])
# Here you get what the player chose
def PostAnswer():
    try:
        # When you answer the controllerClass.answer gets the value
        # and you are redirected to another question or to the menu
        if 'submitAns' in request.form:

            for i in range(controllerClass.numberOfQuestionsForQuiz):
                question = request.form.get(str(i))
                if question:
                    answer = eval(question)[1]
                    if answer:
                        if answer[0] == 'True' or answer[0] == 'False':
                            controllerClass.currentScoreQuiz += 2
                        else:
                            controllerClass.currentScoreQuiz += 4
                            controllerClass.correctAnswerArray.append(
                                controllerClass.quizModeArray[i])

                checkbox = request.form.get('questionCheck' + str(i))
                if checkbox == '':
                    controllerClass.addToGoodQuestions(
                        controllerClass.quizModeArray[i])

            return redirect(url_for('EndGameGet'))
    except:
        return "Something went wrong.."


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
            controllerClass.survivalModeArray = []
            controllerClass.currentScoreSurvival = 0
        elif controllerClass.currentGameMode == "quiz":
            nickname = request.form.get('nicknamePick')
            score = controllerClass.currentScoreQuiz
            data = {"nickName": nickname, "score": score}
            if data["nickName"].lower() in badWords.bad:
                data["nickName"] = 'Vondurkall'
            controllerClass.addQuizHighScore(data)
            controllerClass.correctAnswerArray = []
            controllerClass.currentScoreQuiz = 0
    return redirect(url_for('getHighScores'))


@app.route('/highscore')
def getHighScores():
    return render_template('highscore.html', quiz=controllerClass.getQuizHighScores(), survival=controllerClass.getSurvivalHighScores())


if __name__ == '__main__':
    app.run()
