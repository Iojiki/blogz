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
    entries = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html', title = 'Blog', entries = entries)

@app.route('/newpost', methods = ['GET','POST'])
def newpost():
    if request.method == "GET":
        return render_template("newpost.html", title = 'Newpost')

    elif request.method == "POST":
        name = request.form["name"]
        body = request.form["body"]
        error = False
        error_title = ''
        error_body = ''
        if name == "":
            error = True
            error_title = "Please include a title"
        if body == "":
            error = True
            error_body = "Please enter text in your post"
        if error == True:
            return render_template("newpost.html", title = 'Newpost', error_title = error_title, error_body = error_body)
        else:
            blog_post = Blog(name, body)
            db.session.add(blog_post)
            db.session.commit()
            id = blog_post.id
            return redirect("/submit?id={}".format(id))
@app.route('/submit')
def submit():
    id = request.args.get("id")
    blog_submit = Blog.query.filter_by(id = id).first()
    return render_template("submit.html", blog_submit = blog_submit) 

if __name__ == "__main__":
    app.run()