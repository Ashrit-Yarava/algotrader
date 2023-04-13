class Strategy:
    """
    A superclass for creating stock trading algorithms. Inherit this class to
    perform operations.
    """

    def __init__(self, stocks: list):
        """
        Initialize the base strategy to always store the dataset and the
        starting cash.

        :param stocks: The stocks to use for the strategy.
        """
        self.stocks = stocks

    def trade(self, data, capital):
        """
        Perform a step in the strategy everytime a new datapoint is given.

        The outputted value must be an dictionary of how the remaining cash
        will be split amongst the stocks.

        For example,

        * { 'SPY': 0.7, 'AAPL': 0.3, 'AMZN': -1 }

        In this example, SPY will get 70% of the remaining cash, AAPL gets 30%
        and we are selling all stocks of AMZN.

        :param data: Latest stock price of each of the stock in the universe.
        :return: dictionary of the holdings and how holdings should be split up
        as a percentage.
        """
        pass
