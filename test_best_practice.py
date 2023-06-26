# app = dash.Dash(
#     __name__,
#     external_scripts=['https://cdn.tailwindcss.com'],
# )
from dash import Dash, dcc, html, Input, Output,callback, State, dash_table
from dash.exceptions import PreventUpdate
import functions
import plot_functions
import pandas as pd
import plotly.express as px
app = Dash(__name__, external_scripts=['https://cdn.tailwindcss.com', '/assets/style.css'])

app.layout = html.Div([
    html.Header(children=[
        html.Nav(children=[
            html.Div(children=[
                html.A(children=[
                    html.Span(children="MICROBIOME TEAM", className="self-center text-xl font-semibold whitespace-nowrap dark:text-white")
                    ],href="https://github.com/thientantran", className='flex items-center',),
                html.Div(children='DASHBOARD', className = "inline-block dark:text-white text-xl")
            ], className="flex items-center justify-between"),
        ], className='bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-gray-800')
    ]),
    html.Div(className='grid grid-cols-9 gap-4',children=[
        html.Div(className='col-span-4',children=
            dcc.Upload(
            className='dashboard_upload',
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files',className='font-bold cursor-pointer')
            ]),
        # Allow multiple files to be uploaded
        # multiple=True
    )),
        html.Div(
            dcc.Dropdown(id='column-1', placeholder="Please choose dependent variable"),className='dashboard_dropdown col-span-2'
            # html.Select(id='column-1', className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full h-full p-2.5',children=[
            #     html.Option(value='ko co gi',children="Select the value"),
            #     html.Option(value='1', children='1'),
            #     html.Option(value='2', children='2'),
            #     html.Option(value='3', children='3') 
            # ]),className='dashboard_dropdown'
            ),
        html.Div(
            dcc.Dropdown(id='column-2', placeholder="Please choose independent variable"), className='dashboard_dropdown col-span-2'
            ),
        html.Div(className='dashboard_dropdown mr-2.5',children=[
            html.Button(className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800 w-full h-full", children=['Submit'],id='submit-button-state', n_clicks=0)
        ])
        
    ]),
    html.Div([
        html.Div(id='output-data-upload'),
        html.Div(className='grid grid-cols-2 gap-x-3',children=[
            html.Div(id='scatter-plot'),
            html.Div(id='histogram-plot')
            ]),
        html.Div(id='output'),
    ], style={"margin":'10px'}),
    
    dcc.Store(id='data_on_app'),
    dcc.Store(id='local', storage_type='local')
])

@callback(
    Output('local', 'data', allow_duplicate=True),
    Output('column-1','value', allow_duplicate=True),
    Output('column-2', 'value', allow_duplicate=True),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    prevent_initial_call=True
)
def get_data_to_local(content, name, date):
    if content is None:
        raise PreventUpdate
    children, data = functions.parse_contents(content, name, date)
    dict_data = functions.tranform_df_to_json(data)
    return {'data':dict_data, 'filename':name, 'date_of_file':date, 'value1': None, 'value2':None},None, None

@callback(
    Output("local","data"),
    Input('data_on_app', 'data'),
    Input('submit-button-state', 'n_clicks'),
    State('column-1','value'),
    State('column-2', 'value'),
)
def upload_value_to_local(data, n_clicks,value1, value2):
    if value1 is not None:
        data['value1'] = value1
        data['value2'] = value2
    return data

@callback(
    Output('data_on_app', 'data'),
    Input("local",'modified_timestamp'),
    State("local",'data'),
)
def get_data_to_app(ts, data):
    if ts is None:
        raise PreventUpdate
    return data

@callback(
    Output('output-data-upload', 'children'),
    Output("column-1",'options'),
    Output("column-2",'options'),
    Output("column-1",'value'),
    Output("column-2",'value'),
    Input('data_on_app', 'data')
)
def update_tabel_and_columns(data):
    if data is not None:
        df = pd.DataFrame(data['data'])
        children =  functions.transform_to_table(df)
        columns = list(df.columns)
        return children, columns, columns, data['value1'], data['value2']
    else:
        return html.Div("Please import the data"), list(),list(), None, None

@callback(
    Output('scatter-plot','children'),
    Output('histogram-plot','children'),
    Input('data_on_app', 'data')
)

def generate_plot(data):
    if data is not None:
        value1 = data['value1']
        value2 = data['value2']
        if value1 is not None:
            df = pd.DataFrame(data['data'])
            if value2 is not None:
                scatter_figure = plot_functions.scatter_plot(df, value2, value1)
            else:
                scatter_figure = plot_functions.scatter_plot(df, value1, value1)
            histogram_figure = plot_functions.histogram_plot(df,value1)
            return scatter_figure, histogram_figure
        else:
            return None,None
    else:
        return None, None


if __name__ == "__main__":
    app.run_server(debug=True, port=8050, threaded=True)
