from flask import Flask, render_template, request, url_for, redirect
from ControllerClass import Controller


app = Flask(__name__)
controllerClass = Controller()

quizmode = []

app.debug = True


@app.route('/')
def MasterMenu():
    return render_template('MasterView.html', msg="some messaage")


@app.route('/menu')
# questions, create question etc...
def MainMenu():
    return render_template('MenuView.html')

def getQuestions(numberOfQuestions):
    for i in range(numberOfQuestions):
        quizmode.append(controllerClass.DeployQuestion())
    return quizmode

@app.route('/quiz')

def QuizMenu():
    q = getQuestions(5)
    return render_template('QuizView.html', questions = q)


@app.route('/survival')
# Post the questions here
def QuestionMenu():
    q = getQuestions(1)
    return render_template('QuestionView.html', msg= q)

@app.route('/results')

def ResultMenu():
    return render_template('ResultView.html', result = controllerClass.answer, goodQuestion = controllerClass.goodQuestions)


@app.route('/question', methods=['GET', 'POST'])
# Here you get what the player chose
def PostAnswer():
    try:
        # When you answer the controllerClass.answer gets the value
        # and you are redirected to another question or to the menu
        if 'submitAns' in request.form:
            ans = request.form.get("ans")
            question = request.form.get("submitAns")
            #if request.form.get('goodQuestion'):
                #controllerClass.goodQuestions.append(currentQuestion)
            controllerClass.answer = ans
            
            return redirect(url_for('ResultMenu'))
        elif 'menu' in request.form:
            return redirect(url_for('MainMenu'))

    except:
        return "Something went wrong.."


if __name__ == '__main__':
    app.run()
