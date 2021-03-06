'''
This file holds the logic of the controller
'''
import sqlite3
from flask import Flask, render_template, request, session, \
                  flash, redirect, url_for, g
from functools import wraps

# Configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'    #-- TODO: This key need to be changed before deployment

app = Flask(__name__)

# Pulling in the app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

@app.route('/',methods = ['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != app.config["USERNAME"] or \
           request.form['password'] != app.config["PASSWORD"]:
            error = "Username and/or Password don't match"
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))

    return render_template("login.html", error = error)

@app.route('/main')
@login_required
def main():
    g.database = get_db_connection()
    cur = g.database.execute('SELECT * FROM posts')
    posts_list = [ dict(title = row[0],post = row[1]) for row in cur.fetchall() ]
    g.database.close()
    return render_template("main.html", posts=posts_list)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/add',methods=['POST'])
@login_required
def add_post():
    title = request.form['title']
    post = request.form['post']
    if not post or not title:
        flash('All fields are required before submitting your posts')
        return redirect(url_for('main'))
    else:
        g.database = get_db_connection()
        cur = g.database.execute('INSERT INTO posts VALUES("{0}","{1}")'.format(title,post))
        g.database.commit()
        g.database.close()
        flash('A new post is added')
        return redirect(url_for('main'))

def get_db_connection():
    return sqlite3.connect(app.config["DATABASE"])

if __name__ == "__main__":
    app.run(debug=True)