from flask import Flask, session, render_template, request, url_for, flash, redirect
import  sqlite3
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c4a7c610573aecf8b60d19e32b4d4c51'


posts = [
    {
        'author': 'Realdo Beja',
        'title' : 'Blog post 1',
        'date_posted' : '6 May 2020'
    },
    {
        'author': 'Klara Lami',
        'title': 'Blog post 2',
        'date_posted': '7 May 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        flash(f'Account created for {registration_form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', registration_form=registration_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template('login.html', title = 'Login', login_form = login_form)



if __name__ == "__main__":
    app.run(debug = True)
