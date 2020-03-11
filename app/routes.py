import os, shutil
import time

from flask import render_template, request, Response, make_response
from pytrie import SortedStringTrie as Trie

from fpdf import FPDF

from app import app
from app.text_preprocess import preprocess
from app.normalization import normalize
from app.tokenization import tokenize
from app.get_docs import get_docs, get_docs_length
from app.data_loader import load_data
from app.index_loader import load_index
from app.search_index import search_disk
from app.search_aux import search_ram


@app.before_first_request
def _declareStuff():
    try:
        shutil.rmtree('./app/collection')
    except:
        print('Creating collection folder')
    os.mkdir('./app/collection')

    try:
        shutil.rmtree('./app/index')
    except:
        print('Creating index folder')
    os.mkdir('./app/index')

    global aux
    aux = {}

    global sndx
    sndx = {}

    global prfx
    prfx = Trie()

    global psfx
    psfx = Trie()

    global docs
    docs = get_docs("./app/docs/reuters21578.tar.gz")

    global length
    length = get_docs_length("./app/docs/reuters21578.tar.gz")

    global docs_names
    docs_names = names_generator(length)


def ram_loader(content, name):
    prep_text = preprocess(content)
    norm_text = tokenize(normalize(content))

    global aux
    global sndx
    global prfx
    global psfx

    aux, sndx, prfx, psfx = load_data(content, name, aux, sndx, prfx, psfx)


def write2disk(name, content):
    with open(f'./app/collection/{name}.txt', 'w') as filehandle:
        filehandle.write(content)
    ram_loader(content, name)


def crawler_generator():
    for i in range(length):
        file_name = next(docs_names)
        write2disk(file_name, next(docs))
        if i % 10 == 0:
            load_index(aux, './app/index')

        yield file_name
        time.sleep(2)  # an artificial delay


def names_generator(docs):
    for i in range(length):
        yield f'Collection {i}'


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)

    # uncomment if you don't need immediate reaction
    ##rv.enable_buffering(5)
    return rv


@app.route('/home', methods=['GET'])
def stream_get():
    return Response(stream_template('stream.html', data=crawler_generator()))


@app.route('/home', methods=['POST'])
def stream_post():
    query = request.form['text']
    message, search_result, track = search_disk(query, prfx, psfx, sndx, './app/index')
    search_result = [f'<a href="show_doc_{res}">{res}</a>' for res in search_result]
    return Response(stream_template('stream.html', data=crawler_generator(),
                                    message=message.split('\n')[:-1], search_result=search_result, track=f'<h4>Query track: {track} </h4> <hr>'))


@app.route('/show_doc_<number>')
def show_doc(number):
    with open(f'./app/collection/Collection {number}.txt', 'rb') as filehandle:
        doc = filehandle.read()

    return Response(doc, mimetype='text/plain')


@app.route('/')
def index():
    return render_template('info.html')
