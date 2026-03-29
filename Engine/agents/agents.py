class Agent:
    def __init__(self, name):
        self.name = name

    def evaluate(self, payoff, greeks, regime):
        delta, gamma, vega, theta = greeks

        if self.name == "RA":
            score = payoff - abs(theta)*5 - abs(gamma)*2

            if regime == "Mean Reverting":
                score -= 50

        else:
            score = payoff + abs(gamma)*2 + vega

            if regime == "Trending":
                score += 50

        return score