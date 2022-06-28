# routes_main.py
# Gehua Tong, June 2022
# Login, register, and calibration pages for Virtual Scanner Biobus Mode

import threading
from flask import flash, render_template, session, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
import utils
from forms import *
from info import GAMES_DICT
from models import User, Calibration
from fake_data_generator import get_fake_calibration_plots, SignalPlotsThread, FlipAnglePlotThread, get_empty_calibration_plots
from __main__ import app, login_manager, db, socketio



def initialize_parameters():
    session.clear()
    session['scanningFID'] = False
    session['scanningFA'] = False
    session['calibration'] = {'f0':15e6, 'shimx':0.0, 'shimy':0.0, 'shimz':0.0, 'tx_amp': 3,
                              'autoscale':True, 'show_prev':False}
    session['user_id'] = None



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
            print('login success')
            flash("Login successful!")
            session['user_id'] = user.id
            return redirect('index')
        # If login fails, show error message
        else:
            print('login failed')
            flash('Wrong credentials - login failed')
            return redirect(url_for('login'))

    return render_template("login.html",template_login_form=login_form)

# template_title='login',
#                            template_intro_text="Log into Virtual Scanner Biobus",



# Register page
@app.route('/register',methods=['GET','POST'])
def register():
    reg_form = Register_Form()
    print('on register page...')

    if request.method == 'POST':
        print(request.form)

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

    # Deal with calibration parameters
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
            flash(f"Parameters saved: f0 = {params['f0']}, shimx = {params['shimx']}, shimy={params['shimy']}, \
                  tx amp = {params['tx_amp']}")
        except:
            db.session.rollback()
        # Update session TODO includ all params to session...
        utils.update_session_subdict(session,'calibration', params)
        print(f"session f0 updated to {session['calibration']['f0']}")

    # Deal with shared sequence parameters
    if fid_params_form.validate_on_submit():
        print("FID parameters submission is validated")
        # TODO - integrate it with a model in database...

    #j1, j2, j3 = get_fake_calibration_plots(session['calibration']['f0'])
    j1, j2, j3 = get_empty_calibration_plots()
    return render_template("calibration.html",template_title="Calibration",
                           template_intro_text="Let's calibrate the scanner!",template_calibration_form=calib_form,
                           template_params_form=fid_params_form, template_disp_form=display_opts_form,
                           graphJSON_left=j1, graphJSON_center=j2,graphJSON_right=j3)

# When client says RUN, we run.
@socketio.on('run scans')
def pump_out_fake_plots(message):
    # Initiate the thread only if we are not scanning now
    print(session['scanningFID'])
    if not session.get('scanningFID'):
        print("MAKING A NEW THREAD")
        calib_thread = SignalPlotsThread(session['calibration']['f0'])
        calib_thread.start()
        session['scanningFID'] = True
        session.modified = True
    else:
        print('we are in else')
        for th in threading.enumerate():
            if hasattr(th,'f0'):
                th.f0 = session['calibration']['f0']
    socketio.emit('take this',{'data':'THE SOCKET IS WORKING'})

# When client says STOP, we stop.
@socketio.on('stop scans')
def stop_the_fake_plots(message):
    print(message['data'])
    for th in threading.enumerate():
        if hasattr(th,'f0'):
            th.raise_exception()
            th.join()
            session['scanningFID'] = False
            session.modified = True
        if hasattr(th,'tx_amp_90'): # FA thread
            th.raise_exception()
            th.join()
            session['scanningFA'] = False
            session.modified = True

# Run FA calibration
@socketio.on('run FA')
def run_fake_FA_calibration(message):
    print(message['data'])
    # Get a FA plot
    if not session.get('scanningFA'):
        fa_thread = FlipAnglePlotThread(tx_amp_90=3, tx_amp_max=10, Npts=50) # Preset - TODO incorporate as options?
        fa_thread.start()
        session['scanningFA'] = True
        session.modified = True


@socketio.on('zero shims')
def zero_shims(message):
    print(message['data'])
    utils.update_session_subdict(session,'calibration',{'shimx':0.0,'shimy':0.0,'shimz':0.0})