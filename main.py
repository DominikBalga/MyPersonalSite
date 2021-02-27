from flask import Flask, render_template,redirect,url_for,flash, send_from_directory
from flask_bootstrap import Bootstrap
from forms import ContacForm, ProjectForm, LoginForm, RegisterForm
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required,current_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secretkey")
secret = os.getenv("secret")
Bootstrap(app)
ckeditor = CKEditor(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

my_email = os.getenv("email")
password = os.getenv("password")

class User(UserMixin, db.Model):
    _tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

@app.route('/admin', methods=["GET", "POST"])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('admin'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again or register')
            return redirect(url_for('admin'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("adminlogin.html", form=form,user=current_user)


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

db.create_all()

@app.route('/register', methods=["GET", "POST"])
def adminregister():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            return redirect(url_for('admin'))
        elif form.secret.data == secret:
            print("i did this")
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=form.email.data,
                password=hash_and_salted_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home"))
        flash("BAD ADMIN SECRET, IF YOU WANT TO MODIFY PROJECTS ASK ADMIN AT BALGA.DOMO@GMAIL.COM FOR SECRET")

    return render_template("registeradmin.html", form=form,user=current_user)

@app.route("/")
def home():
    all_projects = db.session.query(Project).all()
    return render_template("index.html",projects=all_projects,user=current_user)

@app.route("/projects/<int:id>")
def project(id):
    project = Project.query.filter_by(id=id).first()
    return render_template("project.html", project=project,user=current_user)

@app.route("/add-project", methods = ["POST","GET"])
@login_required
def add_project():
    form = ProjectForm()
    round = 1
    if form.validate_on_submit():
        project_name=form.data["name"]
        project_subtitle=form.data["subtitle"]
        project_text=form.data["body"]
        project_img=form.data["img_url"]
        new_project =  Project(title=project_name,
                               subtitle=project_subtitle,
                               body=project_text,
                               img_url=project_img)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("myprojects"))
    return render_template("addproject.html", form=form, round=round,user=current_user)

@app.route("/my-projects")
def myprojects():
    all_projects = db.session.query(Project).all()
    return render_template("allprojects.html",projects=all_projects,user=current_user)

@app.route("/about-me")
def aboutme():
    return render_template("aboutme.html",user=current_user)


@app.route("/contact-me",methods=["GET","POST"])
def contactme():
    form = ContacForm()
    message_sent = False
    if form.validate_on_submit():
        name = form.data["name"]
        email = form.data["email"]
        text = form.data["text"]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=my_email, msg=f"Subject: {name} contacted you\n\n"
                                                    f"Email: {email}\n"
                                                    f"Text : {text}\n")
            message_sent=True
    return render_template("contactme.html",form=form,message_sent=message_sent,user=current_user)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/downloadcert')
def downloadcert():
    return send_from_directory('static',
                              filename="images/cert.pdf", as_attachment=True)

@app.route('/downloadcven')
def downloadcven():
    return send_from_directory('static',
                               filename="images/cvenDominikBalga.pdf", as_attachment=True)

@app.route('/downloadcvsk')
def downloadcvsk():
    return send_from_directory('static',
                               filename="images/cvskDominikBalga.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
