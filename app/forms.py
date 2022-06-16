from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, PasswordField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange


# Accounts and Authentication
class Register_Form(FlaskForm):
    username_field = StringField("Username",validators=[DataRequired()])
    password_field = PasswordField('Password', validators=[DataRequired()])
    password2_field = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit_field = SubmitField("Register!")

class Login_Form(FlaskForm):
    username_field = StringField("Username",validators=[DataRequired()],default='admin')
    password_field = PasswordField("Password",validators=[DataRequired()])
    submit_field = SubmitField("Log in")


# Calibration
class F0_Form(FlaskForm):
    f0_field = DecimalField("f0 (kHz)", validators=[DataRequired(), NumberRange(min=0,max=100)],default=15)
    submit_field = SubmitField("Save")

class Shim_Form(FlaskForm):
    shimx_field = DecimalField("Shim x", validators=[DataRequired(),NumberRange(min=-1.0,max=1.0)],default=0)
    shimy_field = DecimalField("Shim y", validators=[DataRequired(),NumberRange(min=-1.0,max=1.0)],default=0)
    shimz_field = DecimalField("Shim z", validators=[DataRequired(),NumberRange(min=-1.0,max=1.0)],default=0)
    submit_field = SubmitField("Save")

class RF_Form(FlaskForm):
    tx_amp_field = DecimalField('RF Tx amplitude', validators=[DataRequired()],default=3)
    rx_gain_field = DecimalField('RF Rx gain', validators=[DataRequired()],default=3)
    submit_field = SubmitField("Run flip angle calibration")


# TODO we need forms for all games
class Game1Form(FlaskForm):
    # TODO include fields
    submit_field = SubmitField("Submit")


# EXAMPLE
class Game4Form(FlaskForm):
    thk_field = DecimalField('Slice thickness (mm)',places=1,validators=[DataRequired(),NumberRange(min=1.0,max=10.0)])
    flip_field = IntegerField('Flip angle (degrees)',validators=[DataRequired(),NumberRange(min=1,max=90)])
    tr_field = IntegerField('Repetition Time (ms)',validators=[DataRequired(),NumberRange(min=20,max=2000)])
    submit_field = SubmitField("Run")


