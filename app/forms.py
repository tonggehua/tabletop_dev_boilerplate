from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, PasswordField, DecimalField, DecimalRangeField
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange, InputRequired


# Accounts and Authentication
class Register_Form(FlaskForm):
    username_field = StringField("Username",validators=[DataRequired()])
    password_field = PasswordField('Password', validators=[DataRequired()])
    password2_field = PasswordField('Re-enter Password',
                                    validators=[DataRequired(), EqualTo('password_field',message='Passwords must match')])
    submit_field = SubmitField("Register!")

class Login_Form(FlaskForm):
    username_field = StringField("Username",validators=[DataRequired()],default='admin')
    password_field = PasswordField("Password",validators=[DataRequired()])
    submit_field = SubmitField("Log in")


# Calibration
class FID_Params_Form(FlaskForm):
    tr_field = DecimalField('Repetition Time (ms)', validators=[DataRequired(), NumberRange(min=5,max=5000)],default=1000)
    readout_time_field = DecimalField('Readout duration (ms)',validators=[DataRequired(),NumberRange(min=10,max=100)],default=30)
    num_rep_field = IntegerField('Number of repetitions',validators=[DataRequired(),NumberRange(min=1,max=50)],default=1)
    num_avg_field = IntegerField('Number of averages', validators=[DataRequired(),NumberRange(min=1,max=100)],default=1)
    submit_field = SubmitField('Update')

class Display_Opts_Form(FlaskForm):
    autoscale_field = BooleanField("Autoscale", default=True)
    show_prev_field = BooleanField('Show previous', default=False)

class Calibration_Form(FlaskForm):
    f0_field = DecimalField("Frequency (MHz)", validators=[InputRequired(), NumberRange(min=0,max=50)],default=15)
    shimx_field = DecimalRangeField("Shim x", validators=[InputRequired(),NumberRange(min=-1.0,max=1.0)],default=0.0)
    shimy_field = DecimalRangeField("Shim y", validators=[InputRequired(),NumberRange(min=-1.0,max=1.0)],default=0.0)
    shimz_field = DecimalRangeField("Shim z", validators=[InputRequired(),NumberRange(min=-1.0,max=1.0)],default=0.0)
    tx_amp_field = DecimalField('Tx amplitude', validators=[InputRequired()],default=0.5)
    rx_gain_field = DecimalField('Rx gain (db)', validators=[InputRequired()],default=3)
    submit_field = SubmitField("SAVE")


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


