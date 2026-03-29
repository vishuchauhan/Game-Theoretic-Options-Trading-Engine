import numpy as np


class Backtester:

    def __init__(self):
        self.trades = []

    def run(self, prices, strategy_func):

        for i in range(50, len(prices)-1):

            window = prices[:i]

            decision = strategy_func(window)

            S_today = prices[i]
            S_next = prices[i+1]

            pnl = self.simulate_trade(decision, S_today, S_next)

            self.trades.append(pnl)

        return self.trades

    def simulate_trade(self, strategy, S, S_next):

        if strategy == "Long Call":
            return max(S_next - S, 0)

        elif strategy == "Long Put":
            return max(S - S_next, 0)

        elif strategy == "Straddle":
            return abs(S_next - S)

        elif strategy == "Iron Condor":
            return 50 - abs(S_next - S)

        return 0