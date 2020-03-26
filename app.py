from collections import namedtuple
from random import choice

from flask import Flask, jsonify, request
import json

from match_setup import setup

Quote = namedtuple("Quote", ("text", "author"))

quotes = [
    Quote("Talk is cheap. Show me the code.", "Linus Torvalds"),
    Quote("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    Quote("Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live",
          "John Woods"),
    Quote("Give a man a program, frustrate him for a day. Teach a man to program, frustrate him for a lifetime.", "Muhammad Waseem"),
    Quote("Progress is possible only if we train ourselves to think about programs without thinking of them as pieces of executable code. ",
          "Edsger W. Dijkstra")
]

app = Flask(__name__)


@app.route("/app/data", methods=["POST"])
def get_volunteers():
    jdata = request.json
    # print('jdata', json.loads(jdata)[0])
    js0 = json.loads(jdata)
    v_ = {}
    j_ = {}
    # print('jdata', json.JSONDecoder.decode(s=jdata))
    for j in js0[0]:
        # print('j', j, js0[0][j])

        # for x, y in enumerate(j):
        #     print(x, y)

        name, prefs = j, js0[0][j]
        # print('type prefs', type(prefs))
        v_[name] = prefs
    for j in js0[1]:
        name, prefs = j, js0[1][j]
        # print('type prefs', type(prefs))
        j_[name] = prefs

    # for j in jdata[1]:
    #     name, prefs = j.split(': ')
    #     j_[name] = prefs.split(', ')
    return setup(v_, j_)
    # return jsonify(v_)


# @app.route("/app/jobs", methods=["POST"])
# def get_jobs():
#     jdata = request.get_json()
#     for j in jdata['Newlist'][1]:
#         j_[j['job']] = j['names'].split(', ')
#     return setup(v_, j_)


@app.route("/quote", methods=["GET"])
def get_random_quote():
    return jsonify(choice(quotes)._asdict())
