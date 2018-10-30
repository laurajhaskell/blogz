from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogpassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&xPsB'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date


@app.route('/')
def index():

    blogs = Blog.query.all()

    if request.args:
        return redirect('/blog')

    return render_template('index.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    if request.method == 'POST':
        title = request.form['blog-title']
        body = request.form['blog-body']

        #validate blog title and body
        if title == "":
            flash("Please enter a title", 'error')
            return render_template('newpost.html', body=body)
        elif body == "":
            flash("Please write a blog post", 'error')
            return render_template('newpost.html', title=title)

        
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.flush()
        db.session.commit()

        #set unique id for each new blog
        num = new_blog.id
        return redirect('/blog?id={0}'.format(num))

    return render_template('newpost.html')


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    #handle additional GET request
    num = request.args.get('id')
    blog = Blog.query.filter_by(id=num).first()
    return render_template('blog.html', blog=blog)


if __name__ == '__main__':
    app.run()