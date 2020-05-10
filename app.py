from flask import Flask, render_template, url_for, flash, redirect
from flask import session
from forms import RegistrationForm, LoginForm
import sqlite3
from passlib.hash import sha256_crypt
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

conn2 = sqlite3.connect('post.db', check_same_thread= False)
cursor2 = conn2.cursor()
sql2 = '''CREATE TABLE IF NOT EXISTS Post 
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
        username = form.username.data
        cursor1.execute("SELECT username FROM User WHERE username=? ", (username,))
        username_fetched_from_db = cursor1.fetchone()

        email = form.email.data
        cursor1.execute("SELECT email FROM User WHERE email=? ", (email,))
        email_fetched_from_db = cursor1.fetchone()

        #take_username_fetched_from_tuple = pd.DataFrame(username_fetched_from_db)
        #convert_username_in_list = take_username_fetched_from_tuple[0].tolist()

        if username_fetched_from_db or email_fetched_from_db:
            return _handle_account_exists(username_fetched_from_db, email_fetched_from_db)

        password = form.password.data
        return _handle_create_db_entry(username, email, password)

    return render_template('register.html', title='Register', form=form)

def _handle_account_exists(username, email):
    messages = []
    if username:
        messages.append('Username taken')
    elif email:
        messages.append('Email taken')

    message = "\n".join([str(m) for m in messages])
    flash(message, 'danger')
    return redirect(url_for('register'))

def _handle_create_db_entry(username, email, password):
    secure_password = sha256_crypt.encrypt(str(password))
    sql1 = "INSERT INTO User (username, email, password) VALUES ('{}','{}','{}')".format(
        username, email, secure_password
    )
    cursor1.execute(sql1)
    conn1.commit()
    flash(f'Account created! You are now able to log in ', 'success')
    return redirect(url_for('login'))



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email_login = form.email.data
        password_login = form.password.data
        cursor1.execute("SELECT email FROM User WHERE email=?", (email_login,))
        email_fetched = cursor1.fetchone()
        cursor1.execute("SELECT email FROM User WHERE email=?", (password_login,))
        password_fetched = cursor1.fetchone()
        if not email_fetched:
            flash("Email does not exists", "danger")
            return redirect(url_for("login"))
        else:
            for password_fetched_index in password_fetched:
                if sha256_crypt.verify(password_login, password_fetched_index):
                    session['log'] = True
                    flash('You are now Logged In', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Incorrect password', 'danger')
                    return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


conn2.close()
conn1.close()