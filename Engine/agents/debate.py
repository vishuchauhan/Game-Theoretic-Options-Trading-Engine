import requests
from config import OLLAMA_URL, MODEL_NAME


############################################
# LLM CALL (OLLAMA - SAFE VERSION)
############################################

def call_llm(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 200
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)

        # Check HTTP status
        if response.status_code != 200:
            print("⚠️ Ollama HTTP Error:", response.status_code)
            return "LLM Error: HTTP failure"

        data = response.json()

        # Validate response format
        if "response" not in data:
            print("⚠️ Unexpected Ollama response:", data)
            return "LLM Error: Invalid response format"

        return data["response"]

    except Exception as e:
        print("⚠️ Ollama request failed:", e)
        return "LLM Error: Exception occurred"


############################################
# MULTI-ROUND DEBATE ENGINE
############################################

def multi_round_debate(strategy, features, greeks, context, rounds=3):

    belief = 0.5
    history = []

    for r in range(rounds):

        ########################################
        # RISK MANAGER (RA)
        ########################################

        ra_prompt = f"""
You are a professional options risk manager.

Analyze this trade critically.

Market Data:
- Spot: {features['spot']}
- VIX: {features['vix']}
- Realized Vol: {context['realized_vol']}
- Trend: {context['trend']}

Strategy: {strategy}
Greeks:
- Delta: {greeks[0]}
- Gamma: {greeks[1]}
- Vega: {greeks[2]}
- Theta: {greeks[3]}

Round {r+1}:

Give a structured answer:

1. Market condition analysis
2. Key risks (theta decay, volatility mismatch, regime risk)
3. Failure scenario
4. Final verdict: (Strong Reject / Moderate Reject)
"""

        ra = call_llm(ra_prompt)

        # fallback if LLM fails
        if "LLM Error" in ra:
            ra = "Fallback: Trade is risky due to uncertainty and potential theta decay."

        ########################################
        # TRADER (RT)
        ########################################

        rt_prompt = f"""
You are a professional options trader.

Defend this trade.

Strategy: {strategy}

Risk manager said:
{ra}

Respond with:

1. Counter argument
2. Why payoff justifies risk
3. Best-case scenario
4. Final verdict: (Strong Accept / Moderate Accept)
"""

        rt = call_llm(rt_prompt)

        # fallback if LLM fails
        if "LLM Error" in rt:
            rt = "Fallback: Trade has convex payoff and potential upside."

        ########################################
        # BELIEF UPDATE (SMARTER)
        ########################################

        ra_lower = ra.lower()
        rt_lower = rt.lower()

        if "strong accept" in rt_lower:
            belief += 0.15
        elif "moderate accept" in rt_lower:
            belief += 0.07

        if "strong reject" in ra_lower:
            belief -= 0.15
        elif "moderate reject" in ra_lower:
            belief -= 0.07

        # clamp between 0 and 1
        belief = max(0, min(1, belief))

        ########################################
        # STORE ROUND
        ########################################

        history.append({
            "round": r + 1,
            "RA": ra,
            "RT": rt,
            "belief": belief
        })

    return history, belief


############################################
# FINAL CONSENSUS DECISION
############################################

def final_consensus(strategy, belief):

    if belief > 0.65:
        return f"EXECUTE {strategy} (High Conviction)"

    elif belief > 0.5:
        return f"EXECUTE {strategy} (Hedged / Reduced Size)"

    elif belief > 0.35:
        return f"UNCERTAIN — Avoid aggressive exposure"

    else:
        return f"REJECT {strategy} — Prefer neutral strategies like Iron Condor"