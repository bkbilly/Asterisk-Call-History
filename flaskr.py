#!/usr/bin/env python

import json
import os
import sys

from flask import Flask, send_from_directory, request

from datetime import datetime
from asteriskcallhistory import AsteriskCallHistory


if len(sys.argv) > 1:
    if ".pid" in sys.argv[1]:
        with open(sys.argv[1], "w") as f:
            f.write(str(os.getpid()))


app = Flask(__name__, static_url_path='')
wd = os.path.dirname(os.path.realpath(__file__))
webDirectory = os.path.join(wd, 'web')
configfile = os.path.join(wd, "configuration.json")
callhistory = AsteriskCallHistory(configfile)


@app.route('/')
def index():
    return send_from_directory(webDirectory, 'index.html')


@app.route('/main.css')
def main():
    return send_from_directory(webDirectory, 'main.css')


@app.route('/icon.png')
def icon():
    return send_from_directory(webDirectory, 'icon.png')


@app.route('/mycss.css')
def mycss():
    return send_from_directory(webDirectory, 'mycss.css')


@app.route('/mycssMobile.css')
def mycssMobile():
    return send_from_directory(webDirectory, 'mycssMobile.css')


@app.route('/myjs.js')
def myjs():
    return send_from_directory(webDirectory, 'myjs.js')


@app.route('/getCallHistory.json')
def getCallHistory():
    limit = request.args.get('limit')
    print "------------> ", limit
    return json.dumps(callhistory.getCallHistory(int(limit)))


if __name__ == '__main__':
    app.run(host='', port=5002)
