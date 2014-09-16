'''
Creating a database file blog.db with one table 'posts'
The table has two fields title and post.
'''
import sqlite3

with sqlite3.connect('blog.db') as connection:

    c = connection.cursor()

    c.execute("CREATE TABLE posts (title TEXT, post TEXT)")

    # executemany() could have been used instead
    c.execute('INSERT INTO posts VALUES("Good","I\'m good")')
    c.execute('INSERT INTO posts VALUES("Well","I\'m well")')
    c.execute('INSERT INTO posts VALUES("Excellent","I\'m excellent")')
    c.execute('INSERT INTO posts VALUES("Okay","I\'m okay")')
