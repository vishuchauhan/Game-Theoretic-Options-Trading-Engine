import numpy as np

# ===== IMPORTS =====
from data.market_data import get_live_data, get_historical_prices
from models.pricing import black_scholes
from models.regime import detect_regime
from strategies.strategies import generate_strategies, payoff_curve
from agents.debate import call_llm
from utils.visualization import plot_payoff
from config import *

from backtest.backtester import Backtester
from analytics.performance import performance_stats


# ===== MARKET CONTEXT =====
def market_context(prices):
    returns = np.diff(np.log(prices))
    return {
        "realized_vol": np.std(returns) * np.sqrt(252),
        "trend": prices[-1] - prices[-20]
    }


# ===== BACKTEST STRATEGY =====
def strategy_decision(prices_window):
    if prices_window[-1] < prices_window[-5]:
        return "Long Put"
    else:
        return "Long Call"


# ===== 🔥 FINAL PRO DEBATE ENGINE (UPGRADED) =====
def strategy_game_debate(strategies, features, context):

    strategy_names = [s.name for s in strategies]

    # ===== STEP 1: STRICT CONTROLLED DEBATE =====
    reasoning_prompt = f"""
You are a quantitative trading engine.

STRICT RULES:
- No greetings
- No explanations outside template
- Use ONLY these strategies: {strategy_names}
- If any other strategy is used → output INVALID

============================
ROUND 1

Agent1:
Strategy:
Reason1:
Reason2:

Agent2:
Inferred_Type:
Challenge:
Alternative_Strategy: (must be from list)
Reason:

============================
ROUND 2

Agent1:
Response:
Final_Stance:

Agent2:
Updated_Belief:

Strategy_Comparison:
- Compare at least 3 strategies from the list
- Use payoff logic (directional vs volatility vs range)
- Include volatility impact (VIX)
- Explain clearly why one dominates others

Final_Choice: (must be from list)

============================

MARKET:
Spot: {features['spot']}
VIX: {features['vix']}
Trend: {context['trend']}
Volatility: {context['realized_vol']}

IMPORTANT:
- Fill ALL fields
- DO NOT skip sections
- Use payoff shape reasoning (directional vs volatility vs range)
"""

    reasoning = call_llm(reasoning_prompt)

    # ===== VALIDATION =====
    if "ROUND 2" not in reasoning:
        reasoning += "\n\n[WARNING: INCOMPLETE OUTPUT]"

    # ===== STEP 2: STRICT FINAL DECISION =====
    final_prompt = f"""
From this debate:

{reasoning}

Choose ONLY from:
{strategy_names}

Return EXACTLY:

Best Strategy: <one from list>
Decision: Execute / Avoid / Hedge
Confidence: 0.X
Reason: one short line based on comparison

NO extra text.
"""

    final_output = call_llm(final_prompt)

    return reasoning + "\n\n----------------------\n" + final_output


# ===== PARSERS =====
def extract_strategy(text, strategies):

    for line in text.split("\n"):
        if "best strategy" in line.lower():
            for s in strategies:
                if s.name.lower() in line.lower():
                    return s

    text_lower = text.lower()
    counts = {s.name: text_lower.count(s.name.lower()) for s in strategies}

    best = max(counts, key=counts.get)
    for s in strategies:
        if s.name == best:
            return s

    return strategies[0]


def extract_decision(text):

    t = text.lower()

    if "execute" in t:
        return "EXECUTE"
    elif "avoid" in t:
        return "AVOID"
    elif "hedge" in t:
        return "HEDGE"

    return "HEDGE"


# ===== LIVE ENGINE =====
def run_live():

    print("\n===== LIVE ENGINE =====")

    spot, vix = get_live_data()
    prices = get_historical_prices()

    regime = detect_regime(prices)
    context = market_context(prices)

    K = spot

    # ===== OPTION DATA =====
    try:
        from data.nse_data import get_nse_option_chain, extract_atm_options

        nse_data = get_nse_option_chain()
        atm = extract_atm_options(nse_data, spot)

        if atm:
            call_price = atm["call_price"]
            put_price = atm["put_price"]
            print("✅ Using NSE option chain")
        else:
            raise Exception

    except:
        print("⚠️ NSE failed → using BSM fallback")
        call_price, *_ = black_scholes(
            spot, K, TIME_TO_EXPIRY, RISK_FREE_RATE, vix, "call"
        )
        put_price, *_ = black_scholes(
            spot, K, TIME_TO_EXPIRY, RISK_FREE_RATE, vix, "put"
        )

    strategies = generate_strategies()
    S_range = np.linspace(0.85 * spot, 1.15 * spot, 100)

    # ===== SIGNALING GAME =====
    output = strategy_game_debate(
        strategies,
        {"spot": spot, "vix": vix},
        context
    )

    selected_strategy = extract_strategy(output, strategies)
    decision = extract_decision(output)

    pnl_curve = payoff_curve(
        selected_strategy,
        S_range,
        K,
        call_price,
        put_price
    )

    # ===== OUTPUT =====
    print("\n===== FINAL OUTPUT =====")
    print("Spot:", round(spot, 2), "| VIX:", round(vix, 2))
    print("Regime:", regime)

    print("\n===== SIGNALING GAME OUTPUT =====")
    print(output)

    print("\nSelected Strategy:", selected_strategy.name)
    print("Parsed Decision:", decision)

    plot_payoff(S_range, pnl_curve, selected_strategy.name)


# ===== BACKTEST =====
def run_backtest():

    print("\n===== RUNNING BACKTEST =====")

    prices = get_historical_prices()

    bt = Backtester()
    results = bt.run(prices, strategy_decision)

    stats = performance_stats(results)

    print("\n===== BACKTEST RESULTS =====")

    for k, v in stats.items():
        print(k, ":", round(v, 2))

    print("\n===== BACKTEST INTERPRETATION =====")

    win_rate = stats["Win Rate"]
    sharpe = stats["Sharpe"]

    if win_rate < 0.4:
        print("• Low win rate → options rely on large moves")
    else:
        print("• Decent win rate → stable system")

    if sharpe < 0.5:
        print("• Low Sharpe → unstable returns")
    elif sharpe < 1:
        print("• Moderate Sharpe → improvable")
    else:
        print("• Strong Sharpe → good system")

    print("• Improvements:")
    print("  - Confidence filtering")
    print("  - Volatility-based trades")
    print("  - Use spreads")


# ===== MAIN =====
if __name__ == "__main__":
    run_live()
    run_backtest()