from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Minn#2020@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, name, body):
        self.name = name
        self.body = body
    

@app.route('/')
def index():

    return render_template('home.html', title = 'Hello')

@app.route('/blog')
def blog():

    return render_template('blog.html', title = 'Blog')

@app.route('/newpost')
def newpost():

    return render_template('newpost.html', title = 'Newpost')

if __name__ == "__main__":
    app.run()