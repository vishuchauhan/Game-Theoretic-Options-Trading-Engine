# Game-Theoretic-Options-Trading-Engine
Game-theoretic options trading engine using LLM-based multi-agent debate, regime detection, and payoff visualization to simulate real-world trading decision making.

A quantitative options trading system that combines **market regime detection**, **options payoff modeling**, and a **multi-agent LLM debate framework** to simulate real-world trading decisions.

This project is designed to move beyond traditional indicator-based strategies and instead model how traders **reason, disagree, and converge on decisions under uncertainty**.

---

## Key Idea

Instead of directly predicting prices, this system:

> Simulates a **signaling game** between two agents (Risk Averse vs Risk Seeking)  
> → Uses debate to evaluate strategies  
> → Selects a strategy based on reasoning, not just signals  

---

## Features

### Market Intelligence
- Real-time spot & VIX data
- Historical price ingestion
- Regime detection using HMM (Trending / Mean Reverting / High Volatility)

---

### Options Engine
- Black-Scholes pricing (fallback)
- Real NSE option chain support (when available)
- Payoff modeling for:
  - Long Call
  - Long Put
  - Straddle
  - Iron Condor

---

### Multi-Agent Debate (Core Innovation)
- Two-agent system:
  - **Agent 1**: Hidden type (Risk Averse / Risk Seeking)
  - **Agent 2**: Infers and reacts
- 2-round signaling game:
  - Strategy proposal
  - Challenge & inference
  - Belief update
  - Final decision

---

### Payoff Visualization
- Strategy payoff curves using matplotlib
- Helps interpret risk/reward visually

---

### Backtesting Engine
- Strategy performance tracking
- Metrics:
  - Total PnL
  - Win Rate
  - Average Return
  - Sharpe Ratio
 
---

## System Architecture

Market Data → Feature Extraction → Regime Detection
↓
Strategy Set Generation
↓
LLM Debate Engine (Game Theory Layer)
↓
Strategy Selection
↓
Payoff Simulation + Visualization
↓
Backtesting Engine


---

## Example Output

ROUND 1
Agent1: Proposes Long Call (bullish + volatility)
Agent2: Challenges → suggests Straddle

ROUND 2
Agent1: Defends directional view
Agent2: Updates belief → prefers volatility strategy

Final:
Best Strategy: Straddle
Decision: Execute
Confidence: 0.8


---

## Backtest Insights

Typical results:

- Low win rate → expected for options (convex payoff)
- Positive PnL driven by large moves
- Moderate Sharpe → room for optimization

---

## Limitations

- LLM output may be inconsistent for long structured prompts (model limitation)
- Strategy selection still partially dependent on prompt quality
- No position sizing or portfolio allocation yet
- NSE API reliability varies

---

## Future Improvements

- Integrate AI decisions into backtesting loop
- Confidence-based trade filtering
- Position sizing & risk management
- Volatility surface modeling
- Multi-strategy portfolio optimization

---

## Why This Is Different

Most trading systems:
- Use indicators
- Predict direction

This system:
- Models **decision-making under uncertainty**
- Uses **game theory + agent interaction**
- Focuses on **strategy selection, not prediction**

---

## Tech Stack

- Python
- NumPy, Pandas
- Matplotlib
- HMM (hmmlearn)
- Ollama (LLM - LLaMA3 / Phi)

---

## Author's Note

This project is an attempt to bridge:
Quantitative finance × Game theory × AI reasoning
and explore how modern AI can simulate real trading thought processes, not just outputs.


## How to Run

```bash
python main.py




