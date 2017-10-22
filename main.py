from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
#using the test secret key for session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#creating some classes...classes are good to go
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    

#We can handle that...

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index','submit']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect ('/login')


@app.route('/')
def index():
    users = User.query.all()
    return render_template('home.html', title = 'Hello', users=users)

@app.route('/blog', methods=['POST','GET'])
def blog():
    if request.args.get('id'):
        id = request.args.get('id')
        blog = Blog.query.get(id)
        return render_template('submit.html',blog=blog)
    if request.args.get('user'):
        user_id = request.args.get('user')
        blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('user.html', blogs=blogs)
    blogs = Blog.query.all()
    users = User.query.all()
    return render_template('blog.html', blogs=blogs, users=users)

@app.route('/newpost', methods = ['GET','POST'])
def newpost():
    if request.method == "GET":
        return render_template("newpost.html", title = 'Newpost')

    elif request.method == "POST":
        name = request.form["name"]
        body = request.form["body"]
        owner = User.query.filter_by(username=session['username']).first()
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
            blog_post = Blog(name, body, owner)
            db.session.add(blog_post)
            db.session.commit()
            id = blog_post.id
            return redirect("/submit?id={}".format(id))
@app.route('/submit')
def submit():
    id = request.args.get("id")
    blog = Blog.query.filter_by(id = id).first()
    return render_template("submit.html", blog = blog) 

@app.route("/login", methods=['GET', 'POST'])
def login():
    error_username = ''
    error_password = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        if not user:
            error_username = 'User name does not exist'
            return render_template('login.html', error_username=error_username)
        else: 
            error_password = 'Password incorrect'
            return render_template('login.html', error_password=error_password)
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route("/signup", methods=['GET', 'POST'])
def signup():

    error_username = ''
    error_password = ''
    error_verify_password = ''
    

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']

        if username == '':
            error_username = 'Please enter a User name'
            return render_template('signup.html', error_username = error_username)

        if password == '':
            error_password = 'Please enter a Password'
            return render_template('signup.html', error_password = error_password)

        if verify_password == '':
            error_verify_password = 'Please retype the password'
            return render_template('signup.html', error_verify_password = error_verify_password)

        if len(username) <= 3:
            error_username = 'User name must be longer than 3 characters'
            return render_template('signup.html',error_username=error_username) 

        if len(password) <= 3:
            error_password = 'Password must be longer than 3 characters'
            return render_template('signup.html', error_password=error_password)       
        
        if password != verify_password:
            error_verify_password = 'Please match password'
            return render_template('signup.html', error_verify_password=error_verify_password)
        
        username_in_db = User.query.filter_by(username=username).count()
        if username_in_db > 0:
            error_username = 'User name is already taken'
            return render_template('signup.html', error_username=error_username)


        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/newpost")
    else:
        return render_template('signup.html')

if __name__ == "__main__":
    app.run()