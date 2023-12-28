

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from sensors.models import Range,Temperature, Pressure, Rain
from plotly.offline import plot
import plotly.graph_objs as go
from django_pandas.io import read_frame
import numpy as np
from datetime import datetime,timedelta
from settings.models import TankConfig
import dash
from dash import dcc, html
from django_plotly_dash import DjangoDash


speedofsoundconstant=340 #m/s


# def query_sensordata():
    # settings=TankConfig.objects.first()
    
    # since=datetime.now()-timedelta(days=30)
    # qry=SensorData.objects.filter(epoch__gte=since)
    # sensordf=read_frame(qry)
    # #augment dataframe
    # sensordf['vsound']=20.05*(273.16 + sensordf['temperature']).apply(np.sqrt)
    # sensordf['deltavsound']=speedofsoundconstant-20.05*(273.16 + sensordf['temperature']).apply(np.sqrt)
    # sensordf['waterlevel']= settings.sounderheight*1e2-sensordf['traveltime']*sensordf['vsound']*1e-4/2
    # return sensordf


# df=query_sensordata()


# app = DjangoDash('WetcaveDash')   # replaces dash.Dash

# app.layout = html.Div([
    # dcc.Graph(id='graph-sensor-data'),
    # dcc.RadioItems(
        # id='dropdown-color',
        # options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        # value='red'
    # ),
    # html.Div(id='output-color',className="text-nile"),
    # dcc.RadioItems(
        # id='dropdown-size',
        # options=[{'label': i,
                  # 'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
        # value='medium'
    # ),
    # html.Div(id='output-size')

# ])

# @app.callback(
    # dash.dependencies.Output('output-color', 'children'),
    # [dash.dependencies.Input('dropdown-color', 'value')])
# def callback_color(dropdown_value):
    # return "The selected color is %s." % dropdown_value

# @app.callback(
    # dash.dependencies.Output('output-size', 'children'),
    # [dash.dependencies.Input('dropdown-color', 'value'),
     # dash.dependencies.Input('dropdown-size', 'value')])
# def callback_size(dropdown_color, dropdown_size):
    # return "The chosen T-shirt is a %s %s one." %(dropdown_size,
                                                  # dropdown_color)


def waterlevelPlot(sounderHeight):
    #get since last week
    since=datetime.now()-timedelta(days=7)
    qry=Range.objects.filter(epoch__gte=since)
    sensordf=read_frame(qry)
    # sensordf['vsound']=20.05*(273.16 + sensordf['temperature']).apply(np.sqrt)
    # sensordf['deltavsound']=speedofsoundconstant-20.05*(273.16 + sensordf['temperature']).apply(np.sqrt)
    # sensordf['waterlevel']= sounderHeight*1e2-sensordf['traveltime']*sensordf['vsound']*1e-4/2
    fig=go.Figure()

    fig.add_trace(go.Line(name = 'Range', x = sensordf['time'], y = sensordf['traveltime']*speedofsoundconstant*1e-4/2))
    # fig.add_trace(go.Scatter(name = 'Water level (Temp corrected)', x = sensordf['epoch'], y =sensordf['waterlevel'],mode="lines+markers"))

    # fig.add_trace(go.Line(name = 'Delta Range (Temp effect)', x = sensordf['epoch'], y = sensordf['traveltime']*sensordf['deltavsound']*1e-4/2))
    # fig.add_trace(go.Line(name = 'Delta Range (Temp effect)', x = sensordf['epoch'], y = sensordf['pressure']))
    

    #Update layout 
    fig.update_layout(title_text = 'Tank water level',
            xaxis_title = 'time',
            yaxis_title = 'height [cm]',template="plotly_dark")
    
    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj


@login_required()
def dashboard(request):
    # retrieve the settings
    settings=TankConfig.objects #.first()
    if settings.count() == 0:
        settings=TankConfig()
    else:
        settings=settings.first()
    plotlyhtml=waterlevelPlot(settings.sounderheight) 
    # return render(request,"dashboard.html")
    return render(request,"dashboard.html",context={"content":plotlyhtml})
