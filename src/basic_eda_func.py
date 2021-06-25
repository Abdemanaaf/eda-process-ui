import pandas as pd

class BasicEDAFunctions(object):

    def __init__(self):
        pass

    @staticmethod
    def drop_na(data_path, col_list, inplace_bool, new_file_name):
        column_subset = []
        return_dict = {
            'process_name': 'Drop NA'
        }

        dataframe = pd.read_csv(data_path)

        if 'All Columns' in col_list:
            column_subset = list(dataframe.columns)
        else:
            column_subset = col_list

        dataframe = dataframe.dropna(subset=column_subset)

        if inplace_bool == 1:
            return_dict['dataframe'] = dataframe
        else:
            dataframe.to_csv(f'media/csv_files/cache/{new_file_name}.csv', index=False)

            return_dict['dataframe'] = dataframe

        return return_dict

    @staticmethod
    def filter_columns(data_path, col_list, inplace_bool, new_file_name):
        column_subset = []
        return_dict = {
            'process_name': 'Filter Columns'
        }

        dataframe = pd.read_csv(data_path)

        if 'All Columns' in col_list:
            column_subset = list(dataframe.columns)
        else:
            column_subset = col_list

        dataframe = dataframe[column_subset]

        if inplace_bool == 1:
            return_dict['dataframe'] = dataframe
        else:
            dataframe.to_csv(f'media/csv_files/cache/{new_file_name}.csv', index=False)

            return_dict['dataframe'] = dataframe

        return return_dict

    @staticmethod
    def drop_duplicates(data_path, col_list, inplace_bool, new_file_name):
        column_subset = []
        return_dict = {
            'process_name': 'Filter Columns'
        }

        dataframe = pd.read_csv(data_path)

        if 'All Columns' in col_list:
            column_subset = list(dataframe.columns)
        else:
            column_subset = col_list

        dataframe = dataframe.drop_duplicates(subset=column_subset)

        if inplace_bool == 1:
            return_dict['dataframe'] = dataframe
        else:
            dataframe.to_csv(f'media/csv_files/cache/{new_file_name}.csv', index=False)

            return_dict['dataframe'] = dataframe

        return return_dict

    @staticmethod
    def convert_datatype():
        pass
