import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

eda_layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Link(
                            dbc.Button('Add New Function', color='success', className='mr-1', id='add_func', n_clicks=0, style={'width': '80%'}),
                            href='/add-function'
                        ),
                    ], id='add_func_btn_div', style={'margin': '0 auto', 'textAlign': 'center'}),
                ], width=6),

                dbc.Col([
                    html.Div([
                        dbc.Button('Delete Function', color='danger', className='mr-1', id='delete_func', n_clicks=0, style={'width': '80%'}),
                    ], id='delete_func_btn_div', style={'margin': '0 auto', 'textAlign': 'center'}),
                ], width=6),

            ], className='mb-5 mt-3'),

            html.Hr(className='mb-5', style={'width': '70%', 'margin': '0 auto'}),

            html.Div([
                html.Div([],
                style={
                    'width': '100%', 'height': 'auto', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'solid',
                    'borderRadius': '5px', 'margin': '0 auto'
                })
            ], id='eda_func_content', className='mb-5'),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Button('Execute Functions', color='light', className='mr-1', id='exec_func_list', n_clicks=0),
                    ], id='exec_func_btn_div', style={'margin': '0 auto', 'textAlign': 'center'}),

                    html.Div([
                        dbc.Spinner(html.Div(id="loading-output", style={'margin': '0 auto', 'textAlign': 'center'})),
                    ], style={'margin': '0 auto', 'textAlign': 'center'}),
                ], width=6),

                dbc.Col([
                    html.Div([
                        dcc.Link(
                            dbc.Button('Check Output >>>', color='secondary', className='mr-1', id='check_output', n_clicks=0, disabled=True),
                            href='/output-page'
                        )
                    ], id='check_output_btn_div', style={'margin': '0 auto', 'textAlign': 'center'}),
                ], width=6),
            ], className='mb-5 mt-3'),
        ])
    ])
], className='container-fluid')