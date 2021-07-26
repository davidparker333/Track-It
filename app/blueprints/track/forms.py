from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PackageForm(FlaskForm):

    carrier = SelectField('Choose...', choices=['USPS', 'FedEx', 'UPS'], validators=[DataRequired()])
    tracking_number = StringField('Tracking Number', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    submit = SubmitField()