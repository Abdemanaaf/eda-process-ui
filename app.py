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
    'add_new_row': html.Div(
        [
            dcc.Link(
                dbc.Button('Add New Function', color='light', className='mr-1', id='add_func', n_clicks=0),
                href='/add-function'
            ),
        ],
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        }
    )
}

NEW_FUNCTION_ADDED = False
NEW_PROCESS_DICTIONARY = {}
ALL_PROCESS_LIST = []


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
], style={'background-color': '#e2eee5', 'height': '100vh'})


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
            html.Th('Sr.No.'),
            html.Th('File Name'),
            html.Th('Date Uploaded'),
            html.Th('Content Type'),
            html.Th('File Type'),
            html.Th('Sneek Peek'),
        ]))
    ]

    btn_obj = dbc.Button('Clear Table', color='light', className='mr-1', id='clear_mapping_table', n_clicks=0)

    table_rows = []

    if list_of_contents is not None:
        for sr_no, contents, filename, date in zip(list(range(len(list_of_contents))), list_of_contents, list_of_names, list_of_dates):
            MAPPING_TABLE_ROWS_LIST.append(parse_contents(contents, filename, date))

            MAPPING_TABLE_ROWS_LIST[sr_no][2].to_csv(Path('media/mapping_files/', filename), index=False)

            table_rows.append(html.Tr([
                html.Td(sr_no),
                html.Td(MAPPING_TABLE_ROWS_LIST[sr_no][0]),
                html.Td(MAPPING_TABLE_ROWS_LIST[sr_no][1]),
                html.Td(MAPPING_TABLE_ROWS_LIST[sr_no][3]),
                html.Td(MAPPING_TABLE_ROWS_LIST[sr_no][4]),
                html.Td(
                    dcc.Link(dbc.Button('View File', color='success'), href=f'/dashboard/{MAPPING_TABLE_ROWS_LIST[sr_no][0]}/{MAPPING_TABLE_ROWS_LIST[sr_no][4]}')
                ),
            ]))
    else:
        if MAPPING_TABLE_ROWS_LIST == []:
            table_rows.append(html.Tr([
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
            ]))
        else:
            for row in range(len(MAPPING_TABLE_ROWS_LIST)):
                table_rows.append(html.Tr([
                    html.Td(row),
                    html.Td(MAPPING_TABLE_ROWS_LIST[row][0]),
                    html.Td(MAPPING_TABLE_ROWS_LIST[row][1]),
                    html.Td(MAPPING_TABLE_ROWS_LIST[row][3]),
                    html.Td(MAPPING_TABLE_ROWS_LIST[row][4]),
                    html.Td(
                        dcc.Link(dbc.Button('View File', color='success'), href=f'/dashboard/{MAPPING_TABLE_ROWS_LIST[row][0]}/{MAPPING_TABLE_ROWS_LIST[row][4]}')
                    ),
                ]))

    if nclicks != 0:
        btn_obj = dbc.Button('Clear Table', color='light', className='mr-1', id='clear_mapping_table', n_clicks=0)

        MAPPING_TABLE_ROWS_LIST = []

        table_rows = [
            html.Tr([
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
            ])
        ]

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, bordered=True, dark=True, hover=True, responsive=True, striped=True, id='data_table')

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
            html.Th('Sr.No.'),
            html.Th('File Name'),
            html.Th('Date Uploaded'),
            html.Th('Content Type'),
            html.Th('File Type'),
            html.Th('Sneek Peek'),
        ]))
    ]

    btn_obj = dbc.Button('Clear Table', color='light', className='mr-1', id='clear_input_table', n_clicks=0)

    table_rows = []

    if list_of_contents is not None:
        for sr_no, contents, filename, date in zip(list(range(len(list_of_contents))), list_of_contents, list_of_names, list_of_dates):
            INPUT_TABLE_ROWS_LIST.append(parse_contents(contents, filename, date))

            INPUT_TABLE_ROWS_LIST[sr_no][2].to_csv(Path('media/csv_files/', filename), index=False)

            table_rows.append(html.Tr([
                html.Td(sr_no),
                html.Td(INPUT_TABLE_ROWS_LIST[sr_no][0]),
                html.Td(INPUT_TABLE_ROWS_LIST[sr_no][1]),
                html.Td(INPUT_TABLE_ROWS_LIST[sr_no][3]),
                html.Td(INPUT_TABLE_ROWS_LIST[sr_no][4]),
                html.Td(
                    dcc.Link(dbc.Button('View File', color='success'), href=f'/dashboard/{INPUT_TABLE_ROWS_LIST[sr_no][0]}/{INPUT_TABLE_ROWS_LIST[sr_no][4]}')
                ),
            ]))
    else:
        if INPUT_TABLE_ROWS_LIST == []:
            table_rows.append(html.Tr([
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
            ]))
        else:
            for row in range(len(INPUT_TABLE_ROWS_LIST)):
                table_rows.append(html.Tr([
                    html.Td(row),
                    html.Td(INPUT_TABLE_ROWS_LIST[row][0]),
                    html.Td(INPUT_TABLE_ROWS_LIST[row][1]),
                    html.Td(INPUT_TABLE_ROWS_LIST[row][3]),
                    html.Td(INPUT_TABLE_ROWS_LIST[row][4]),
                    html.Td(
                        dcc.Link(dbc.Button('View File', color='success'), href=f'/dashboard/{INPUT_TABLE_ROWS_LIST[row][0]}/{INPUT_TABLE_ROWS_LIST[row][4]}')
                    ),
                ]))

    if nclicks != 0:
        btn_obj = dbc.Button('Clear Table', color='light', className='mr-1', id='clear_input_table', n_clicks=0)

        INPUT_TABLE_ROWS_LIST = []

        table_rows = [
            html.Tr([
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
                html.Td('Empty Cell'),
            ])
        ]

    table_body = [html.Tbody(table_rows)]
    table = dbc.Table(table_header + table_body, bordered=True, dark=True, hover=True, responsive=True, striped=True, id='data_table')

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
        file_name = pathname.split('/')[2]
        ext = pathname.split('/')[3]

        dataframe = pd.read_csv(f'media/csv_files/{file_name}.{ext}')

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
    delete_btn = dbc.Button('Delete Function', color='light', className='mr-1', id='delete_func', n_clicks=0)

    if '/eda-page/func-added' in pathname and NEW_FUNCTION_ADDED:
        NEW_FUNCTION_ADDED = False
        FUNCTION_NUMBER += 1

        new_func = html.Div(
            [
                html.P([NEW_PROCESS_DICTIONARY['dataframe_path']]),
                html.P([NEW_PROCESS_DICTIONARY['eda_process']]),
                html.P([', '.join(NEW_PROCESS_DICTIONARY['column_list'])]),
                html.P([NEW_PROCESS_DICTIONARY['inplace_bool']]),
            ],
            style={
                'width': '100%', 'height': 'auto', 'borderWidth': '1px', 'borderStyle': 'dashed',
                'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
            }
        )

        FUNCTION_LIST[f'function-{FUNCTION_NUMBER}'] = new_func
        ALL_PROCESS_LIST.append(NEW_PROCESS_DICTIONARY)

    if nclicks_delete != 0:
        delete_btn = dbc.Button('Delete Function', color='light', className='mr-1', id='delete_func', n_clicks=0)

        del FUNCTION_LIST[f'function-{FUNCTION_NUMBER}']

        FUNCTION_NUMBER -= 1

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

        return [html.Div(['Select Columns', select_columns])]

    return [html.Div(['Select Columns', select_columns])]


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
    global ALL_PROCESS_LIST

    exec_btn = dbc.Button('Execute Functions', color='light', className='mr-1', id='exec_func_list', n_clicks=0)
    badge_obj_success = dbc.Badge("Success", pill=True, color="success", className="mr-1", id='success_badge', style={'display': 'block'})
    badge_obj_info = dbc.Badge("Not Executed", pill=True, color="info", className="mr-1", id='info_badge', style={'display': 'block'})

    for process in ALL_PROCESS_LIST:
        func = config['process_function_mapping'][process['eda_process']]

        print(func())

    if nclicks != 0:
        time.sleep(2)
        return [badge_obj_success], exec_btn, False
    else:
        return [badge_obj_info], exec_btn, True


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8099)