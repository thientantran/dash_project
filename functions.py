from dash import html, dash_table, dcc
import pandas as pd
import base64
import io

def get_data_frame(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            return {"result": True, "data": df}
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return {"result": True, "data": df}
        else:
            return {"result": False, "data": "This file is incorrect format!"}
    except Exception as e:
        print(e)
        return {"result": False, "data": "There was an error processing this file."}
        
def parse_contents(contents, filename, date):
    output = get_data_frame(contents, filename)
    if output['result'] == True:
        df = output['data']
        return html.Div([
            # html.H5(filename),
            html.H5(f"There is {df.shape[0]} rows and {df.shape[1]} columns"),
            # html.H6(datetime.datetime.fromtimestamp(date)),

            dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns],
                page_size=5
            ),

            html.Hr(),  # horizontal line

            # For debugging, display the raw contents provided by the web browser
            # html.Div('Raw Content'),
            # html.Pre(contents[0:200] + '...', style={
            #     'whiteSpace': 'pre-wrap',
            #     'wordBreak': 'break-all'
            # })
        ]), df
    else:
        return html.Div(output['data']), pd.DataFrame()

def tranform_df_to_json(data):
    return {column:data[column].to_list() for column in data.columns}