import time

from flask import render_template, request, Response, stream_with_context
from app import app
from app.text_preprocess import preprocess


@app.before_first_request
def _declareStuff():
    global text
    text = '''Alice's Adventures in Wonderland (commonly shortened to Alice in Wonderland) is an 1865 novel written ''' \
           '''by English author Charles Lutwidge Dodgson under the pseudonym Lewis Carroll.[1]'''


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)

    # uncomment if you don't need immediate reaction
    ##rv.enable_buffering(5)
    return rv


def crawler_generator():
    for i, c in enumerate("hello" * 10):
        time.sleep(1)  # an artificial delay
        yield i, c


@app.route('/stream', methods=['GET', 'POST'])
def stream():
    text = request.form['text']
    result = ' '.join(preprocess(text))
    return Response(stream_template('stream.html', data=crawler_generator(), result=result))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def form():
    text = request.form['text']
    result = ' '.join(preprocess(text))
    return render_template('index.html', result=result)
