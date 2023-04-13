import numpy as np


def print_data(data):
    """
    Print the current day's data in a nicer format compared to the dictionary.

    :param data: The current data generated from the dataset.
    :return: A string representation of the given data formatted nicely.
    """
    text = ""

    for stock in data.keys():
        text += f"* {stock}: "

        stock_details = np.round(data[stock], 2)
        text += np.array2string(stock_details,
                                formatter={'float_kind': '{:0.2f}'.format}
                                ) + "\n"

    return text[:-1]

