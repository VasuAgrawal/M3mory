#!/usr/bin/env python

from flask import Flask
from flask.ext.mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
