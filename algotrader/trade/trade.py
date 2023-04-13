import logging
import numpy as np

from algotrader.utils import print_data


class Trader:
    """
    Base class for all trader implementations for different markets.
    """

    def __init__(self, strategy, dataset, starting_cash):
        self.strategy = strategy
        self.dataset = dataset
        self.curr_holdings = {s: 0 for s in self.dataset.get_items()}
        self.starting_cash = starting_cash
        self.cash = starting_cash
        self.history = {
            "holdings": {s: [] for s in self.dataset.get_items()},
            "evaluation": [self.starting_cash],
            "stock_price": {s: [] for s in self.dataset.get_items()},
            "requested_holdings": {s: [] for s in self.dataset.get_items()},
            "counts": {
                "sold": 0,
                "bought": 0,
            },
            "trades": {
                "profit": 0,
                "loss": 0,
                "equal": 0
            }
        }

    def _perform_transactions(self, price, requested_holdings):
        """
        Liquidate all assets that the strategy has requested to sell and buy
        assets strategy wishes to invest in.

        :stock_price: The current stock prices.
        :requested_holdings: The trades that the strategy has set out.
        :return: The amount of money that the user has lost or gained as a
                 result.
        """
        return 0

    def _price(self, price, item):
        return price[item][0]

    def get_total_value(self, price):
        evaluation = self.cash

        for item in self.curr_holdings.keys():
            evaluation += self._price(price, item) * self.curr_holdings[item]

        return evaluation

    def save_iteration(self, stock_price, holdings):
        for stock in self.curr_holdings.keys():
            self.history["holdings"][stock].append(self.curr_holdings[stock])
            self.history["stock_price"][stock].append(stock_price[stock])
            self.history["requested_holdings"][stock].append(holdings[stock])
        self.history["evaluation"].append(self.get_total_value(stock_price))

    def backtest(self):
        while (stock_price := next(self.dataset)) is not None:
            logging.info(f"\nIteration: {self.dataset.index}\n{print_data(stock_price)}")
            holdings = self.strategy.trade(stock_price, self.cash)

            cash_delta = self._perform_transactions(stock_price, holdings)

            self.cash += cash_delta

            self.save_iteration(stock_price, holdings)

    def sharpe_ratio(self, risk_free_rate: float = 8):
        """
        Calculate the Sharpe Ratio with the given risk-free rate.
        Sharpe Ratio is defined as:
            * (Return - Risk Free Rate) / Standard Deviation of return.

        :param risk_free_rate: The specified risk-free rate.
        :return: The Sharpe Ratio.
        """
        delta_portfolio = (self.get_total_value(self.dataset.get_last_price()) - self.starting_cash)
        period = sum(self.history["counts"].values())
        avg_return = delta_portfolio / period
        std_return = (np.array(self.history["evaluation"]) - self.starting_cash).std()
        ratio = (avg_return - (risk_free_rate / 100)) / std_return
        return round(ratio, 2)

    def win_rate(self):
        """
        Calculate the win rate.

        :return: The win rate as a decimal.
        """
        total_trades = sum(self.history["trades"].values())
        wins = self.history["trades"]["profit"]
        return round(wins / total_trades if total_trades != 0 else 0, 2)

    def loss_rate(self):
        """
        Calculate the loss rate.

        :return: The loss rate as a decimal.
        """
        total_trades = sum(self.history["trades"].values())
        losses = self.history["trades"]["loss"]
        return round(losses / total_trades if total_trades != 0 else 0, 2)

    def net_profit(self):
        """
        Get the net profit from running the backtest.

        :return: The net profit of the algorithm.
        """
        return round(self.history['evaluation'][-1] - self.starting_cash, 2)

    def get_history(self):
        """
        Return the backtest history.
                    "holdings": {s: [] for s in self.dataset.get_items()},
            "evaluation": [self.starting_cash],
            "stock_price": {s: [] for s in self.dataset.get_items()},
            "requested_holdings": {s: [] for s in self.dataset.get_items()},
            "counts": {
                "sold": 0,
                "bought": 0,
                "days": 0
            },
            "trades": {
                "profit": 0,
                "loss": 0,
                "equal": 0
            }
            * holdings: The current stock holdings.
            * evaluation: The changes in the account's evaluation.
            * stock_price: The last known stock price.
            * requested_holdings: The last requested holdings.
            * counts: The number of each type of trade made.
                * sold: The number of times a stock was sold.
                * bought: The number of times a stock was bought.
            * trades: The number of trades that were made.
                * profit: Profitable trades.
                * loss: Trades that resulted in a loss.
                *

        :return: The backtesting history.
        """
        return self.history
