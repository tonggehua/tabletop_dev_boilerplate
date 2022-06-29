import threading

from flask import flash, render_template, session, redirect, url_for
from flask_login import login_required, login_user, logout_user
import plotly
import plotly.graph_objects as go
import utils
from forms import Game5Form
from info import GAMES_DICT
from models import User, Calibration
from __main__ import app, login_manager, db, socketio
import plotly.express as px
import pandas as pd
import json
import numpy as np

@app.route('/games/5',methods=["GET","POST"])
def game5():
    # Form for submitting data - current settings
    game_form = Game5Form()
    if game_form.validate_on_submit():
        # Run simulation and display results
        print('form validated')

    j1, j2, j3, j4 = make_default_graphs()
    print(j1)


    return render_template('game5.html',template_title="Proton's got moves",template_intro_text="Can you follow on?",
                           template_game_form=game_form, graphJSON_spin=j1, graphJSON_mx =j2, graphJSON_my=j3, graphJSON_mz =j4)

def make_default_graphs():
    tmodel = np.linspace(0,1,100)
    df = pd.DataFrame({'t':tmodel,'Mx':np.zeros(tmodel.shape),'My':np.zeros(tmodel.shape),'Mz':np.ones(tmodel.shape)})
    # J1 : vector
    f1 = go.Figure(data=go.Cone(x=[0],y=[0],z=[1],u=[0],v=[0],w=[1]))
    f1.add_trace(go.Scatter3d(x=[0,0],y=[0,0],z=[0,1],mode='lines'))
    j1 = json.dumps(f1,cls=plotly.utils.PlotlyJSONEncoder)

    # j2,j3,j4 : M

    j2 = json.dumps(px.scatter(df,x='t',y='Mx'),cls=plotly.utils.PlotlyJSONEncoder)
    j3 = json.dumps(px.scatter(df,x='t',y='My'),cls=plotly.utils.PlotlyJSONEncoder)
    j4 = json.dumps(px.scatter(df,x='t',y='Mz'),cls=plotly.utils.PlotlyJSONEncoder)

    return j1,j2,j3,j4