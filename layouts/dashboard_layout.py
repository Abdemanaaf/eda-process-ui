import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

dashboard_layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.P(['Upload Input File & Preview Table']),
                html.P(['File Types Allowed - xlsx, csv']),

                dcc.Upload(
                    children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                    id='upload-input-data',
                    style={
                        'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed',
                        'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                    },
                    multiple=True
                ),

                html.Div(id='output-input-data'),

                html.Div([
                    dbc.Button('Clear Table', color='light', className='mr-1', id='clear_input_table', n_clicks=0),
                ], id='clear_input_btn_div'),

                html.P(['Upload Mapping File & Preview Table']),
                html.P(['File Types Allowed - xlsx, csv']),

                dcc.Upload(
                    children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                    id='upload-mapping-data',
                    style={
                        'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed',
                        'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                    },
                    multiple=True
                ),

                html.Div(id='output-mapping-data'),

                html.Div([
                    dbc.Button('Clear Table', color='light', className='mr-1', id='clear_mapping_table', n_clicks=0),
                ], id='clear_mapping_btn_div'),

                html.Div([
                    dcc.Link(
                        dbc.Button('Submit and Move Ahead to EDA', color='light', className='mr-1', id='submit_move_eda'),
                        href='/eda-page'
                    ),
                ]),
            ])
        ])
    ])
], className='container-fluid')