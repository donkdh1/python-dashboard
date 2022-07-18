#!/usr/bin/env python
# coding: utf-8

# Trends in Number of COVID-19 and Vaccine - Visualization

### Call package
import pandas as pd
import numpy as np
import datetime

# visualization
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# route folder setting (your laptop's folder)
path = 'data/'

### Data
df = pd.read_csv(path + 'covid_vaccine.csv')
df.head()

# Dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

### file upload
# import io       # I/O(input/output)
# import base64   # decoding

# button setting
button = ['confirmed', 'deaths']
states = df['state'].unique()

# App structure
app = dash.Dash(__name__)
app.title = ('Dashboard | COVID-19 & Vaccines')
server = app.server

# App layout
app.layout = html.Div([
    # Title
    html.Div([html.H2('Trends in COVID-19 Cases and Vaccination in The United States', style={'textAlign': 'center'})]),
    
    # Dropdown - States
    html.Div([dcc.Dropdown(id = 'id_state',options=[{'label':i, 'value':i} for i in states],value = states[0])], style={'width':'200px'}),
    html.Br(),
    
    # Button - Confirmed, Deaths
    html.Div([dcc.RadioItems(id='id_covid', options=[{'label': i, 'value': i} for i in button], value = button[0])]),
    html.Br(),
    
    # Chart
    html.Div([dcc.Graph(id = 'graph', style={'height':650})]
            , style={'width': '95%', 'margin-left': 'auto', 'margin-right': 0})
])

@app.callback(Output('graph', 'figure'), 
              [Input('id_state', 'value'),
               Input('id_covid', 'value')])

# Define by input order = (1) state, (2) covid
def update_graph(stat, cov):
    
    # secondary y-axis setting,
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    
    # text - legend name & yaxis label
    if cov == 'confirmed':
        legend = 'Confirmed'
        ytitle = '<b>Number of Confirmed Cases</b>'
    else:
        legend = 'Deaths'
        ytitle = '<b>Number of Deaths Cases</b>'
    
    
    # Selecting the data
    df1 = df[df['state'] == stat]
    
    # primary Y : Covid-19
    fig.add_trace(go.Bar(x = df1['date'],
                         y = df1[cov],
                         name = legend,
                         hovertemplate = '%{y:,}',
                         marker_color='rgb(185,185,185)'),
                  secondary_y=False)
        
    fig.update_layout(go.Layout(xaxis = dict(title = 'Time (day)'),
                                yaxis = dict(title = ytitle, showgrid = False),
                                legend = dict(orientation='h', yanchor='top', y=1.1, traceorder='normal'),
                                hovermode = 'x unified',
                                plot_bgcolor='white'))
    
    
    # secondary Y : Fully Vaccine %
    fig.add_trace(go.Scatter(x = df1['date'],
                             y = df1['fully']/df1['population']*100,
                             name = 'Fully',
                             hovertemplate='%{y:,.1f}%',   # one decimal place
                             mode="lines",
                             line={'width':2.5}),
                  secondary_y=True)
    
    # secondary Y : At least one Vaccine %
    fig.add_trace(go.Scatter(x = df1['date'],
                             y = df1['at_least_one']/df1['population']*100,
                             name = 'At least 1',
                             hovertemplate='%{y:,.1f}%',   # one decimal place
                             mode="lines",
                             line={'width':2.5}),
                  secondary_y=True)
    
    # secondary_y axis : title, suffix
    fig.update_yaxes(title_text='<b>Series Complete (% of Population)</b>', 
                     ticksuffix = '%', 
                     range = [0, 100],
                     secondary_y=True)

    return fig

# Run App
if __name__=='__main__':
    app.run_server(debug=False)
