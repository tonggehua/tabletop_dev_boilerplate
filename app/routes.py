from flask import flash, render_template, session, redirect, url_for
from flask_login import login_required, login_user, logout_user
import utils
from forms import *
from info import GAMES_DICT
from models import User, Calibration
from fake_data_generator import get_fake_calibration_plots
from __main__ import app, login_manager, db

def initialize_parameters():
    session['f0'] = 18e6 # TODO replace with current value in config

# Login callback (required)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to view this page"

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

# Home
@app.route('/index')
@login_required
def index():
    return render_template("index.html",template_dict_games=GAMES_DICT)


# Login page
@app.route('/',methods=["GET","POST"])
@app.route('/login',methods=["GET","POST"])
def login():
    initialize_parameters()
    login_form = Login_Form()
    if login_form.validate_on_submit():
        # If login successful, redirect to main page
        # Check login against database
        user = User.query.filter_by(username=login_form.username_field.data).first()
        if user is not None and user.check_password(login_form.password_field.data):
            login_user(user)
            flash("Login successful!")
            session['user_id'] = user.id
            return redirect('index')
        # If login fails, show error message
        else:
            flash('Wrong credentials - login failed')
            return redirect(url_for('login'))

    return render_template("login.html",template_login_form=login_form)




# Register page
@app.route('/register',methods=['GET','POST'])
def register():
    reg_form = Register_Form()
    print('on register page...')
    if reg_form.validate_on_submit(): #define user with data from form here:
        print("Validated!")
        user = User(username=reg_form.username_field.data) # set user's password here:
        user.set_password(reg_form.password_field.data)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    return render_template('register.html', title='Register', template_form=reg_form)


@app.route('/calibration',methods=["GET","POST"])
def calibration():
    #if request.method == 'POST':
     #   print(request.form['xshim'])
    calib_form = Calibration_Form()
    fid_params_form = FID_Params_Form()
    display_opts_form = Display_Opts_Form()
    j1, j2, j3 = get_fake_calibration_plots(session['f0'])
    if calib_form.validate_on_submit():
        print('Calibration validated')
        # Save to database
        new_calibration = Calibration(f0=calib_form.f0_field.data, shimx=calib_form.shimx_field.data,
                                      shimy=calib_form.shimy_field.data, shimz=calib_form.shimz_field.data,
                                      tx_amp=calib_form.tx_amp_field.data)
        params = new_calibration.get_config_dict()
        utils.update_configuration(params,"config.py")
        db.session.add(new_calibration)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        # Update session TODO includ all params to session...
        session['f0'] = float(params['f0'])

    return render_template("calibration.html",template_title="Calibration",
                           template_intro_text="Let's calibrate the scanner!",template_calibration_form=calib_form,
                           template_params_form=fid_params_form, template_disp_form=display_opts_form,
                           graphJSON_left=j1, graphJSON_center=j2,graphJSON_right=j3)


# Games
@app.route('/games/1',methods=["GET","POST"])
def game1():
    return render_template('game1.html',template_title="What is in an image?",template_intro_text="Voxels, field-of-views, and resolution ",template_game_form=None)


@app.route('/games/2',methods=["GET","POST"])
def game2():
    return render_template('game2.html',template_title="K-space magik",template_intro_text="Can you find your way?",template_game_form=None)


@app.route('/games/3',methods=["GET","POST"])
@login_required
def game3():
    return render_template('game3.html',template_title="Brains, please!",template_intro_text="Of mice and men",
                           template_game_form=None)


@app.route('/games/4',methods=["GET","POST"])
@login_required
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
@login_required
def game5():
    return render_template('game5.html',template_title="Proton's got moves",template_intro_text="Can you follow on?",template_game_form=None)


@app.route('/games/6',methods=["GET","POST"])
@login_required
def game6():
    return render_template('game6.html',template_title="Relaxation station",template_intro_text="Sit back and map",template_game_form=None)


@app.route('/games/7',methods=["GET","POST"])
def game7():
    return render_template('game7.html',template_title="Puzzled by Projection I",template_intro_text="Forward puzzle",template_game_form=None)


@app.route('/games/8',methods=["GET","POST"])
def game8():
    return render_template('game8.html',template_title="Puzzled by Projection II",template_intro_text="Backward puzzle",template_game_form=None)
