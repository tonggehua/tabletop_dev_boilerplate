import plotly
import pandas as pd
import plotly.express as px
import json
import numpy as np

def get_fake_calibration_plots(f0):
    tmodel, fid = generate_fake_fid(f0)
    dt = tmodel[1] - tmodel[0]
    fmodel = np.linspace(-0.5*(1/dt),0.5*(1/dt),len(fid),endpoint=False)
    spectrum = generate_spectrum_from_fake_fid(fid)
    tx_model, signal = generate_Tx_signal_plot()
    df = pd.DataFrame({'t':tmodel, 'fid':fid, 'f':fmodel, 'spectrum':spectrum})
    df2 = pd.DataFrame({'tx_model':tx_model, 'tx_signal':signal})

    fig_fid = px.line(df,x='t',y='fid')
    fig_spectrum = px.line(df,x='f',y='spectrum')
    fig_fa_calib = px.scatter(df2, x='tx_model',y='tx_signal')

    graphJSON1 = json.dumps(fig_fid,cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig_spectrum,cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig_fa_calib, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON1, graphJSON2, graphJSON3

def generate_fake_fid(f0):
    tmodel = np.linspace(0,1,1000,endpoint=False)
    signal = 30*np.exp(-tmodel)*np.sin((f0 - 15.43e6)*tmodel) + (np.random.rand(len(tmodel))-0.5)
    return tmodel, signal

def generate_spectrum_from_fake_fid(fid):
    spectrum = np.absolute(np.fft.fftshift(np.fft.fft(fid)))
    return spectrum

def generate_Tx_signal_plot():
    tx_model = np.linspace(0,1,100)
    signal = np.sin(tx_model*np.pi*(5*np.random.rand()))
    return tx_model, signal
