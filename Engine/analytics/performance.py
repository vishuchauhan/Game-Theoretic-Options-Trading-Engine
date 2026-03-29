import numpy as np


def performance_stats(trades):

    trades = np.array(trades)

    total = np.sum(trades)
    win_rate = np.mean(trades > 0)
    avg_return = np.mean(trades)

    sharpe = np.mean(trades) / (np.std(trades) + 1e-6)

    return {
        "Total PnL": total,
        "Win Rate": win_rate,
        "Avg Return": avg_return,
        "Sharpe": sharpe
    }