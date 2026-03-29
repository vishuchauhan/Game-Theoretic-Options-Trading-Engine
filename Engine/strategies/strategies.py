import numpy as np

class Strategy:
    def __init__(self, name):
        self.name = name


def generate_strategies():
    return [
        Strategy("Long Call"),
        Strategy("Long Put"),
        Strategy("Straddle"),
        Strategy("Iron Condor")
    ]


def payoff_curve(strategy, S_range, K, call_price, put_price):

    pnl = []

    for S_T in S_range:

        if strategy.name == "Long Call":
            payoff = max(S_T-K,0) - call_price

        elif strategy.name == "Long Put":
            payoff = max(K-S_T,0) - put_price

        elif strategy.name == "Straddle":
            payoff = max(S_T-K,0)+max(K-S_T,0)-(call_price+put_price)

        elif strategy.name == "Iron Condor":
            width = 300
            max_profit = 100

            if abs(S_T - K) < width:
                payoff = max_profit
            else:
                payoff = max_profit - abs(S_T-K-width)

        pnl.append(payoff)

    return np.array(pnl)