# 🧠 Monte Carlo Option Pricing for Portfolio

This project simulates and prices European options using Monte Carlo methods on a multi-asset portfolio. It also compares the results to Black-Scholes analytical pricing.

## Features
- Supports call and put options
- Uses GBM for stock price simulation
- Compares Monte Carlo vs Black-Scholes price
- Histograms of price distributions
- Configurable portfolio

## Example Assets
```python
[
  {"ticker": "AAPL", "S0": 190, "K": 200, "T": 0.5, "r": 0.05, "sigma": 0.3, "type": "call"},
  {"ticker": "TSLA", "S0": 250, "K": 230, "T": 1.0, "r": 0.05, "sigma": 0.5, "type": "put"}
]
