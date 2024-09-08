import math
import statistics
import sys

import numpy as np


def print_progress_bar(iteration: int, total: int, length=40, indent="") -> None:
    """
    Prints a progress bar on the same line.

    :param iteration: process along the loading bar
    :param total: total iterations for a complete loading bar
    :param length: total length in characters
    :param indent: ident char at the beginning
    :return:
    """

    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '=' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{indent}[{bar}] {percent:.2f}%')
    sys.stdout.flush()


def dataset_info(data_set: dict) -> (float, float, float, float):
    """
    Returns the sample size, mean, standard deviation, variance, uniqueness, common songs, common songs as
    a percent and the genres that the common songs occur in a data set

    :param data_set: the genre data set
    :return: sample size, mean, standard deviation, variance, common, common_percent, genres
    """

    sample_size = sum(samples(data_set))
    mean = mean_sample_size(data_set)
    std_dev = standard_deviation(data_set)
    var = variance(data_set)
    common, common_percent, genres = check_common_songs(data_set)

    return sample_size, mean, std_dev, var, common, common_percent, genres


def samples(data: dict) -> list:
    """
    Returns the number of songs per genre as a 1D list

    :param data: genre data set
    :return: array of the number of songs per genre
    """

    return np.array([len(val) for val in data.values()])


def mean_sample_size(data: dict) -> float:
    """
    Gets the mean number of songs per genre

    :param data: genre dataset
    :return: mean number of songs per genre
    """

    vals = samples(data)
    vals = vals.tolist()
    return statistics.mean(vals)


def standard_deviation(data: dict) -> float:
    """
    Gets the standard deviation of the number of samples per genre

    :param data: genre dataset
    :return: standard deviation of dataset
    """

    vals = samples(data)
    vals = vals.tolist()
    return statistics.stdev(vals)


def variance(data: dict) -> float:
    """
    Gets the variance of the dataset

    :param data: genre dataset
    :return: variance of dataset
    """

    return math.pow(standard_deviation(data), 2)


def check_common_songs(data: dict) -> (int, float, list):
    """
    Finds the number of shared songs between different genres

    :param data: genre dataset
    :return: the number of shared songs, the percentage of the total number of songs, the genres which have shared songs
    """

    size = sum(samples(data))
    genres = {}
    count = 0
    for key1, val1 in data.items():
        for key2, val2 in data.items():
            if val1 == val2 and key1 != key2:
                count += 1
                if key1 not in genres:
                    genres.update({key1: 1})
                else:
                    genres[key1] += 1

    return count, count / size, genres
