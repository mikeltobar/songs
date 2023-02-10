from helpers import *


p = Path(__file__).parents[1]
file_path_1 = os.path.join(p, 'PEC4/plots')


def bar_plotter(file_path, col_name):
    """
    Plots two different methods of csv reading. Plots them and saves them to the plots folder.
    Args:
    file_path : string
        a column's value. Must be an artist's name.
    col_name: string
        a column's name.
    """
    i = 1
    rows = []
    x_legend = ""
    for path in file_path:
        col_i = file_path.index(path)
        col = col_name[col_i]
        methods = ["pandas", "csv_dictreader"]
        dt = []
        start_time_pandas = timeit.default_timer()
        get_column_pandas(path, col)
        dt.append(timeit.default_timer() - start_time_pandas)
        start_time_csv = timeit.default_timer()
        get_column_csv_dictreader(path, col)
        dt.append(timeit.default_timer() - start_time_csv)
        df = pd.read_csv(path, sep=';')
        length = len(df.index)
        rows.append(length)
        plt.subplot(1, 3, i)
        plt.bar(methods, dt)
        i += 1
    plt.title('Run Time Comparison')
    for idx, row in enumerate(rows):
        x_legend += (str(row) + ", ")
        if idx == (len(rows) - 1):
            x_legend += ('and ' + str(row))
    plt.xlabel('Number of rows read: ' + x_legend)
    plt.ylabel('Time(s)')
    file_path_2 = os.path.join(file_path_1, 'barplot.png')
    plt.savefig(file_path_2)
    plt.show()


def group_mean_feature_plotter(title, leg_x, leg_y, means_1, means_2):
    """
    Plots a certain feature according to a grouping argument and a filter. Saves them to the plots folder.
    Args:
    title: string
        a title for the plot
    leg_x: string
        a legend for the x axis
    leg_y: string
        a legend for the y axis
    means_1: list of numbers
        a list of numeric values
    means_2: list of numbers
        a list of numeric values
    """
    album_list = means_2.index.tolist()
    plt.xlabel(leg_x)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(leg_y)
    plt.title(title)
    plt.bar(album_list, means_1)
    plt.subplots_adjust(bottom=0.3)
    file_path_3 = os.path.join(file_path_1, 'group_mean.png')
    plt.savefig(file_path_3)
    plt.show()


def audio_feature_histogram(column, filter, dataframe, title):
    """
    Gets a density probability histogram of a certain column, usually representing an audio feature.
    Saves them to the plots folder.
    Args:
    column: string
        a column's name included in the dataframe
    filter: pandas dataframe filter
        a condition we want to apply
    dataframe: a pandas dataframe
        self-explanatory
    title: string
        a title for the plot
    """
    dataframe_subset = dataframe[filter]
    col_list = dataframe_subset[column].tolist()
    col_list = list(np.around(np.array(col_list), 2))
    items = len(dataframe_subset)
    hist, bins = np.histogram(col_list, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    bin_counts = zip(bins, bins[1:], hist)
    result = {}
    for bin_start, bin_end, count in bin_counts:
        result_key = str(bin_start) + "-" + str(bin_end)
        result_value = count
        result[result_key] = result_value/items
    x_values = list(result.keys())
    y_values = list(result.values())
    plt.xlabel("Number of items: " + str(items))
    plt.ylabel("Probability density")
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.bar(x_values, y_values)
    plt.subplots_adjust(bottom=0.3)
    file_path_4 = os.path.join(file_path_1, 'audio_feature_histogram.png')
    plt.savefig(file_path_4)
    plt.show()


def density_prob_comparison_plot(column1, filter1, column2, filter2, dataframe, title, name1, name2):
    """
    Compares 2 density probability plots on selected columns and filters. Plots them together.
    Saves them to the plots folder.
    Args:
    column1: string
        a column's name included in the dataframe
    filter1: pandas dataframe filter
        a condition we want to apply
    column12: string
        a column's name included in the dataframe
    filter2: pandas dataframe filter
        a condition we want to apply
    dataframe: a pandas dataframe
        self-explanatory
    name1: a string
        name of the first element for the legend
    name2: a string
        name of the second element for the legend
    """
    dataframe_subset_1 = dataframe[filter1]
    dataframe_subset_2 = dataframe[filter2]
    col_list_1 = dataframe_subset_1[column1].tolist()
    col_list_2 = dataframe_subset_2[column2].tolist()
    col_list_1 = list(np.around(np.array(col_list_1), 2))
    col_list_2 = list(np.around(np.array(col_list_2), 2))
    items_1 = len(dataframe_subset_1)
    items_2 = len(dataframe_subset_2)
    hist_1, bins_1 = np.histogram(col_list_1, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    hist_2, bins_2 = np.histogram(col_list_2, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    bin_counts_1 = zip(bins_1, bins_1[1:], hist_1)
    bin_counts_2 = zip(bins_2, bins_1[1:], hist_2)
    result_1 = {}
    result_2 = {}
    result = {}
    for bin_start, bin_end, count in bin_counts_1:
        result_key = str(bin_start) + "-" + str(bin_end)
        result_value = count
        result_1[result_key] = result_value / items_1
    for bin_start, bin_end, count in bin_counts_2:
        result_key = str(bin_start) + "-" + str(bin_end)
        result_value = count
        result_2[result_key] = result_value / items_2
    for key in list(result_2.keys()):
        dict_list = []
        dict_list.append(result_1[key])
        dict_list.append(result_2[key])
        result[key] = dict_list
    x_values = list(result.keys())
    y_values_1 = list(result_1.values())
    y_values_2 = list(result_2.values())
    plt.xlabel("Number of items: " + str(name1) + "- " + str(items_1) + ", " + str(name2) + "-" + str(items_2))
    plt.ylabel("Probability density")
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    x = np.arange(len(x_values))  # the label locations
    ax = plt.subplot(111)
    ax.bar(x - 0.2, y_values_1, width=0.4, color='b', align='center', label=name1)
    ax.bar(x + 0.2, y_values_2, width=0.4, color='r', align='center', label=name2)
    ax.set_xticks(x, x_values)
    ax.legend()
    file_path_5 = os.path.join(file_path_1, 'density_prob_comparison_plot.png')
    plt.savefig(file_path_5)
    plt.show()


def heatmap(names, features, dataframe, dis_type, col):
    """
    Takes a list of names present in the dataframe. Plots heatmap of the difference between its numeric columns.
    Saves them to the plots folder.
    Args:
    names: list of strings
        a list of names of artists
    features: list of strings
        list of column names to analyze
    dataframe: a pandas dataframe
        self-explanatory
    dis_type: a string, must be either 'euclidean' or 'cosinus'
        distance type
    col: a string, must be 'artist_name'
        intended so that the feature_means function works
    """
    base_list = []
    for name in names:
        use_list = features_mean(name, dataframe, features, col)
        base_list.append(use_list)
    series = np.array(base_list)
    if dis_type == 'euclidean':
        matrix = squareform(pdist(series))
        matrix = matrix.round(decimals=1)
    elif dis_type == 'cosinus':
        matrix = squareform(pdist(series, metric='cosine'))
        matrix = matrix.round(decimals=9)
    fig, ax = plt.subplots()
    im = ax.imshow(matrix)
    ax.set_xticks(np.arange(len(names)), labels=names)
    ax.set_yticks(np.arange(len(names)), labels=names)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    for i in range(len(names)):
        for j in range(len(names)):
            text = ax.text(j, i, matrix[i, j],
                           ha="center", va="center", color="w")
    title = ("Distances (" + dis_type + ") between features")
    ax.set_title(title)
    fig.tight_layout()
    if dis_type == 'euclidean':
        file_path_6 = os.path.join(file_path_1, 'euclidean_heatmap.png')
    elif dis_type == 'cosinus':
        file_path_6 = os.path.join(file_path_1, 'cosinus_heatmap.png')
    plt.savefig(file_path_6)
    plt.show()





