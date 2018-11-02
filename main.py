from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzpassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&xPsB'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    # use foreign key to link user id
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, owner, pub_date=None):
        self.title = title
        self.body = body
        self.owner = owner
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']

    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/')
def index():

    users = User.query.all()
    return render_template('index.html', users=users)
    # blogs = Blog.query.all()

    # if request.args:
    #     return redirect('/blog')

    # return render_template('index.html', blogs=blogs)


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = ''
    password = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        # user enters username not in database and must signup
        if not existing_user:
            flash("User does not exist. Sign up.")
            return redirect('/signup')

        # user enters correct password and directed to create new post
        if existing_user and existing_user.password == password:
            session['username'] = username
            return redirect('/newpost')
        # user enters username in database and password not in database 
        else:
            flash("Incorrect password")
            return render_template('login.html')
    
    return render_template('login.html') 



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username = ''
    password = ''
    verify = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # error for blank username or less than 3 char
        if not username:
            flash("Please enter username", 'error')
            return render_template('signup.html')
        elif len(username) < 3:
            flash("Invalid username. Must be 3 characters or more.", 'error')
            return render_template('/signup.html')

        # error for blank password or less than 3 char
        elif not password:
            flash("Please enter password", 'error')
            return render_template('signup.html')
        elif len(password) < 3:
            flash("Invalid password. Must be 3 characters or more.", 'error')
            return render_template('/signup.html')
        
        # error for blank verify or not matching
        elif not verify:
            flash("Please verify password", 'error')
            return render_template('/signup.html')
        elif verify != password:
            flash("Passwords do not match.", 'error')
            return render_template('/signup.html')

        existing_user = User.query.filter_by(username=username).first()

        # all correct fields, stores info in database
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        # error for existing username
        else:
            flash("Username already exists. Choose a new username." 'error')
            return redirect('/newpost')
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    title = ''
    body = ''
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'GET':
        return render_template('newpost.html', heading="New Blog")
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        #validate blog title and body
        if title == '' and body == '':
            flash("Please enter a title and body.", 'error')
        elif title == "":
            flash("Please enter a title", 'error')
            return render_template('newpost.html', body=body)
        elif body == "":
            flash("Please write a blog post", 'error')
            return render_template('newpost.html', title=title)

        else:
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()

            #set unique id for each new blog
            num = new_blog.id
            return redirect('/blog?id={0}'.format(num))

    return render_template('newpost.html', title=title)


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blogs = Blog.query.all()
    users = User.query.all()
    title = 'title'
    body = 'body'

    if 'id' in request.args:
        blog_id = request.args.get('id')

        for blog in blogs:
            if int(blog_id) == blog.id:
                title = blog.title
                body = blog.body
                owner_id = blog.owner_id
                owner = User.query.filter_by(id=owner_id).first()
                username = owner.username
                return render_template('singlepost.html', title=title, body=body, username=username, owner_id=owner_id)

    elif 'user' in request.args:
        user_id = request.args.get('user')
        user = User.query.filter_by(id=user_id).first()
        blogs = user.blogs
        return render_template('singleuser.html', user=user, blogs=blogs, )

    else: 
        return render_template('blog.html',blogs=blogs)


if __name__ == '__main__':
    app.run()