# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)


@app.route('/pyinfo')
def info():
    import pyinfo
    return pyinfo.info_as_html()
