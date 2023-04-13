import logging

import numpy as np
from algotrader.trade.strategy import Strategy
from algotrader.dataset.base_dataset import Dataset
from algotrader.trade.trade import Trader
from algotrader.utils import print_data
from datetime import datetime
from glob import glob
from algotrader.dataset.pandas_dataset import PandasDataset


logging.basicConfig(level=logging.INFO)


class StockTrader(Trader):
    """
    Data Structure for trading stocks with a given strategy
    and giving useful information about the backtset.
    """

    def __init__(self, strategy: Strategy, dataset: Dataset, starting_cash):
        super().__init__(strategy, dataset, starting_cash)
        self.price_on_buy = {s: None for s in self.dataset.get_items()}

    def _perform_transactions(self, stock_price, requested_holdings):
        """
        Liquidate all assets that the user has requested to sell.

        :stock_price: The current stock prices.
        :requested_holdings: The trades that the strategy has set out.
        :return: The amount of money that the user has lost or gained as a
                 result.
        """

        cash = 0

        for stock in requested_holdings.keys():
            trade_value = 0
            if requested_holdings[stock] < 0:
                # If the strategy wants to sell:
                # * Calculate how much of the stock will be sold.
                # * Calculate the amount of cash liquidated as a result.
                # * Update the current holdings to match.
                amount_stock_sold = (-requested_holdings[stock] * self.curr_holdings[stock])
                trade_value += self._price(stock_price, stock) * amount_stock_sold
                self.curr_holdings[stock] -= amount_stock_sold

                rounded_amount = round(amount_stock_sold, 2)
                logging.info(f"- {stock} ({rounded_amount}): ${self._price(stock_price, stock)}")
                self.history["counts"]["sold"] += 1

                if self.price_on_buy[stock] is not None:
                    if self._price(stock_price, stock) > self.price_on_buy[stock]:  # There was a profit.
                        self.history["trades"]["profit"] += 1
                    elif self._price(stock_price, stock) < self.price_on_buy[stock]:
                        self.history["trades"]["loss"] += 1
                    else:
                        self.history["trades"]["equal"] += 1

            if requested_holdings[stock] > 0:
                # If the strategy wants to buy:
                # * Calculate how much of the stock will be bought.
                # * Calculate the amount of cash used. (Note: always will be
                #   less)
                # * Update the current holdings
                if self.cash < 100:  # Don't buy anything if the user is broke.
                    continue
                money_used = requested_holdings[stock] * self.cash
                amount_stock_gained = money_used / self._price(stock_price, stock)
                self.curr_holdings[stock] += amount_stock_gained
                trade_value -= money_used
                self.price_on_buy[stock] = self._price(stock_price, stock)

                rounded_amount = round(amount_stock_gained, 2)
                logging.info(f"+ {stock} ({rounded_amount}): ${self._price(stock_price, stock)}")
                self.history["counts"]["bought"] += 1

            cash += trade_value

        return cash
