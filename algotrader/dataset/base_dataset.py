class Dataset:
    """
    Abstract class for the dataset structure used for data loading and processing.
    """

    def __init__(self):
        """
        Initialize the dataset. Load/Download the necessary data.
        """
        pass

    def __next__(self):
        """
        Get the very next entry in the dataset.

        :return: A dictionary of the stocks accompanied by the stock prices
                 in OHLC format followed by dividends and splits.
        """
        pass

    def get_items(self):
        """
        Get the universe of all the stocks in this dataset.

        :return: A list of the stock ticker symbols.
        """
        pass

    def get_last_price(self):
        """
        Gets the last prices of the stocks. AKA present day.

        :return: A dictionary of the stock prices. Same style as __next__.
        """