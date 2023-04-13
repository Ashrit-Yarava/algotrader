import pandas as pd
import numpy as np
from pathlib import Path
import logging
from algotrader.dataset.base_dataset import Dataset


class PandasDataset(Dataset):
    """
    A method of loading the dataset using csv files supplied from the Yahoo Finance database.
    """

    def __init__(self, csv_files, start_date, end_date):
        """
        Initialize the data structure and prepare the data pipeline.

        :param csv_files: A list of csv files with the ticker symbol as the stock name.
        :param start_date: The starting date to use from the CSV files.
        :param end_date: The ending date to use from the CSV files.
        """

        super().__init__()

        self.stocks = {}
        try:
            stocks = {Path(f).stem: pd.read_csv(f, index_col="Date",
                                            parse_dates=True).loc[
                                                start_date:end_date].to_numpy()
                  for f in csv_files}
        except Exception:
            logging.error("Something went wrong while loading the file.")
            stocks = {}

        self.index = 0
        self.max_len = 0
        sizes = set(map(len, stocks.values()))

        if len(sizes) != 1:
            logging.error("Input CSV files don't match.")
            return

        self.stocks = stocks

        logging.info(f"Loaded Stocks: {self.stocks.keys()} ({start_date} - {end_date})")
        self.max_len = list(sizes)[0]

    def __next__(self):
        """
        Get the next iteration of the dataset. AKA get the next day.

        :return: A dictionary of the stock symbols and the stock price of that day.
        """

        if not self.index < self.max_len:
            logging.info("Data Loading Finished.")
            return None

        index = self.index
        self.index += 1

        return {s: self.stocks[s][index] for s in self.stocks.keys()}

    def __str__(self):
        """
        A string representation printing the current day.

        :return: Current stock data.
        """

        text = ""

        for stock in self.stocks.keys():
            text += f"{stock}: "

            stock_details = np.round(self.stocks[stock][self.index], 2)
            text += np.array2string(stock_details, formatter={'float_kind': '{:0.2f}'.format}) + "\n"

        return text

    def get_items(self):
        return list(self.stocks.keys())

    def get_last_price(self):
        return {s: self.stocks[s][self.max_len - 1] for s in self.stocks.keys()}
