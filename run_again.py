from dash import Dash, dcc, html, Input, Output, State, callback

import functions
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        # multiple=True
    ),
    html.Div(id='output-data-upload'),
])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        # children = [
        #     functions.parse_contents(c, n, d) for c, n, d in
        #     zip(list_of_contents, list_of_names, list_of_dates)]
        children = functions.parse_contents(list_of_contents, list_of_names, list_of_dates)
        return children

if __name__ == '__main__':
    app.run_server(debug=True)
