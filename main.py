from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from forms import ContacForm
import smtplib
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secretkey")
Bootstrap(app)

my_email = os.getenv("email")
password = os.getenv("password")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/my-projets")
def myprojects():
    return "<h1>Nothing here yet, in progress</h1>"

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
