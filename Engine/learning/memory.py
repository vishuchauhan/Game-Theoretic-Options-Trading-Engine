import numpy as np

class Memory:
    def __init__(self):
        self.history = []

    def update(self, strategy, pnl):
        self.history.append({"strategy": strategy, "pnl": pnl})

    def bias(self, strategy):
        data = [h["pnl"] for h in self.history if h["strategy"] == strategy]

        if len(data) == 0:
            return 0

        return np.mean(data)