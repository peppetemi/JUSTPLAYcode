from flask import Flask, render_template, url_for, flash, redirect
from flask import request, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


# - SET UP -
app = Flask(__name__)
app.config['SECRET_KEY'] = 'wordhardtobeguessed'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///prova1.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# - STUDENT TABLE -
class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(26), unique=True, nullable=True)
    password = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return "<Student %r>" % self.name

# - MATCH TABLE -
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    private_match = db.Column(db.String, nullable=True)
    field = db.Column(db.String(30), nullable=True)
    date = db.Column(db.Date, nullable=True)
    players_number = db.Column(db.Integer, nullable=True)


# - LOGIN MANAGER -
@login_manager.user_loader
def load_user(student_id):
    return Student.query.get(int(student_id))


from forms import Formname, LoginForm, MatchForm

# - DATABASE CREATION -
@app.before_first_request
def setup_db():
    #db.drop_all()
    db.create_all()

# - HOME PAGE -
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# - REGISTRATION PAGE -
@app.route('/register', methods=['POST','GET'])
def register():
    formpage = Formname()
    if formpage.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(formpage.password.data)
        st = Student(firstname=formpage.firstname.data,
                      lastname=formpage.lastname.data,
                      name=formpage.name.data,
                      email=formpage.email.data,
                      password=hashed_password)
        db.session.add(st)
        db.session.commit()
        login_user(st)
        return redirect(url_for('home'))
    return render_template('register.html', formpage=formpage, title='Registration')

# - LOGIN PAGE -
@app.route("/login",methods=['POST','GET'])
def login():
    formpage=LoginForm()
    if formpage.validate_on_submit():
        st=Student.query.filter_by(email=formpage.email.data).first()
        if st:
            if bcrypt.check_password_hash(st.password, formpage.password.data):
                login_user(st)
                return redirect(url_for('profilepage'))
    return render_template('login.html', formpage=formpage, title='Login')

# - PROFILE PAGE -
@app.route("/profilepage")
@login_required
def profilepage():
    return render_template('profilepage.html', name=current_user.name)

# - LOGOUT -
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# - MATCH CREATION -
@app.route("/createamatch", methods=['POST','GET'])
@login_required
def createamatch():
    formpage=MatchForm()
    if formpage.validate_on_submit():
        match = Match(
            private_match=formpage.private_match.data,
            date=formpage.date.data)
        db.session.add(match)
        db.session.commit()
        return redirect(url_for('fieldselection'))
    return render_template('createamatch.html', formpage=formpage, title='Create a match')

# - FIELD SELECTION -
@app.route("/fieldselection", methods=['POST', 'GET'])
@login_required
def fieldselection():
    return render_template('fieldselection.html')


# - ERROR 404 -
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)
