#!/usr/bin/env python3
from flask import Flask
from markupsafe import escape

APP = Flask(__name__)
APP.url_map.strict_slashes =False
# Example 1: Basic Usage
original_string = '<script>window.open(`https://procode24.tech`)</script>'
escaped_string = escape(original_string)
@APP.route("/")
def home_page():
    "doc str"
    return escaped_string
@APP.route("/org")
def org_page():
    "doc str"
    return original_string
if __name__ == "__main__":

    print(f'Original String: {original_string}')
    print(f'Escaped String: {escaped_string}')
    APP.run(host="0.0.0.0", port=5000)