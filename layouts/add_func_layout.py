import glob

from pathlib import Path

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from src.config import config

raw_input_files = glob.glob('media/csv_files/*.csv')
cached_files = glob.glob('media/csv_files/cache/*.csv')
mapping_files = glob.glob('media/mapping_files/*.csv')

raw_input_dict = []
for value, label in enumerate(raw_input_files):
    raw_input_dict.append({'label': label, 'value': label})

cached_dict = []
for value, label in enumerate(cached_files):
    cached_dict.append({'label': label, 'value': label})

mapping_dict = []
for value, label in enumerate(mapping_files):
    mapping_dict.append({'label': label, 'value': label})


df_select_opt = [{"label": "----Input Files", "disabled": True}] + \
    raw_input_dict + \
    [{"label": "----Cached Files", "disabled": True}] + \
    cached_dict + \
    [{"label": "----Mapping Files", "disabled": True}] + \
    mapping_dict


eda_process_list = [{"label": "----Basic Functions", "disabled": True}] + \
    [{'label': label, 'value': label} for label in config['eda_process_list']] + \
    [{"label": "----Advance Functions", "disabled": True}] + \
    [{'label': label, 'value': label} for label in config['adv_eda_process_list']]


radioitems = dbc.FormGroup(
    [
        dbc.Label("Choose one"),
        dbc.RadioItems(
            options=[
                {"label": "Save New DataFrame", "value": 0},
                {"label": "Impute in Original Dataframe", "value": 1},
            ],
            value=1,
            id="radioitems-input",
        ),
    ]
)

text_input = html.Div(
    [
        dbc.Input(id="input", placeholder="Type something...", type="text"),
    ]
)

select = dbc.Select(
    id="select",
    options=df_select_opt
)

select_eda_process = dbc.Select(
    id="select_eda_process",
    options=eda_process_list
)


add_func_layout = dbc.Container([
    html.Div([], id='update_bool', style={'display': 'none'}),

    html.Div([
        html.P('Add New Function'),
        html.Div(['Select Dataframe From List: ', select], id='select_dataframe'),
        html.Div(['Select EDA Process: ', select_eda_process], id='process_select_div'),
        html.Div([
            dcc.Dropdown(
                id="select_columns",
                options=[{'label':'---Select Dataframe', 'value': 'NA'}],
                multi=True
            )
        ], id='select_columns_div'),


        radioitems,
        html.Div(['New Dataframe Name: ', text_input], id='df_name_input_div'),


        dcc.Link(
            dbc.Button('Add New Function to the List', color='light', className='mr-1', id='submit_func_to_list', n_clicks=0),
            href='/eda-page/func-added'
        ),
    ])
], className='container-fluid mt-5')