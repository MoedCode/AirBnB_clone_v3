#!/usr/bin/env python3

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://procode:moed22@localhost/test_flaskr'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(APP)

# Define your model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    text = db.Column(db.Text)

# Database Initialization
def init_db():
    db.create_all()

# Teardown Request: Close Database Connection
@APP.teardown_appcontext
def close_db(error):
    db.session.remove()

# Route to fetch entries as JSON
@APP.route('/api/entries', methods=['GET'])
def get_entries():
    entries = Entry.query.all()
    entries_list = [{'id': entry.id, 'title': entry.title, 'text': entry.text} for entry in entries]
    return jsonify(entries_list)

# Route to serve HTML page with a table
@APP.route('/')
def show_entries():
    return render_template('pytst.html')

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)
