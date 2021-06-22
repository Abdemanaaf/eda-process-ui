from .basic_eda_func import BasicEDAFunctions

config = {
    'eda_process_list': [
        'Drop NA Values',
        'Drop Duplicate Values',
    ],

    'process_function_mapping': {
        'Drop NA Values': BasicEDAFunctions.drop_na
    }
}

