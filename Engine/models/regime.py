import numpy as np
from hmmlearn.hmm import GaussianHMM

def detect_regime(prices):
    returns = np.diff(np.log(prices)).reshape(-1,1)

    model = GaussianHMM(n_components=3, covariance_type="diag", n_iter=100)
    model.fit(returns)

    states = model.predict(returns)
    state = states[-1]

    if state == 0:
        return "Trending"
    elif state == 1:
        return "Mean Reverting"
    else:
        return "High Volatility"