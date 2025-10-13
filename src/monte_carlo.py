import numpy as np

def simulate_gbm(S0, r, sigma, T, N):
    """
    Simulate stock price at time T using Geometric Brownian Motion.
    """
    Z = np.random.standard_normal(N)
    ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
    return ST

def monte_carlo_option_price(S0, K, T, r, sigma, N=100000, option_type='call'):
    """
    Estimate the price of a European option using Monte Carlo simulation.
    """
    ST = simulate_gbm(S0, r, sigma, T, N)
    if option_type == 'call':
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)
    price = np.exp(-r * T) * np.mean(payoff)
    return price, ST
