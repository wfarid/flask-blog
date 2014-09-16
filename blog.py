'''
This file holds the logic of the controller
'''
import sqlite3
from flask import Flask, render_template, request, session, \
                  flash, redirect, url_for, g

# Configuration
DATABASE = "blog.db"

app = Flask(__name__)

# Pulling in the app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/main')
def main():
    return render_template("main.html")

def get_db_connection():
    return sqlite3.connect(app.config["DATABASE"])

if __name__ == "__main__":
    app.run(debug=True)