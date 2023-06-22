# app = dash.Dash(
#     __name__,
#     external_scripts=['https://cdn.tailwindcss.com'],
# )
from dash import Dash, dcc, html, Input, Output,callback, State
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
            dcc.Dropdown(['1','2','3'], id='column-1', placeholder="Please select the column"),className='dashboard_dropdown col-span-2'
            # html.Select(id='column-1', className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full h-full p-2.5',children=[
            #     html.Option(value='ko co gi',children="Select the value"),
            #     html.Option(value='1', children='1'),
            #     html.Option(value='2', children='2'),
            #     html.Option(value='3', children='3') 
            # ]),className='dashboard_dropdown'
            ),
        html.Div(
            dcc.Dropdown(['1','2','3'], id='column-2', placeholder="Please select the column"), className='dashboard_dropdown col-span-2'
            ),
        html.Div(className='dashboard_dropdown mr-2.5',children=[
            html.Button(className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800 w-full h-full", children=['Submit'],id='submit-button-state', n_clicks=0)
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
    
    dcc.Store(id='data-frame-store')
])
@callback(Output('data-frame-store', 'data'),
    Output('output-data-upload', 'children'),
          Output("column-1",'options'),
          Output("column-2",'options'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output_1_input(content, name, date):
    if content is not None:
        children, data = functions.parse_contents(content, name, date)
        columns = list(data.columns)
        dict_data = {column:data[column].to_list() for column in data.columns}
        return dict_data,children, columns, columns
    else:
        return None,html.Div("Please import the data"), list(),list()
@callback(
    Output('scatter-plot','children'),
    Output('histogram-plot','children'),
    Input('data-frame-store', 'data'),
    Input('submit-button-state', 'n_clicks'),
    State('column-1','value'),
    State('column-2', 'value')
)

def generate_plot(data,n_clicks,value1, value2):
    if value1 is not None:
        df = pd.DataFrame(data)
        scatter_figure = plot_functions.scatter_plot(df, value1, value2)
        histogram_figure = plot_functions.histogram_plot(df,value1)
        return scatter_figure, histogram_figure
    else:
        return None,None
if __name__ == "__main__":
    app.run_server(debug=True)
