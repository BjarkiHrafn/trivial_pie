from flask import Flask, render_template


app = Flask(__name__)
app.debug = True

@app.route('/')
def MainMenu():
    return render_template('MasterView.html')
if __name__ == '__main__':
    app.run()