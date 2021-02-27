from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class ContacForm(FlaskForm):
    name = StringField("Your Name",validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    text = TextAreaField('Text', render_kw={"rows": 10, "cols": 11},validators=[DataRequired()])
    submit = SubmitField("SEND ME THE MESSAGE")

class ProjectForm(FlaskForm):
    name = StringField("Project name",validators=[DataRequired()])
    subtitle = StringField('subtitle', validators=[DataRequired()])
    body = CKEditorField('Text',validators=[DataRequired()])
    img_url = StringField('image url', validators=[DataRequired(),URL()])
    submit = SubmitField("SAVE")

class LoginForm(FlaskForm):
    email = StringField("Admin Email", validators=[DataRequired()])
    password = PasswordField("Admin Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class RegisterForm(FlaskForm):
    email = StringField("Admin Email", validators=[DataRequired()])
    password = PasswordField("Admin Password", validators=[DataRequired()])
    secret = StringField("Secret admin passcode", validators=[DataRequired()])
    submit = SubmitField("Reg Me In!")