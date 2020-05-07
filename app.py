from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import sqlite3
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
conn1 = sqlite3.connect('site.db', check_same_thread=False)
cursor1 = conn1.cursor()

sql1 = '''CREATE TABLE IF NOT EXISTS User
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
         username VARCHAR(20),
         email VARCHAR(120),
         image_file VARCHAR(20) DEFAULT 'default.jpg',
         password VARCHAR(60))'''

cursor1.execute(sql1)

conn2 = sqlite3.connect('post.db', check_same_thread=False)
cursor2 = conn2.cursor()
sql2 = '''CREATE TABLE Post
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          title VARCHAR(100),
          date_posted datetime default current_timestamp,
          content TEXT)'''
cursor2.execute(sql2)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)


conn2.close()
conn1.close()

