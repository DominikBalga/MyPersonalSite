from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


class ContacForm(FlaskForm):
    name = StringField("Your Name",validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    text = TextAreaField('Text', render_kw={"rows": 10, "cols": 11},validators=[DataRequired()])
    submit = SubmitField("SEND ME THE MESSAGE")