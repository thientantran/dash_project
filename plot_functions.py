from dash import html, dcc
import pandas as pd

import plotly.express as px

def scatter_plot(df, value1, value2):
    fig =px.scatter(df, x=value1, y=value2)
    return dcc.Graph(figure=fig)

def histogram_plot(df, value):
    fig = px.histogram(df, x=value)
    return dcc.Graph(figure=fig)