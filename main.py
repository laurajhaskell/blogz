from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogpassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'fFjl42&kJ9ls'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    entry = db.Column(db.String(120))

    def __init__(self, name):
        self.title = title
        self.entry = entry


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST'
        blog_title = request.form['title']
        blog_entry = request.form['entry']
        new_blog = Blog(blog_title, blog_entry)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('newpost.html')
        
        #validate
        

    blogs = Blog.query.all()
    return render_template('blog.html', title="Build a Blog", blogs=blogs)


@app.route('/add-entry')
def add_entry():
    return redirect('/')


@app.route('/new-post', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST'
        blog_title = request.form['title']
        blog_entry = request.form['entry']
        new_blog = Blog(blog_title, blog_entry)
        db.session.add(new_blog)
        db.session.commit()

        title_error = ''
        entry_error = ''

        if blog_title == '':
            title_error = "Please enter a title"

        if blog_entry == '':
            entry_error = "Please type an entry"

        if title_error or entry_error:
            return render_template('blog.html')
        
    return render_template('new-post.html', title="Build a Blog")


if __name__ == '__main__':
    app.run()