import pandas as pd
import re
import timeit
import csv
import matplotlib
from matplotlib import pyplot as plt
import os
from scipy.spatial.distance import squareform, pdist
from PIL import Image
from pathlib import Path
import os
import numpy as np
import zipfile


def unzipper(file_path, target_path):
    """
    Unzips file and loads it in path
    Args:
    file_path: string
        a string with the file's location
    target_path: string
        desired location
    """
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_path)


def reader(file_path, sep):
    """
    Reads a dataframe
    Args:
    file_path: string
        a string with the file's location
    sep: string
        a separator
    Returns:
    return_dataframe: a pandas dataframe
        read dataframe
    """
    return_dataframe = pd.read_csv(file_path, on_bad_lines='skip', sep=sep)
    return return_dataframe


def capitalizer(dataframe, column):
    """
    Capitalizes a dataframe's column
    Args:
    dataframe: a pandas dataframe
        self-explanatory
    column: string
        a column's name
    Returns:
    dataframe: a pandas dataframe
        read dataframe
    """
    row_num = -1
    for row in dataframe[column]:
        row_num += 1
        new_list = row.split()
        for item in new_list:
            if not re.match(r"^[A-Z]", item):
                dataframe.at[row_num, column] = row.title()
                break
    return dataframe


def empty_handler(dataframe, column):
    """
    Handles empty values from a dataframe's column
    Args:
    dataframe: a pandas dataframe
        self-explanatory
    column: string
        a column's name
    Returns:
    dataframe: a pandas dataframe
        read dataframe
    """
    avg = dataframe[column].mean()
    val = float('%.1f'%(avg))
    dataframe[column] = dataframe[column].fillna(val)
    return dataframe


def get_column_pandas(file_path, col_name):
    """
    Returns a pandas dataframe column
    Args:
    file_path: string
        a string with the file's location
    col_name: string
        a column's name (which is included in the file)
    Returns:
    column: series
        the desired column
    """
    col_use = []
    col_use.append(col_name)
    column = pd.read_csv(file_path, usecols=col_use, sep=';')
    return column


def get_column_csv_dictreader(file_path, col_name):
    """
    Reads a csv's column with csv library
    Args:
    file_path: string
        a string with the file's location
    col_name: string
        a column's name (which is included in the file)
    Returns:
    result: list
        the read column in a list format
    """
    with open(file_path, encoding="utf-8") as f:
        data = csv.DictReader(f, delimiter=';')
        result = []
        for row in data:
            result.append(row[col_name])
    return result


def value_count(value, column, dataframe, description):
    """
    Counts the occurrences of a value called like a String in a certain column of a dataset
    Args:
    value: string
        a string we want to evaluate
    column: string
        a column's name (which is included in the file)
    dataframe: a pandas dataframe
        self-explanatory
    description: string
        a description to include in the output
    Returns:
    message: string
        a comment with the desired output
    """
    count = ((dataframe[column] == value).sum())
    message = 'There are ' + str(count) + ' occurrences of ' + description + '.'
    return message


def contain_count(value, column, dataframe, description):
    """
    Counts the occurrences of a value called like a String contained as part of a certain column of a dataset
    Args:
    value: string
        a string we want to evaluate
    column: string
        a column's name (which is included in the file)
    dataframe: a pandas dataframe
        self-explanatory
    description: string
        a description to include in the output
    Returns:
    message: string
        a comment with the desired output
    """
    count = (dataframe[column].astype(str).str.count(value).sum())
    message = 'There are ' + str(count) + ' occurrences of ' + description + '.'
    return message


def get_top_value(column1, column2, dataframe, description, constraint):
    """
    Gets an attribute of a value being the top one in another one, applying a constraint if
    applicable.
    Args:
    column1 : string
        a column's name (which is included in the file)
    column2 : string
        a column's name (which is included in the file)
    dataframe: a pandas dataframe
        self-explanatory
    description: string
        a description to include in the output
    constraint: pandas dataframe filter
        a condition we want to apply
    Returns:
    message: string
        a comment with the desired output
     """
    if constraint is not None:
        dataframe = dataframe[constraint]
    top = (dataframe[column1].max())
    value = dataframe.loc[dataframe[column1] == top, column2].iloc[0]
    message = 'The ' + description + ' is ' + value + '.'
    return message


def decade(column1, column2, beginning, end, dataframe, description):
    """
    Checks which values appear in different decades.
    Args:
    column1 : string
        a column's name (which is included in the file). Must contain year values.
    column2 : string
        a column's name (which is included in the file)
    beginning: int
        the first year of the decade
    end: int
        the last year of the decade
    dataframe: a pandas dataframe
        self-explanatory
    description: string
        a description to include in the output
    Returns:
    message: string
        a comment with the desired output
    """
    current = int(beginning/10)
    finish = int(end/10)
    reference_x = dataframe[column2].unique()
    reference_y = 0
    reference_dict = dict.fromkeys(reference_x, reference_y)
    must_have = 0
    result = ''
    while current <= finish:
        already_done = []
        my_series = dataframe[column1].astype(str).str.contains("^" + str(current))
        my_list = my_series.tolist()
        counter = -1
        for val in my_list:
            counter += 1
            if val:
                key = dataframe.loc[counter, column2]
                if key not in already_done:
                    reference_dict[key] += 1
                    already_done.append(key)
        current += 1
        must_have += 1
    for key in reference_dict:
        if reference_dict[key] == must_have:
            result += key + ', '
    message = 'The values ' + description + ' are: ' + result + 'according to the given dataframe.'
    return message


def min_mean_max_feature(column, filter, dataframe, description):
    """
    Calculates min, mean, and max values of a certain feature in a dataframe
    applying a given filter.
    Args:
    column : string
        a column's name (which is included in the file). Must contain numeric values.
    filter: pandas dataframe filter
        a condition we want to apply
    dataframe: a pandas dataframe
        self-explanatory
    description: string
        a description to include in the output
    Returns:
    message: string
        a comment with the desired output
    """
    if filter is not None:
        dataframe = dataframe[filter]
    min = dataframe[column].min()
    max = dataframe[column].max()
    mean = dataframe[column].mean()
    message = 'For ' + description + ' min value is: ' + "{:.2f}".format(min) + ', max value is: ' + \
              "{:.2f}".format(max) + ', & mean value is: ' + "{:.2f}".format(mean) + '.'
    return message


def get_means(column, filter, group_by, dataframe):
    """
    Gets the mean values of a dataframe's column, grouping by a column.
    Args:
    column : string
        a column's name (which is included in the file). Must contain numeric values.
    filter: pandas dataframe filter
        a condition we want to apply
    group_by: string
        a column's name (which is included in the file). Must contain numeric values.
    dataframe: a pandas dataframe
        self-explanatory
    Returns:
    means_list, means: tuple
        a tuple with the means as a list and as pandas column series
    """
    if filter is not None:
        dataframe = dataframe[filter]
    means = dataframe.groupby(group_by)[column].mean()
    means_list = means.values.tolist()
    means_list = list(np.around(np.array(means_list), 2))
    return means_list, means


def features_mean(name, dataframe, features, column):
    """
    Calculates the mean value of the audio features for a certain artist
    Args:
    name : string
        a column's value. Must be an artist's name.
    dataframe: a pandas dataframe
        self-explanatory
    features: list of strings
        a list of desired columns to include
    column : string
        a column's name (which is included in the file). Must contain numeric values.
    Returns:
    means: list
        a list with mean values
    """
    dataframe_subset = dataframe[(dataframe[column] == name)]
    dataframe_subset = dataframe_subset[features]
    means = []
    for col in dataframe_subset.columns:
        mean = dataframe_subset[col].mean()
        means.append(mean)
    return means








