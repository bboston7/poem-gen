#!/usr/bin/env python3

import config
import flask
import poem_gen

app = flask.Flask(__name__)

models = poem_gen.parse_poems()
poets = sorted(models.keys())

@app.route('/', methods=['GET'])
def index():
    poet = flask.request.args.get('poet', None)
    if poet and poet in models:
        poem = poem_gen.generate_poem(models[poet])
        print(poem)
    else:
        poem = None
    return flask.render_template('index.html',
                                 authors=poets,
                                 poet=poet,
                                 poem=poem)

app.run(host=config.HOST, port=config.PORT)
