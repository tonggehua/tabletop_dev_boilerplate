import plotly
import pandas as pd
import plotly.express as px
import json
import numpy as np

def get_fake_calibration_plots():
    tmodel, fid = generate_fake_fid()
    dt = tmodel[1] - tmodel[0]
    fmodel = np.linspace(-0.5*(1/dt),0.5*(1/dt),len(fid),endpoint=False)
    spectrum = generate_spectrum_from_fake_fid(fid)
    df = pd.DataFrame({'t':tmodel, 'fid':fid, 'f':fmodel, 'spectrum':spectrum})
    fig_fid = px.line(df,x='t',y='fid')
    fig_spectrum = px.line(df,x='f',y='spectrum')

    graphJSON1 = json.dumps(fig_fid,cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig_spectrum,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON1, graphJSON2

def generate_fake_fid():
    tmodel = np.linspace(0,1,500,endpoint=False)
    signal = 30*np.exp(-tmodel) + (np.random.rand(500)-0.5)
    return tmodel, signal

def generate_spectrum_from_fake_fid(fid):
    spectrum = np.absolute(np.fft.fftshift(np.fft.fft(fid)))
    return spectrum


if __name__ == '__main__':
    j1,j2 = get_fake_calibration_plots()
    print(j1)
    print(j2)