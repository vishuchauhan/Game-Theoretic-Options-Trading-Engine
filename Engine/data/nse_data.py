import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

SESSION = requests.Session()


def get_nse_option_chain():

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    # Step 1: get cookies
    SESSION.get("https://www.nseindia.com", headers=HEADERS)

    # Step 2: actual request
    response = SESSION.get(url, headers=HEADERS, timeout=10)

    data = response.json()

    return data


def extract_atm_options(data, spot):

    strikes = []

    for item in data['records']['data']:
        if 'CE' in item and 'PE' in item:
            strikes.append(item['strikePrice'])

    # find closest strike
    atm = min(strikes, key=lambda x: abs(x - spot))

    for item in data['records']['data']:
        if item['strikePrice'] == atm:
            return {
                "strike": atm,
                "call_iv": item['CE']['impliedVolatility'],
                "put_iv": item['PE']['impliedVolatility'],
                "call_price": item['CE']['lastPrice'],
                "put_price": item['PE']['lastPrice']
            }

    return None