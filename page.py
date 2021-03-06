#!/usr/bin/env python3

import config
import flask
import poem_gen

VERBOSE = False

app = flask.Flask(__name__)

models = poem_gen.parse_poems(VERBOSE)
poets = sorted(models.keys())

@app.route('/', methods=['GET'])
def index():
    poet = flask.request.args.get('poet', None)
    if poet and poet in models:
        poem = poem_gen.generate_poem(models[poet])
        if VERBOSE:
            print(poem)
    else:
        poem = None
    return flask.render_template('index.html',
                                 authors=poets,
                                 poet=poet,
                                 poem=poem)

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
