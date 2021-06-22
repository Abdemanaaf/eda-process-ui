import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

eda_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button('Delete Function', color='light', className='mr-1', id='delete_func', n_clicks=0),
            ], id='delete_func_btn_div'),

            html.Div([
                html.Div([
                    html.Div([
                        dcc.Link(
                            dbc.Button('Add New Function', color='light', className='mr-1', id='add_func', n_clicks=0),
                            href='/add-function'
                        ),
                    ], id='add_func_btn_div'),
                ],
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed',
                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                })
            ], id='eda_func_content'),

            html.Div([
                dbc.Button('Execute Functions', color='light', className='mr-1', id='exec_func_list', n_clicks=0),
            ], id='exec_func_btn_div'),

            dbc.Spinner(html.Div(id="loading-output")),

            html.Div([
                dcc.Link(
                    dbc.Button('Check Output', color='light', className='mr-1', id='check_output', n_clicks=0, disabled=True),
                    href='/output-page'
                )
            ], id='check_output_btn_div'),
        ])
    ])
], className='container-fluid')