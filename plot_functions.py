from dash import html, dcc
import pandas as pd

import plotly.express as px

def scatter_plot(df, value1, value2):
    fig =px.scatter(df, x=value1, y=value2)
    return html.Div(children=[html.H1(['Scatter Plot'], className='text-center'), dcc.Graph(figure=fig)],className='shadow-xl mt-2.5 border rounded-lg')

def histogram_plot(df, value):
    fig = px.histogram(df, x=value)
    return html.Div(children=[html.H1(['Histogram Plot'], className='text-center'), dcc.Graph(figure=fig)],className='shadow-xl mt-2.5 border rounded-lg')