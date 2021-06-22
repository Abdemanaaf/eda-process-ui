import base64
import datetime
import io

import pandas as pd

import dash_html_components as html
from pandas.core.frame import DataFrame


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            dataframe = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(f'Exception Encountered\n{e}')

        return html.Div([f'There was an error processing this file - {filename}'])

    return (filename.split('.')[0], datetime.datetime.fromtimestamp(date), dataframe, content_type, filename.split('.')[1])