import requests
from flask import Flask, jsonify
import json

# the volunteers and their list of ordered job preferences
url = "https://o9ktamo0f2.execute-api.us-east-1.amazonaws.com/dev"


def create_app():
    app = Flask(__name__)

    with app.app_context():
        # print("Hello?")
        v_ = dict((m, prefs.split(', ')) for [m, prefs] in (
            line.rstrip().split(': ') for line in open('volunteers.txt')))
        j_ = dict((m, prefs.split(', ')) for [m, prefs] in (
            line.rstrip().split(': ') for line in open('jobs.txt')))
        newList = (v_, j_)
        # print(newList)
        # j = jsonify(newList)
        # print('Did I get here?')
        jd = json.dumps(newList)
        # print(json.dumps(newList))
        res = requests.post(
            url + '/app/data', json=jd)
        print('response from server:', res.text)
       # print(res.json())
    return app


create_app()
