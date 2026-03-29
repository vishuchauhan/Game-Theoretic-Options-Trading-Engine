import requests
import numpy as np

def get_live_data():
    try:
        nifty = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI").json()
        vix = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5EINDIAVIX").json()

        spot = nifty['chart']['result'][0]['meta']['regularMarketPrice']
        vix_val = vix['chart']['result'][0]['meta']['regularMarketPrice']

        return float(spot), float(vix_val)

    except:
        return 22500.0, 15.0


import requests
import numpy as np

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def safe_request(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)

        if response.status_code != 200:
            print(f"Error: Status {response.status_code}")
            return None

        return response.json()

    except Exception as e:
        print("Request failed:", e)
        return None


def get_live_data():
    try:
        nifty_data = safe_request("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI")
        vix_data = safe_request("https://query1.finance.yahoo.com/v8/finance/chart/%5EINDIAVIX")

        if nifty_data is None or vix_data is None:
            raise Exception("API failed")

        spot = nifty_data['chart']['result'][0]['meta']['regularMarketPrice']
        vix = vix_data['chart']['result'][0]['meta']['regularMarketPrice']

        return float(spot), float(vix)

    except:
        print("⚠️ Using fallback live data")
        return 22500.0, 15.0


def get_historical_prices():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?range=6mo&interval=1d"
        data = safe_request(url)

        if data is None:
            raise Exception("No data")

        prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
        prices = [p for p in prices if p is not None]

        if len(prices) == 0:
            raise Exception("Empty prices")

        return np.array(prices)

    except:
        print("⚠️ Using fallback historical data")
        # fallback synthetic data
        return np.cumsum(np.random.normal(0, 1, 200)) + 22500