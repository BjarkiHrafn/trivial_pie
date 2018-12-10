from flask import Flask, render_template, request, url_for, redirect
from ControllerClass import Controller


app = Flask(__name__)
controllerClass = Controller()

app.debug = True

@app.route('/')
def MasterMenu():
    return render_template('MasterView.html', msg= "some messaage")

@app.route('/menu')
#questions, create question etc...
def MainMenu():
    return render_template('MenuView.html')

@app.route('/questions')
#Post the questions here
def QuestionMenu():
    return render_template('QuestionView.html', msg= controllerClass.DeployQuestion())

@app.route('/question', methods = ['GET','POST'])
#Here you get what the player chose
def PostAnswer():
    try:
        #When you answer the controllerClass.answer gets the value
        #and you are redirected to another question or to the menu
        if 'ans' in request.form:
            ans = request.form.get("ans")
            controllerClass.answer = ans
            return redirect(url_for('QuestionMenu'))
        elif 'menu' in request.form:
            return redirect(url_for('MainMenu'))
    except:
        return "Something went wrong.."


if __name__ == '__main__':
    app.run()