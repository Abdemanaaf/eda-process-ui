from dash_bootstrap_components._components.Card import Card
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

input_upload_div = html.Div([
    html.Div([
        html.H2(['Upload Input File & Preview Table']),
        html.H6(['File Types Allowed - ', html.Strong('xlsx, csv')], className='mb-4'),
    ], style={'textAlign': 'center'}),

    html.Div([
        dcc.Upload(
            children=html.Div([
                html.Img(
                    src='/assets/images/R7d175e02479c6d8044f9345fdb606826.png',
                    style={'height':'10%', 'width':'10%'},
                    className='mt-5 mb-2'
                ),
                html.P('Select Input Files or Drag here', style={'font-size': '1.3rem'}),
                html.A(dbc.Button('Select Files', color='secondary', className='mr-1 mb-5')),
            ]),
            id='upload-input-data',
            multiple=True
        ),
    ],
    style={
        'width': '85%', 'height': 'auto', 'borderWidth': '2px', 'borderStyle': 'solid', 'borderColor': 'grey',
        'borderRadius': '4px', 'textAlign': 'center', 'margin': '0 auto', 'background-color': '#FDFDFC'
    }, className='mb-5'),
])


mapping_upload_div = html.Div([
    html.Div([
        html.H2(['Upload Mapping File & Preview Table']),
        html.H6(['File Types Allowed - ', html.Strong('xlsx, csv')], className='mb-4'),
    ], style={'textAlign': 'center'}),

    html.Div([
        dcc.Upload(
            children=html.Div([
                html.Img(
                    src='/assets/images/R7d175e02479c6d8044f9345fdb606826.png',
                    style={'height':'10%', 'width':'10%'},
                    className='mt-5 mb-2'
                ),
                html.P('Select Mapping Files or Drag here', style={'font-size': '1.3rem'}),
                html.A(dbc.Button('Select Files', color='secondary', className='mr-1 mb-5')),
            ]),
            id='upload-mapping-data',
            multiple=True
        ),
    ],
    style={
        'width': '85%', 'height': 'auto', 'borderWidth': '2px', 'borderStyle': 'solid', 'borderColor': 'grey',
        'borderRadius': '4px', 'textAlign': 'center', 'margin': '0 auto', 'background-color': '#FDFDFC'
    }, className='mb-5'),
])


dashboard_layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([input_upload_div]),
                    dbc.Col([mapping_upload_div])
                ]),

                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col(['Input Files Table']),
                            dbc.Col([
                                html.Div([
                                    dbc.Button(
                                        'Clear Table', color='warning', className='mr-1',
                                        id='clear_input_table', n_clicks=0, style={'height': 'auto'}
                                    ),
                                ], id='clear_input_btn_div', className='text-right')
                            ]),
                            dbc.Col([], width=1),
                        ]),
                    ], style={'font-size': '1.5rem'}),
                    dbc.CardBody([html.Div(id='output-input-data')])
                ], color="light", className="w-100 mb-3 mt-3"),

                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col(['Mapping Files Table']),
                            dbc.Col([
                                html.Div([
                                    dbc.Button(
                                        'Clear Table', color='warning', className='mr-1',
                                        id='clear_mapping_table', n_clicks=0, style={'height': 'auto'}
                                    ),
                                ], id='clear_mapping_btn_div', className='text-right')
                            ]),
                            dbc.Col([], width=1),
                        ]),
                    ], style={'font-size': '1.5rem'}),
                    dbc.CardBody([html.Div(id='output-mapping-data')])
                ], color="light", inverse=False, className="w-100 mb-3 mt-5"),

                html.Div([
                    dcc.Link(
                        dbc.Button('Submit and Move Ahead to EDA', color='secondary', className='mr-1', id='submit_move_eda'),
                        href='/eda-page'
                    ),
                ], className='mt-4 text-right'),
            ])
        ])
    ])
], className='container-fluid')