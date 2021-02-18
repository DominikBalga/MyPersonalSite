from flask import Flask, render_template,redirect,url_for
from flask_bootstrap import Bootstrap
from forms import ContacForm, ProjectForm
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
import smtplib
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secretkey")
Bootstrap(app)
ckeditor = CKEditor(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

my_email = os.getenv("email")
password = os.getenv("password")

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

db.create_all()

@app.route("/")
def home():
    all_projects = db.session.query(Project).all()
    return render_template("index.html",projects=all_projects)


@app.route("/add-project", methods = ["POST","GET"])
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
    return render_template("addproject.html", form=form, round=round)

@app.route("/my-projects")
def myprojects():
    all_projects = db.session.query(Project).all()
    return render_template("allprojects.html",projects=all_projects)

@app.route("/about-me")
def aboutme():
    return render_template("aboutme.html")


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
    return render_template("contactme.html",form=form,message_sent=message_sent)



if __name__ == "__main__":
    app.run(debug=True)
