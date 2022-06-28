import threading

from flask import flash, render_template, session, redirect, url_for
from flask_login import login_required, login_user, logout_user
import utils
from forms import *
from info import GAMES_DICT
from models import User, Calibration
from __main__ import app, login_manager, db, socketio


@app.route('/games/5',methods=["GET","POST"])
@login_required
def game5():
    # Form for submitting data - current settings




    return render_template('game5.html',template_title="Proton's got moves",template_intro_text="Can you follow on?",template_game_form=None)

