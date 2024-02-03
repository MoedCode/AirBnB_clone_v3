#!/usr/bin/env python3
from flask import Flask,Blueprint, render_template, abort
from jinja2 import TemplateNotFound


APP = Flask(__name__)
APP.url_map.strict_slashes =False

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
if __name__ == "__main__":


    APP.run(host="0.0.0.0", port=5000)