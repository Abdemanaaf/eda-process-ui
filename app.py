import dash
import time

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from pathlib import Path

import pandas as pd

from dash.dependencies import Input, Output, State

from layouts.dashboard_layout import dashboard_layout
from layouts.eda_layout import eda_layout
from layouts.sneek_peek_layout import get_sneek_peek_layout
from layouts.add_func_layout import add_func_layout
from layouts.output_layout import output_layout
from layouts.nav_layout import left_side_nav_layout, top_navbar_layout

from src.utils import parse_contents
from src.config import config

external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {
        'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM',
        'crossorigin': 'anonymous'
    }
]

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC',
        'crossorigin': 'anonymous'
    },
    dbc.themes.BOOTSTRAP
]

app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    title='Ease EDA'
)

app.config.suppress_callback_exceptions = True

server = app.server


INPUT_TABLE_ROWS_LIST = []
MAPPING_TABLE_ROWS_LIST = []

FUNCTION_NUMBER = 0
FUNCTION_LIST = {
    'add_new_row': html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H1(['00'],
                            style={'font-size': '60px'}
                        )
                    ], style={'margin': 'auto auto'})
                ], width=2, className='ml-5'),

                dbc.Col([
                    html.H3(['Input File']),
                    html.Hr(style={'width': '70%'}),
                    html.H4(['EDA Process Name: --NA--']),
                    html.H4(['File Name: --NA--']),
                    html.H4(['Number of Columns: --NA--']),
                    html.H4(['Inplace (True/False): --NA--'])
                ], className='mt-4 mb-4'),

                dbc.Col([
                    html.H3(['Mapping File']),
                    html.Hr(style={'width': '70%'}),
                    html.H4(['EDA Process Name: --NA--']),
                    html.H4(['File Name: --NA--']),
                    html.H4(['Number of Columns: --NA--']),
                    html.H4(['Inplace (True/False): --NA--'])
                ], className='mt-4 mb-4')
            ])
        ],
        style={
            'width': '100%', 'height': 'auto', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'solid',
            'borderRadius': '10px', 'margin': '0 auto', 'background-color': 'white'
        }
    )
}

NEW_FUNCTION_ADDED = False
NEW_PROCESS_DICTIONARY = {}
ALL_PROCESS_LIST = []

FUNCTION_EXEC_LIST = []


app.layout = html.Div([
    dcc.Location(id='route_url', refresh=False),

    dbc.Row([
        dbc.Col([top_navbar_layout])
    ], className='mb-5'),

    dbc.Container([
        dbc.Row([
            dbc.Col([], width=1),
            dbc.Col([left_side_nav_layout], width=2),
            dbc.Col([html.Div(id='page_content')], width=8),
            dbc.Col([], width=1)
        ], className='mt-5, mr-5')
    ], fluid=True, className='mr-5 ml-5')
], style={'background-color': '#e2eee5', 'height': '120vh'})


@app.callback(
    [
        Output('output-mapping-data', 'children'),
        Output('clear_mapping_btn_div', 'children')
    ],
    [
        Input('upload-mapping-data', 'contents'),
        Input('clear_mapping_table', 'n_clicks')
    ],
    [
        State('upload-mapping-data', 'filename'),
        State('upload-mapping-data', 'last_modified')
    ]
)
def update_mapping_table(list_of_contents, nclicks, list_of_names, list_of_dates):
    global MAPPING_TABLE_ROWS_LIST

    table_header = [
        html.Thead(html.Tr([
            html.Th('Sr. No.', style={'textAlign': 'center'}),
            html.Th('File Name', style={'textAlign': 'center'}),
            html.Th('Date Uploaded', style={'textAlign': 'center'}),
            html.Th('Content Type', style={'textAlign': 'center'}),
            html.Th('File Type', style={'textAlign': 'center'}),
            html.Th('Sneek Peek', style={'textAlign': 'center'}),
        ], style={'font-size': '1.4rem', 'font-style': 'italic', 'font-weight': 'bold'}))
    ]

    btn_obj = dbc.Button(
        'Clear Table', color='warning', className='mr-1', id='clear_mapping_table', n_clicks=0, style={'height': 'auto'}
    )

    table_rows = []

    if list_of_contents is not None:
        for sr_no, contents, filename, date in zip(
            list(range(len(list_of_contents))), list_of_contents, list_of_names, list_of_dates
        ):
            MAPPING_TABLE_ROWS_LIST.append(parse_contents(contents, filename, date))

            MAPPING_TABLE_ROWS_LIST[sr_no][2].to_csv(Path('media/mapping_files/', filename), index=False)

            table_rows.append(html.Tr([
                html.Td(sr_no, style={'textAlign': 'center'}),
                html.Td(MAPPING_TABLE_ROWS_LIST[sr_no][0], style={'textAlign': 'center'}),
                html.Td(MAPPING_TABLE_ROWS_LIST[sr_no][1], style={'textAlign': 'center'}),
                html.Td(MAPPING_TABLE_ROWS_LIST[sr_no][3], style={'textAlign': 'center'}),
                html.Td(MAPPING_TABLE_ROWS_LIST[sr_no][4], style={'textAlign': 'center'}),
                html.Td(
                    dcc.Link(
                        dbc.Button('View File', color='success', style={'height': 'auto'}),
                        href=f'/dashboard/mapping/{MAPPING_TABLE_ROWS_LIST[sr_no][0]}/{MAPPING_TABLE_ROWS_LIST[sr_no][4]}'
                    ),
                    style={'textAlign': 'center'}
                ),
            ], style={'font-size': '1.2rem'}))
    else:
        if MAPPING_TABLE_ROWS_LIST == []:
            table_rows.append(html.Tr([
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
            ], style={'font-size': '1.2rem'}))
        else:
            for row in range(len(MAPPING_TABLE_ROWS_LIST)):
                table_rows.append(html.Tr([
                    html.Td(row, style={'textAlign': 'center'}),
                    html.Td(MAPPING_TABLE_ROWS_LIST[row][0], style={'textAlign': 'center'}),
                    html.Td(MAPPING_TABLE_ROWS_LIST[row][1], style={'textAlign': 'center'}),
                    html.Td(MAPPING_TABLE_ROWS_LIST[row][3], style={'textAlign': 'center'}),
                    html.Td(MAPPING_TABLE_ROWS_LIST[row][4], style={'textAlign': 'center'}),
                    html.Td(
                        dcc.Link(
                            dbc.Button('View File', color='success', style={'height': 'auto'}),
                            href=f'/dashboard/mapping/{MAPPING_TABLE_ROWS_LIST[row][0]}/{MAPPING_TABLE_ROWS_LIST[row][4]}'
                        ),
                        style={'textAlign': 'center'}
                    ),
                ], style={'font-size': '1.2rem'}))

    if nclicks != 0:
        btn_obj = dbc.Button(
            'Clear Table', color='warning', className='mr-1', id='clear_mapping_table', n_clicks=0, style={'height': 'auto'}
        )

        MAPPING_TABLE_ROWS_LIST = []

        table_rows = [
            html.Tr([
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
            ], style={'font-size': '1.2rem'})
        ]

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(
        table_header + table_body,
        bordered=True, dark=False, hover=True, responsive=True, striped=True,
        id='data_table'
    )

    return table, btn_obj


@app.callback(
    [
        Output('output-input-data', 'children'),
        Output('clear_input_btn_div', 'children')
    ],
    [
        Input('upload-input-data', 'contents'),
        Input('clear_input_table', 'n_clicks')
    ],
    [
        State('upload-input-data', 'filename'),
        State('upload-input-data', 'last_modified')
    ]
)
def update_input_table(list_of_contents, nclicks, list_of_names, list_of_dates):
    global INPUT_TABLE_ROWS_LIST

    table_header = [
        html.Thead(html.Tr([
            html.Th('Sr. No.', style={'textAlign': 'center'}),
            html.Th('File Name', style={'textAlign': 'center'}),
            html.Th('Date Uploaded', style={'textAlign': 'center'}),
            html.Th('Content Type', style={'textAlign': 'center'}),
            html.Th('File Type', style={'textAlign': 'center'}),
            html.Th('Sneek Peek', style={'textAlign': 'center'}),
        ], style={'font-size': '1.4rem', 'font-style': 'italic', 'font-weight': 'bold'}))
    ]

    btn_obj = dbc.Button(
        'Clear Table', color='warning', className='mr-1', id='clear_input_table', n_clicks=0, style={'height': 'auto'}
    )

    table_rows = []

    if list_of_contents is not None:
        for sr_no, contents, filename, date in zip(
            list(range(len(list_of_contents))), list_of_contents, list_of_names, list_of_dates
        ):
            INPUT_TABLE_ROWS_LIST.append(parse_contents(contents, filename, date))

            INPUT_TABLE_ROWS_LIST[sr_no][2].to_csv(Path('media/csv_files/', filename), index=False)

            table_rows.append(html.Tr([
                html.Td(sr_no, style={'textAlign': 'center'}),
                html.Td(INPUT_TABLE_ROWS_LIST[sr_no][0], style={'textAlign': 'center'}),
                html.Td(INPUT_TABLE_ROWS_LIST[sr_no][1], style={'textAlign': 'center'}),
                html.Td(INPUT_TABLE_ROWS_LIST[sr_no][3], style={'textAlign': 'center'}),
                html.Td(INPUT_TABLE_ROWS_LIST[sr_no][4], style={'textAlign': 'center'}),
                html.Td(
                    dcc.Link(
                        dbc.Button('View File', color='success', style={'height': 'auto'}),
                        href=f'/dashboard/input/{INPUT_TABLE_ROWS_LIST[sr_no][0]}/{INPUT_TABLE_ROWS_LIST[sr_no][4]}'
                    ),
                    style={'textAlign': 'center'}
                ),
            ], style={'font-size': '1.2rem'}))

    else:
        if INPUT_TABLE_ROWS_LIST == []:
            table_rows.append(html.Tr([
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
            ], style={'font-size': '1.2rem'}))
        else:
            for row in range(len(INPUT_TABLE_ROWS_LIST)):
                table_rows.append(html.Tr([
                    html.Td(row, style={'textAlign': 'center'}),
                    html.Td(INPUT_TABLE_ROWS_LIST[row][0], style={'textAlign': 'center'}),
                    html.Td(INPUT_TABLE_ROWS_LIST[row][1], style={'textAlign': 'center'}),
                    html.Td(INPUT_TABLE_ROWS_LIST[row][3], style={'textAlign': 'center'}),
                    html.Td(INPUT_TABLE_ROWS_LIST[row][4], style={'textAlign': 'center'}),
                    html.Td(
                        dcc.Link(
                            dbc.Button('View File', color='success', style={'height': 'auto'}),
                            href=f'/dashboard/input/{INPUT_TABLE_ROWS_LIST[row][0]}/{INPUT_TABLE_ROWS_LIST[row][4]}'
                        ),
                        style={'textAlign': 'center'}
                    ),
                ], style={'font-size': '1.2rem'}))

    if nclicks != 0:
        btn_obj = dbc.Button(
            'Clear Table', color='warning', className='mr-1', id='clear_input_table', n_clicks=0, style={'height': 'auto'}
        )

        INPUT_TABLE_ROWS_LIST = []

        table_rows = [
            html.Tr([
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
                html.Td('Empty Cell', style={'textAlign': 'center'}),
            ], style={'font-size': '1.2rem'})
        ]

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(
        table_header + table_body,
        bordered=True, dark=False, hover=True, responsive=True, striped=True,
        id='data_table'
    )

    return table, btn_obj


@app.callback(
    Output('page_content', 'children'),
    [
        Input('route_url', 'pathname'),
    ]
)
def change_layout_view(pathname):
    if '/eda-page' in pathname:
        return eda_layout

    elif '/dashboard' in pathname:
        file_category = pathname.split('/')[2]
        file_name = pathname.split('/')[3]
        ext = pathname.split('/')[4]

        if file_category == 'input':
            dataframe = pd.read_csv(f'media/csv_files/{file_name}.{ext}')
        else:
            dataframe = pd.read_csv(f'media/mapping_files/{file_name}.{ext}')

        return get_sneek_peek_layout(dataframe)

    elif '/add-function' in pathname:
        return add_func_layout

    elif '/output-page' in pathname:
        return output_layout

    return dashboard_layout


@app.callback(
   Output('df_name_input_div', 'style'),
    [
        Input('radioitems-input', 'value')
    ]
)
def show_hide_df_input(visibility_state):
    if visibility_state == 0:
        return {'display': 'block'}
    if visibility_state == 1:
        return {'display': 'none'}


@app.callback(
    [
        Output('eda_func_content', 'children'),
        Output('delete_func_btn_div', 'children'),
    ],
    [
        Input('route_url', 'pathname'),
        Input('delete_func', 'n_clicks'),
    ]
)
def add_new_func(pathname, nclicks_delete):
    global FUNCTION_NUMBER, FUNCTION_LIST, NEW_FUNCTION_ADDED, NEW_PROCESS_DICTIONARY, ALL_PROCESS_LIST
    delete_btn = dbc.Button('Delete Function', color='danger', className='mr-1', id='delete_func', n_clicks=0, style={'width': '80%'})

    if '/eda-page/func-added' in pathname and NEW_FUNCTION_ADDED:
        NEW_FUNCTION_ADDED = False
        FUNCTION_NUMBER += 1

        file_name = NEW_PROCESS_DICTIONARY['dataframe_path'].split('\\')[1].split('.')[0]
        eda_process = NEW_PROCESS_DICTIONARY['eda_process']
        column_list = ', '.join(NEW_PROCESS_DICTIONARY['column_list'])

        column_len = 0
        if 'All Columns' in NEW_PROCESS_DICTIONARY['column_list']:
            df = pd.read_csv(NEW_PROCESS_DICTIONARY['dataframe_path'])
            column_len = str(len(df.columns)) + ' (All)'
        else:
            column_len = len(NEW_PROCESS_DICTIONARY['column_list'])

        if eda_process in ['Drop NA Values', 'Drop Duplicate Values']:

            new_func = html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H1([f'{str(FUNCTION_NUMBER).zfill(2)}'],
                                style={'font-size': '60px'}
                            )
                        ], style={'margin': 'auto auto'})
                    ], width=2, className='ml-5'),

                    dbc.Col([
                        html.H3(['Input File']),
                        html.Hr(style={'width': '70%'}),
                        html.H4([f'EDA Process Name: {eda_process}']),
                        html.H4([f'File Name: {file_name}']),
                        html.H4([f'Number of Columns: {column_len}']),
                        html.H4([f'Inplace (True/False): {bool(NEW_PROCESS_DICTIONARY["inplace_bool"])}'])
                    ], className='mt-4 mb-4'),

                    dbc.Col([
                        html.H3(['Mapping File']),
                        html.Hr(style={'width': '70%'}),
                        html.H4([f'EDA Process Name: --NA--']),
                        html.H4([f'File Name: --NA--']),
                        html.H4([f'Number of Columns: --NA--']),
                        html.H4([f'Inplace (True/False): --NA--'])
                    ], className='mt-4 mb-4')
                ])
            ],
            style={
                'width': '100%', 'height': 'auto', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'solid',
                'borderRadius': '10px', 'margin': '0 auto', 'background-color': 'white'
            },
            className='mt-5'
        )

            FUNCTION_LIST[f'function-{FUNCTION_NUMBER}'] = new_func
        ALL_PROCESS_LIST.append(NEW_PROCESS_DICTIONARY)

    if nclicks_delete != 0:
        delete_btn = dbc.Button('Delete Function', color='danger', className='mr-1', id='delete_func', n_clicks=0, style={'width': '80%'})

        del FUNCTION_LIST[f'function-{FUNCTION_NUMBER}']

        FUNCTION_NUMBER -= 1

    if FUNCTION_NUMBER > 0:
        return list(FUNCTION_LIST.values())[1:], delete_btn

    return list(FUNCTION_LIST.values()), delete_btn


@app.callback(
    Output('update_bool', 'children'),
    [
        Input('submit_func_to_list', 'n_clicks'),
        Input('radioitems-input', 'value'),
        Input('select', 'value'),
        Input('select_eda_process', 'value'),
        Input('select_columns', 'value'),
    ]
)
def update_func_bool(nclicks_input, new_df_bool, select_df, process_select, cols_list):
    global NEW_FUNCTION_ADDED, NEW_PROCESS_DICTIONARY
    NEW_FUNCTION_ADDED = True

    new_func_process_dict = {
        'dataframe_path': select_df,
        'eda_process': process_select,
        'column_list': cols_list,
        'inplace_bool': new_df_bool
    }

    NEW_PROCESS_DICTIONARY = new_func_process_dict

    return nclicks_input


@app.callback(
    [
        Output('select_columns_div', 'children'),
    ],
    [
        Input('select', 'value'),
    ]
)
def select_dataframe(select_df_value):

    if select_df_value is not None:
        dataframe = pd.read_csv(select_df_value)

        select_columns = dcc.Dropdown(
            id="select_columns",
            options=[{'label':'All Columns', 'value': 'All Columns'}] + [{'label': label, 'value': label} for label in list(dataframe.columns)],
            value=['All Columns'],
            multi=True
        )
    else:
        select_columns = dcc.Dropdown(
            id="select_columns",
            options=[{'label':'---Select Dataframe', 'value': 'NA'}],
            multi=True
        )

        return [html.Div(['Select Columns (Subset)', select_columns])]

    return [html.Div(['Select Columns (Subset)', select_columns])]


@app.callback(
    [
        Output('loading-output', 'children'),
        Output('exec_func_btn_div', 'children'),
        Output('check_output', 'disabled')
    ],
    [
        Input('exec_func_list', 'n_clicks')
    ]
)
def execute_process_list(nclicks):
    global ALL_PROCESS_LIST, FUNCTION_EXEC_LIST

    print(ALL_PROCESS_LIST)

    exec_btn = dbc.Button('Execute Functions', color='light', className='mr-1', id='exec_func_list', n_clicks=0)

    badge_obj_success = dbc.Badge("Success", pill=True, color="success", className="mt-3", id='success_badge', style={'display': 'block', 'width': '40%'})
    badge_obj_info = dbc.Badge("Not Executed", pill=True, color="info", className="mt-3", id='info_badge', style={'display': 'block', 'width': '40%'})

    FUNCTION_EXEC_LIST = []
    for process in ALL_PROCESS_LIST:
        func = config['process_function_mapping'][process['eda_process']]

        FUNCTION_EXEC_LIST.append(func(
            process['dataframe_path'],
            process['column_list'],
            process['inplace_bool'],
            'random_file_name',
        ))

    if nclicks != 0:
        time.sleep(2)
        return [badge_obj_success], exec_btn, False
    else:
        return [badge_obj_info], exec_btn, True


@app.callback(
    Output('output_div', 'children'),
    Input('output_div', 'children')
)
def show_output(output_div_children):
    print(FUNCTION_EXEC_LIST)
    return 'FUNCTION_EXEC_LIST'


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8099)