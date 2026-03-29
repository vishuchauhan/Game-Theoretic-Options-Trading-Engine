import matplotlib.pyplot as plt

def plot_payoff(S_range, pnl, strategy):
    plt.figure()
    plt.plot(S_range, pnl)
    plt.axhline(0)
    plt.title(f"{strategy} Payoff")
    plt.xlabel("Price at Expiry")
    plt.ylabel("P&L")
    plt.show()