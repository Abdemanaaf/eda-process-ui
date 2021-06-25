from .basic_eda_func import BasicEDAFunctions

config = {
    'eda_process_list': [
        'Filter Columns',
        'Drop Duplicate Values',
        'Drop NA Values',
        'Drop Columns',
        'Convert Datatypes',
        'Filter Rows',
        'Sort Data',
    ],

    'adv_eda_process_list': [
        'Group By',
        'Pivot Table',
        'Merge Data',
        'Append/Concat Data'
    ],

    'process_function_mapping': {
        'Filter Columns': BasicEDAFunctions.filter_columns,
        'Drop Duplicate Values': BasicEDAFunctions.drop_duplicates,
        'Drop NA Values': BasicEDAFunctions.drop_na
    }
}

