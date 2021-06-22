import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_table

def get_sneek_peek_layout(dataframe):
    sneek_peek_layout = html.Div([
        html.Div([
            # html.H5(filename),
            # html.H6(datetime.datetime.fromtimestamp(date)),

            dash_table.DataTable(
                data=dataframe.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in dataframe.columns]
            ),

            html.Div('Raw Content'),
            # html.Pre(contents[0:200] + '...', style={
            #     'whiteSpace': 'pre-wrap',
            #     'wordBreak': 'break-all'
            # })
        ])
    ], className='container-fluid')

    return sneek_peek_layout