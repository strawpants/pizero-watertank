

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from sensors.models import Range,Temperature, Pressure, Rain
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from django_pandas.io import read_frame
import numpy as np
from datetime import datetime,timedelta
from settings.models import TankConfig
import dash
from dash import dcc, html
from django_plotly_dash import DjangoDash
from django.utils import timezone 

speedofsoundconstant=340 #m/s
current_tz = timezone.get_current_timezone()
wc_color="#7bd5fe"

def initwaterlevelFig(settings):
    
    sounderHeight=settings.sounderheight;
    #get since last week
    since=datetime.now(timezone.utc)-timedelta(days=2)
    qry=Range.objects.filter(time__gte=since)
    sensordf=read_frame(qry)
    # breakpoint()
    sensordf["time"]=sensordf["time"].dt.tz_convert(current_tz.key)
    # sensordf['vsound']=20.05*(273.16 + sensordf['temperature']).apply(np.sqrt)
    # sensordf['deltavsound']=speedofsoundconstant-20.05*(273.16 + sensordf['temperature']).apply(np.sqrt)
    # sensordf['waterlevel']= sounderHeight*1e2-sensordf['traveltime']*sensordf['vsound']*1e-4/2
    fig=go.Figure()
    fig.add_trace(go.Line(name = 'Range', x = sensordf['time'], y = sounderHeight*1e2-sensordf['traveltime']*speedofsoundconstant*1e-4/2,mode="lines+markers",line_color=wc_color))
    #add overflow and minimum lines
    fig.add_hrect(y0=settings.normalzone*1e2, y1=settings.sounderheight*1e2, fillcolor="salmon", opacity=0.1)
    
    fig.add_hrect(y0=0, y1=settings.deadzone*1e2, fillcolor="salmon", opacity=0.1)

    #Update layout 
    fig.update_layout(title_text = 'Tank water level',
            xaxis_title = 'time',
            yaxis_title = 'height [cm]',template="plotly_dark")
    
    return fig

def initPressureTempFig():
    
    #get since last week
    since=datetime.now(timezone.utc)-timedelta(days=2)
    qryP=Pressure.objects.filter(time__gte=since)
    sensordf=read_frame(qryP)
    sensordf["time"]=sensordf["time"].dt.tz_convert(current_tz.key)



    # fig=go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    sensordf.pressure.where(sensordf.pressure < 2000,inplace=True)
    fig.add_trace(go.Line(name = 'Pressure', x = sensordf['time'], y = sensordf['pressure'],line_color=wc_color))
     
    #also add temperature data 
    qryT=Temperature.objects.filter(time__gte=since)
    sensorTdf=read_frame(qryT)
    sensorTdf["time"]=sensorTdf["time"].dt.tz_convert(current_tz.key)
    fig.add_trace(go.Line(name = 'Temperature', x = sensordf['time'], y = sensorTdf['temperature'],line_color="salmon"),secondary_y=True)
    

    #Update layout 
    fig.update_layout(title_text = 'Atmospheric pressure and temperature at sensor head',
            xaxis_title = 'time',
            yaxis_title = 'Pressure [hPa]',template="plotly_dark")
    
    fig.update_yaxes(title_text="Temperature [&deg;C]", secondary_y=True)

    return fig

def initRainFig(settings):
    
    mmtip=settings.mmtip
    since=datetime.now(timezone.utc)-timedelta(days=15)
    qryR=Rain.objects.filter(time__gte=since)
    sensordf=read_frame(qryR)
    sensordf["time"]=sensordf["time"].dt.tz_convert(current_tz.key)
    sensordf.validflag.where(sensordf.validflag == 1,inplace=True)
    sensordf["rain_accum"]=sensordf['validflag'].cumsum()*mmtip

    # Construct get the rain rate
    rainrate=3600*sensordf.rain_accum.diff()/(sensordf.time.diff().dt.total_seconds())
    timerate=sensordf.time-sensordf.time.diff()/2
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Line(name = 'Rain accumulated', x = sensordf.time, y = sensordf.rain_accum,line_color=wc_color))
    
    fig.add_trace(go.Bar(name = 'Rain rate', x = timerate, y = rainrate),secondary_y=True)
     
    #Update layout 
    fig.update_layout(title_text = 'Accumulated rain since',
            xaxis_title = 'time',
            yaxis_title = 'Rain [mm/m2]',template="plotly_dark")
    
    fig.update_yaxes(title_text="Rain rate [mm/m2/hour]", secondary_y=True)
    

    return fig



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


app_wl = DjangoDash('TankLevel')  


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



@login_required()
def dashboard(request):
    # get settings
    
    settings=TankConfig.objects 
    if settings.count() == 0:
        settings=TankConfig()
    else:
        settings=settings.first()

    app_wl.layout = html.Div([
        dcc.Graph(figure=initwaterlevelFig(settings),id='water-level-data', responsive=True),
        dcc.Graph(figure=initPressureTempFig(),id='pres-temp-data', responsive=True),
        dcc.Graph(figure=initRainFig(settings),id='rain-data', responsive=True)],
        id="wc_app")
    return render(request,"dashboard.html")
#return render(request,"dashboard.html",context={"content":plotlyhtml})
