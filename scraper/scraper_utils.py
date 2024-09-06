import math
import statistics
import sys

import numpy as np


def print_progress_bar(iteration, total, length=40, indent=""):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '=' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{indent}[{bar}] {percent:.2f}%')
    sys.stdout.flush()


def dataset_info(data_set):

    print("dataset info:")

    sample_size = sum(samples(data_set))
    print(f"\t- sample size: {sample_size}")

    mean = mean_sample_size(data_set)
    print(f"\t- mean genre size: {round(mean, 3)}")

    std_dev = standard_deviation(data_set)
    print(f"\t- standard deviation of genre size: {round(std_dev, 3)}")

    var = variance(data_set)
    print(f"\t- variance of genre size: {round(var, 3)}")

    common, common_percent = check_common_songs(data_set)
    print(f"\t- uniqueness: {round((1-common_percent)*100, 3)}% - {common} shared songs between different genres")

    return sample_size, mean, std_dev, var


def samples(data):
    return np.array([len(val) for val in data.values()])


def mean_sample_size(data):
    vals = samples(data)
    vals = vals.tolist()
    return statistics.mean(vals)


def standard_deviation(data):
    vals = samples(data)
    vals = vals.tolist()
    return statistics.stdev(vals)


def variance(data):
    return math.pow(standard_deviation(data), 2)


def check_common_songs(data):
    size = sum(samples(data))
    count = 0
    for key1, val1 in data.items():
        for key2, val2 in data.items():
            if val1 == val2:
                count += 1

    return count, count / size
