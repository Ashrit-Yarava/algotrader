import logging

import numpy as np
from datetime import datetime
from glob import glob
from algotrader.trade.strategy import Strategy
from algotrader.trade.stock_trade import StockTrader
from algotrader.dataset.pandas_dataset import PandasDataset


class SimpleStrategy(Strategy):

    def __init__(self, stocks):
        super().__init__(stocks)
        self.index = 1

    def trade(self, data, capital):
        # Invest and sell every alternate day.
        self.index += 1
        if self.index % 2 == 0:
            return {s: 1 / len(self.stocks) for s in self.stocks}
        else:
            return {s: -1 for s in self.stocks}


def test_stock_trader():
    START_DATE = datetime(2021, 12, 1)
    END_DATE = datetime(2022, 3, 1)
    files = glob("./data/*.csv")
    dataset = PandasDataset(files, START_DATE, END_DATE)

    strategy = SimpleStrategy(dataset.get_items())
    trader = StockTrader(strategy, dataset, 10000)

    trader.backtest()
    logging.info(f"Profit: ${trader.net_profit()}")
    logging.info(f"Sharpe Ratio: {trader.sharpe_ratio()}")
    logging.info(f"Win Rate: {trader.win_rate()}")
    logging.info(f"Loss Rate: {trader.loss_rate()}")
