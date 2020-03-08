from flask import render_template, request
from app import app
from app.text_preprocess import preprocess


@app.before_first_request
def _declareStuff():
    global text
    text = '''Alice's Adventures in Wonderland (commonly shortened to Alice in Wonderland) is an 1865 novel written ''' \
           '''by English author Charles Lutwidge Dodgson under the pseudonym Lewis Carroll.[1]'''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def form():
    text = request.form['text']
    return ' '.join(preprocess(text))
