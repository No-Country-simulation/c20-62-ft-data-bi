import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import ast
import os
import io
import sys
import json
import numpy as np



def load_files_to_dataframe(main_folder_path):
    '''
    Function to read JSON, CSV, and XLSX files from a directory, process them,
    and return a dictionary of Pandas DataFrames.

    Parameters:
    - main_folder_path (str): The path to the main folder containing subfolders with files.

    Returns:
    - dicc (dict): A dictionary where keys are folder or file names and values are Pandas DataFrames.
    '''
    dicc = {}

    for sub_folder in os.listdir(main_folder_path):
        sub_folder_path = os.path.join(main_folder_path, sub_folder)

        # Process files in subfolders
        if os.path.isdir(sub_folder_path):
            folder_name = sub_folder
            dataframe_list = []

            for file in os.listdir(sub_folder_path):
                file_path = os.path.join(sub_folder_path, file)
                dataframe_aux = read_file(file_path, file)
                if dataframe_aux is not None:
                    dataframe_list.append(dataframe_aux)

            if dataframe_list:
                dataframe_object = pd.concat(dataframe_list, axis=0, ignore_index=True)
                dicc[folder_name] = dataframe_object
                print(f'Data from {folder_name} successfully loaded.')

        # Process files in main folder
        elif sub_folder.endswith(('.json', '.csv', '.xlsx')):
            file_path = sub_folder_path
            file_name = sub_folder.split('.')[0]

            dataframe_aux = read_file(file_path, sub_folder)
            if dataframe_aux is not None:
                dicc[file_name] = dataframe_aux
                print(f'File {file_name} successfully loaded.')

    return dicc


def read_file(file_path, file_name):
    '''
    Helper function to read a file based on its extension and return a DataFrame.
    Tries different strategies for JSON files, reading them fully, line by line with ast.literal_eval,
    or line by line normalizing.

    Parameters:
    - file_path (str): The path to the file.
    - file_name (str): The name of the file.

    Returns:
    - df (pd.DataFrame): A Pandas DataFrame containing the data from the file or None if the file is empty or unsupported.
    '''
    if file_name.endswith('.json'):
        try:
            if os.path.getsize(file_path) > 0:
                return read_generic_json(file_path)
            else:
                print(f'File {file_name} is empty, skipping.')
                return None
        except ValueError as e:
            print(f'Error reading {file_name}: {e}')
            return None
    elif file_name.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_name.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        print(f'Unsupported file format: {file_name}')
        return None


def read_generic_json(file_path):
    '''
    Function to read JSON files and handle different formats:
    1. Full JSON reading.
    2. Line by line reading using ast.literal_eval.
    3. Line by line normalizing JSON objects.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - df (pd.DataFrame): A Pandas DataFrame containing the data from the JSON file.
    '''
    # Try 1: Read as JSON 
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    
    except json.JSONDecodeError:
        print(f'Failed to load full JSON from {file_path}. Trying line-by-line methods.')

    # Try 2: Read line by line using ast.literal_eval
    rows = []
    try:
        with open(file_path, encoding='utf-8') as f:
            for line in f.readlines():
                rows.append(ast.literal_eval(line))
        return pd.DataFrame(rows)
    
    except (ValueError, SyntaxError):
        print(f'Failed to parse JSON with ast.literal_eval for {file_path}. Trying normalization.')

    # Try  3: Read line by line normalizing JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        json_obj = [json.loads(line) for line in content.split('\n') if line.strip()]
        return pd.json_normalize(json_obj)
    
    except Exception as e:
        print(f'All parsing methods failed for {file_path}. Error: {e}')
        return None
    

def convert_column_to_string(dataframe, col):
    '''
    Converts a specific column in the dataframe to string (object dtype).
    
    Parameters:
    - dataframe (pd.DataFrame): The DataFrame containing the column.
    - col (str): The column to convert to string.
    
    Returns:
    - pd.Series: The column converted to string.
    '''
    dataframe[col] = dataframe[col].astype(str)
    return dataframe[col]

def try_save_parquet(dataframe_aux, file_path):
    '''
    Tries to save the DataFrame as a Parquet file. If it fails, only converts problematic columns to string type.
    
    Parameters:
    - dataframe_aux (pd.DataFrame): The DataFrame to be saved.
    - file_path (str): The file path where the Parquet file will be saved.
    
    Returns:
    - None
    '''
    try:
        # Try to convert full  DataFrame to Parquet
        table = pa.Table.from_pandas(dataframe_aux)
        pq.write_table(table, file_path)
        print(f'Dataframe saved successfully at {file_path}')
    except Exception as e:
        print(f"Error saving DataFrame at {file_path}: {e}")
        print("Converting problematic columns to string and retrying...")
        
        # Ir it fails, identify problematic columns
        problematic_columns = []
        for col in dataframe_aux.columns:
            try:
                # Try to convert column by column to parquet
                pa.array(dataframe_aux[col])
            except Exception:
                # when a column fails, mark as problematic column
                problematic_columns.append(col)
        
        # Converto the problematic columns to string
        for col in problematic_columns:
            dataframe_aux[col] = convert_column_to_string(dataframe_aux, col)
            print(f"Column '{col}' converted to string.")

        # Try to save the dataframe again
        try:
            table = pa.Table.from_pandas(dataframe_aux)
            pq.write_table(table, file_path)
            print(f'Dataframe saved successfully after converting problematic columns to string at {file_path}')
        except Exception as final_error:
            print(f"Final error saving DataFrame at {file_path}: {final_error}")

def dataframe_to_parquet(dicc, subfolder_name):
    '''
    Function to save Pandas DataFrames as Parquet files. If the conversion fails, it will convert problematic
    columns to string and retry saving.
    
    Parameters:
    - dicc (dict): A dictionary where keys are folder names and values are Pandas DataFrames.
    - subfolder_name (str): The desired subfolder name to be used in the file path.
    
    Returns:
    - None
    '''
    for key, dataframe_aux in dicc.items():
        # File path
        file_path = f'/lakehouse/default/Files/{subfolder_name}/{key}.parquet'
        
        # Save dataframee
        try_save_parquet(dataframe_aux, file_path)


def save_to_pq(dfs, names):

    """
    Saves a DataFrame to a parquet file in a specific directory.
        Parameters:
        - df: DataFrame to save.
        - file_name: Name of the parquet file.
    """
    for df, name in zip(dfs, names):
        archivo = f'data/parquet/{name}.parquet'
        pq.write_table(pa.Table.from_pandas(df), archivo)
        print(f"DataFrame '{name}' save as '{archivo}'")


def data_summ_f(df, title=None):
    '''
    Function to provide detailed information about the dtype, null values,
    and outliers for each column in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame for which information is to be generated.
    - title (str, optional): Title to be used in the summary. If None, the title will be omitted.

    Returns:
    - df_info (pd.DataFrame): A DataFrame containing information about each column,
                              including data type, non-missing quantity, percentage of
                              missing values, missing quantity, and information about outliers.
    '''
    info_dict = {"Column": [], "Data_type": [], "No_miss_Qty": [], "%Missing": [], "Missing_Qty": []}

    for column in df.columns:
        info_dict["Column"].append(column)
        info_dict["Data_type"].append(df[column].apply(type).unique())
        info_dict["No_miss_Qty"].append(df[column].count())
        info_dict["%Missing"].append(round(df[column].isnull().sum() * 100 / len(df), 2))
        info_dict['Missing_Qty'].append(df[column].isnull().sum())

  
    df_info = pd.DataFrame(info_dict)

    if title:
        print(f"{title} Summary")
        print("\nTotal rows: ", len(df))
        print("\nTotal full null rows: ", df.isna().all(axis=1).sum())

    print(df_info.to_string(index=False))
    print("=====================================")

    return df_info

def data_summ_on_parquet(folder_path):
    '''
    Function to apply data_summ function to each Parquet file in a folder.

    Parameters:
    - folder_path (str): The path to the folder containing Parquet files.

    Returns:
    - summaries (list): A list of DataFrames containing the summary information for each Parquet file.
    '''
    summaries = []

    # Loop through each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is a Parquet file
        if file_name.endswith('.parquet'):
            # Read the Parquet file into a DataFrame
            df = pq.read_table(file_path).to_pandas()

            # Get the title for the DataFrame based on the file name
            title = file_name.replace('.parquet', '')

            # Apply data_summ function to the DataFrame
            summary = data_summ_f(df, title=title)

            # Append the summary DataFrame to the list
            summaries.append(summary)

    return summaries


def data_summ(df, title=None):
    '''
    Function to provide detailed information about the dtype, null values,
    and outliers for each column in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame for which information is to be generated.
    - title (str, optional): Title to be used in the summary. If None, the title will be omitted.

    Returns:
    - df_info (pd.DataFrame): A DataFrame containing information about each column,
                              including data type, non-missing quantity, percentage of
                              missing values, missing quantity, and information about outliers.
    '''
    info_dict = {"Column": [], "Data_type": [], "No_miss_Qty": [], "%Missing": [], "Missing_Qty": []}

    for column in df.columns:
        info_dict["Column"].append(column)
        info_dict["Data_type"].append(df[column].apply(type).unique())
        info_dict["No_miss_Qty"].append(df[column].count())
        info_dict["%Missing"].append(round(df[column].isnull().sum() * 100 / len(df), 2))
        info_dict['Missing_Qty'].append(df[column].isnull().sum())

  
    df_info = pd.DataFrame(info_dict)

    if title:
        print(f"{title} Summary")
        print("\nTotal rows: ", len(df))
        print("\nTotal full null rows: ", df.isna().all(axis=1).sum())

    
    return df_info



def duplicates(df, column):
    '''
    Checks and displays duplicate rows in a DataFrame based on a specific column.

    This function takes as input a DataFrame and the name of a specific column.
    Then, identify duplicate rows based on the content of the specified column,
    filters and sorts them for easier comparison.

    Parameters:
        df (pandas.DataFrame): The DataFrame to search for duplicate rows.
        column (str): The name of the column based on which to check for duplicates.

    Returns:
        pandas.DataFrame or str: A DataFrame containing the filtered and sorted duplicate rows,
        lists for inspection and comparison, or the message "No Duplicates" if no duplicates are found.
    '''
    # Duplicate rows are filtered out
    duplicated_rows = df[df.duplicated(subset=column, keep=False)]
    if duplicated_rows.empty:
        return "There are no duplicates"
    
    # sort duplicate rows to compare with each other
    duplicated_rows_sorted = duplicated_rows.sort_values(by=column)
    return duplicated_rows_sorted


def drop_duplicates(df, column):
    '''
    This function counts the null values in each row to organize the dataframe in order of null values, 
    in order to eliminate duplicate records that have the same value 
    without affecting the row that has the most valid records.
    '''

     # temporary column 
    df['temp_index'] = range(len(df))

    # Count null values in each row
    df['num_null'] = df.isnull().sum(axis=1)

    # Sort by the specified column and the number of nulls
    df = df.sort_values(by=[column, 'num_null'])

    # Drop duplicates, keep the first occurrence
    df = df.drop_duplicates(subset=column, keep='first')

    # Sort again by the temporary column
    df = df.sort_values(by='temp_index')

    # Remove temporary columns
    df.drop(['temp_index', 'num_null'], axis=1, inplace=True)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df


def replace_all_nulls(df):
    '''
    Recieves a df as parameter and fills all the null values per column depending on their dtype
    '''

    for column in df.columns:
        # Crear una máscara para los valores no nulos
        mask = df[column].notnull()
        dtype = df[column][mask].apply(type).unique()

        if dtype[0] == str: 
            # Usar .loc para asegurar que la operación se aplique correctamente
            df.loc[:, column] = df.loc[:, column].fillna('No data')
        elif dtype[0] == float:
            mean = df[column].mean()
            # Usar .loc para asignar el valor de la media en los NaN
            df.loc[:, column] = df.loc[:, column].fillna(mean)
        elif dtype[0] == list:
            # Usar .loc para asignar 'No data' a las columnas de listas
            df.loc[:, column] = df.loc[:, column].fillna('No data')

    return df



    



