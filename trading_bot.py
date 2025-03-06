import pandas as pd
import numpy as np
from binance.client import Client
import ta
import time
import json
import os
import random  # For dummy price simulation

# Parameters
RISK_PER_TRADE = 0.01
EMA_SHORT_PERIOD = 20
EMA_LONG_PERIOD = 50
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRAILING_STOP = True
TIMEFRAME = "8h"
INITIAL_BALANCE = 2000
MIN_TRADE_SIZE = 0.001
DCA_AMOUNT = 100
DCA_INTERVAL = 28800
DAILY_CAP_PER_COIN = 100

# Simulation toggle
SIMULATION = True  # Set to True for dummy mode, False for live

# Coins
COINS = ["SUIUSDT", "HBARUSDT", "TIAUSDT"]  # Updated order per your note
COIN_BALANCES = {coin: INITIAL_BALANCE / len(COINS) for coin in COINS}

# Load JSON keys (still needed for live mode or testnet)
json_file = "binance_keys.json"
if not os.path.exists(json_file):
    raise FileNotFoundError(f"{json_file} not found in {os.getcwd()}")
with open(json_file, 'r') as f:
    keys = json.load(f)
    client = Client(keys["api_key"], keys["api_secret"])  # Dummy mode ignores this

POSITIONS = {coin: {"amount": 0, "avg_entry_price": 0, "stop_loss": 0, "take_profit": 0} for coin in COINS}
DAILY_SPENT = {coin: 0 for coin in COINS}
TOTAL_PROFIT = {coin: 0 for coin in COINS}

# Mock prices for simulation (starting points)
MOCK_PRICES = {"SUIUSDT": 4.50, "HBARUSDT": 0.25, "TIAUSDT": 4.00}

def fetch_historical_data(symbol, timeframe, limit=100):
    if SIMULATION:
        # Simulate price data with random walk
        last_price = MOCK_PRICES[symbol]
        data = pd.DataFrame({
            'timestamp': [int(time.time() * 1000) - i * 8 * 3600 * 1000 for i in range(limit)],
            'open': [last_price * (1 + random.uniform(-0.02, 0.02)) for _ in range(limit)],
            'high': [last_price * (1 + random.uniform(0, 0.03)) for _ in range(limit)],
            'low': [last_price * (1 - random.uniform(0, 0.03)) for _ in range(limit)],
            'close': [last_price * (1 + random.uniform(-0.02, 0.02)) for _ in range(limit)],
            'volume': [random.uniform(100, 1000) for _ in range(limit)]
        })
        MOCK_PRICES[symbol] = data['close'].iloc[-1]  # Update last price
        return data
    else:
        kl
