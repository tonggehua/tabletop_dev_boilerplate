from flask import Flask, abort, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from forms import *
from info import GAMES_DICT
from models import User
from os import environ
from fake_data_generator import get_fake_calibration_plots

from __main__ import app


# Home
@app.route('/index')
#@login_required
def index():
    return render_template("index.html",template_dict_games=GAMES_DICT)


# Login page
@app.route('/',methods=["GET","POST"])
@app.route('/login',methods=["GET","POST"])
def login():
    login_form = Login_Form()
    if login_form.validate_on_submit():
        # If login successful, redirect to main page
        print(login_form.username_field.data)
        if login_form.username_field.data=='admin':
            print("I am an admin")
            return redirect('index')
        # If login fails, show error image
    return render_template("login.html",template_login_form=login_form)


# Register page
@app.route('/register',methods=['GET','POST'])
# TODO - this view function was copied in
def register():
    reg_form = Register_Form(csrf_enabled=False)
    if reg_form.validate_on_submit(): #define user with data from form here:
        user = User(username=reg_form.username.data, email=reg_form.email.data) # set user's password here:
        user.set_password(reg_form.password.data)
    #db.session.add(user)
    #db.session.commit()
    return render_template('register.html', title='Register', template_form=reg_form)


@app.route('/calibration',methods=["GET","POST"])
def calibration():
    #if request.method == 'POST':
     #   print(request.form['xshim'])
    f0_form = F0_Form()
    rf_form = RF_Form()
    shim_form = Shim_Form()
    j1, j2 = get_fake_calibration_plots()
    j3 = j2
    if f0_form.validate_on_submit():
        print(f0_form.f0_field.data)
    return render_template("calibration.html",template_title="Calibration",
                           template_intro_text="Let's calibrate the scanner!",template_f0_form=f0_form,
                           template_rf_form = rf_form, template_shim_form = shim_form,
                           graphJSON_left=j1, graphJSON_center=j2,graphJSON_right=j3)


# Games
@app.route('/games/1',methods=["GET","POST"])
def game1():
    return render_template('game1.html',template_title="",template_intro_text="",template_game_form=None)


@app.route('/games/2',methods=["GET","POST"])
def game2():
    return render_template('game2.html',template_title="",template_intro_text="",template_game_form=None)


@app.route('/games/3',methods=["GET","POST"])
def game3():
    return render_template('game3.html',template_title="",template_intro_text="",template_game_form=None)


@app.route('/games/4',methods=["GET","POST"])
def game4():
    game4form = Game4Form()
    if game4form.validate_on_submit():
        # Run simulation
        print(f"Slice thickness selected: {game4form.thk_field.data} mm")
    #if 'fov_field' in request.form:
    #    print(f"I have got the fov = {request.form['fov_field']} mm data!")

    return render_template('game4.html',template_title="Fresh Blood",template_intro_text="See how flow changes MR signal!",
                           template_game_form=game4form)


@app.route('/games/5',methods=["GET","POST"])
def game5():
    return render_template('game5.html',template_title="",template_intro_text="",template_game_form=None)


@app.route('/games/6',methods=["GET","POST"])
def game6():
    return render_template('game6.html',template_title="",template_intro_text="",template_game_form=None)


@app.route('/games/7',methods=["GET","POST"])
def game7():
    return render_template('game7.html',template_title="",template_intro_text="",template_game_form=None)


@app.route('/games/8',methods=["GET","POST"])
def game8():
    return render_template('game8.html',template_title="",template_intro_text="",template_game_form=None)
