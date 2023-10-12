

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sensors.models import SensorData
from plotly.offline import plot
import plotly.graph_objs as go
from django_pandas.io import read_frame
import numpy as np
from datetime import datetime,timedelta
from settings.models import TankConfig
speedofsoundconstant=340 #m/s

def waterlevelPlot(sounderHeight):
    #get since last week
    since=datetime.now()-timedelta(days=7)
    qry=SensorData.objects.filter(epoch__gte=since)
    sensordf=read_frame(qry)
    sensordf['vsound']=20.05*(273.16 + sensordf['temperature']).apply(np.sqrt)
    sensordf['deltavsound']=speedofsoundconstant-20.05*(273.16 + sensordf['temperature']).apply(np.sqrt)
    sensordf['waterlevel']= sounderHeight*1e2-sensordf['traveltime']*sensordf['vsound']*1e-4/2
    fig=go.Figure()

    # fig.add_trace(go.Line(name = 'Range', x = sensordf['epoch'], y = sensordf['traveltime']*speedofsoundconstant*1e-4/2))
    fig.add_trace(go.Scatter(name = 'Water level (Temp corrected)', x = sensordf['epoch'], y =sensordf['waterlevel'],mode="lines+markers"))

    # fig.add_trace(go.Line(name = 'Delta Range (Temp effect)', x = sensordf['epoch'], y = sensordf['traveltime']*sensordf['deltavsound']*1e-4/2))
    # fig.add_trace(go.Line(name = 'Delta Range (Temp effect)', x = sensordf['epoch'], y = sensordf['pressure']))
    

    #Update layout 
    fig.update_layout(title_text = 'Tank water level',
            xaxis_title = 'time',
                      yaxis_title = 'height [cm]')
    
    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj


@login_required()
def dashboard(request):
    # retrieve the settings
    settings=TankConfig.objects.first()
    plotlyhtml=waterlevelPlot(settings.sounderheight) 
    return render(request,"dashboard.html",context={"content":plotlyhtml})
