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
    #redirects to different routes depending on what button was pressed on the header
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
    #resets the controller for a new survival game
    controllerClass.__init__()
    return redirect(url_for('survival'))


@app.route('/survival')
# Post the questions here
def survival():
    #when the good questions are finished in survival ten random questions will be scraped
    if len(controllerClass.listOFGoodQuestionsAlreadyAdded) == 0:
        controllerClass.listOFGoodQuestionsAlreadyAdded = getQuestions(10)
    questions = controllerClass.listOFGoodQuestionsAlreadyAdded[0]
    controllerClass.currentGameMode = "survival"
    return render_template('survivalView.html', lives=controllerClass.survivalModeLives, score=controllerClass.currentScoreSurvival, item=questions)


@app.route('/survival', methods=['POST'])
def processSurvivalQuestion():
    #to prevent abuse using postman or such
    if 'submitChoice' in request.form:
        #this removes the question that the player last had
        if len(controllerClass.listOFGoodQuestionsAlreadyAdded) != 0:
            controllerClass.listOFGoodQuestionsAlreadyAdded.pop(0)
        wholeForm = request.form
        addToGood = wholeForm.get('questionCheck')
        #adds the question to good questions or increments it if it was already a good question
        if addToGood:
            controllerClass.addToGoodQuestions(eval(addToGood))
        answer = wholeForm.get('choice')
        #answer is either true or false if its true the player chose the right answer
        if answer and eval(answer):
            score = wholeForm.get('points')
            controllerClass.currentScoreSurvival += int(score)
        #if the player chose wrong he loses a heart
        else:
            controllerClass.survivalModeLives -= 1
        #when all lives are depleted its game over man!
        if controllerClass.survivalModeLives < 1:
            return redirect(url_for('endGameGet'))
        return redirect(url_for('survival'))


@app.route('/results')
def resultMenu():
    return render_template('resultView.html', result=controllerClass.answer, goodQuestion=controllerClass.goodQuestions)


@app.route('/quiz', methods=['GET'])
def quizMenu():
    #reset controllerclass since a new game is started
    controllerClass.__init__()
    #gets questions equal to the amount of question initialized in the controller class
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
        wholeForm = request.form
        totalScore = wholeForm.get('totalScore')
        # minus two because of submitAns and totalscore
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
        
        points = str(controllerClass.currentScoreQuiz) + '/' + totalScore
        grade = f'{eval(points) * 10:.2f}'
        controllerClass.currentScoreQuiz = [points, eval(grade)]

    return redirect(url_for('endGameGet'))

@app.route('/endgame')
def endGameGet():
    points = 0
    # currentscorequiz is a list it means the endgame was achieved via a quiz
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
        #set the appropraite score to the appropriate table in the database
        #if a quiz game was played the score cant be a 0, its always a list
        if controllerClass.currentScoreQuiz == 0:
            score = controllerClass.currentScoreSurvival
        else:
            score = controllerClass.currentScoreQuiz
        data = {"nickName": nickname, "score": score}
        #lousy profanity filter, finds if the nickname submitted is any of them but does not check bad names plus other chars
        if data["nickName"].lower() in badWords.bad:
            data["nickName"] = 'Vondurkall'
        if controllerClass.currentGameMode == "survival":
            controllerClass.addSurvivalHichScore(data)
        elif controllerClass.currentGameMode == "quiz":
            controllerClass.addQuizHighScore(data)
        #reset the controllerclass since either game is over
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
