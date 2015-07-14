#!/usr/bin/env python3

import flask
import poem_gen

app = flask.Flask(__name__)

models = poem_gen.parse_poems()

def nl_to_br(string):
    return "<br />".join(string.split("\n"))

@app.route('/', methods=['GET'])
def index():
    poet = flask.request.args.get('poet', None)
    if poet and poet in models:
        poem = poem_gen.generate_poem(models[poet])
        print(poem)
    else:
        poem = None
    return flask.render_template('index.html',
                                 authors=models.keys(),
                                 poet=poet,
                                 poem=poem)

app.run(debug=True)
