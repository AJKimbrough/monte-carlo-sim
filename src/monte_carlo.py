import numpy as np

def simulate_gbm(S0, r, sigma, T, N):
    """
    Simulate stock price at time T using Geometric Brownian Motion.
    """
    Z = np.random.standard_normal(N)
    ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
    return ST

def monte_carlo_option_price(S0, K, T, r, sigma, N, option_type='call', return_paths=False):
    dt = T
    np.random.seed(42)
    Z = np.random.standard_normal(N)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

    if option_type == 'call':
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)

    price = np.exp(-r * T) * np.mean(payoff)

    if return_paths:
        return price, ST
    else:
        return price


def asian_option_price(S0, K, T, r, sigma, N, option_type='call', return_paths=False):
    np.random.seed(42)
    M = 252  # daily steps in a year
    dt = T / M
    paths = np.zeros((N, M + 1))
    paths[:, 0] = S0

    for t in range(1, M + 1):
        z = np.random.standard_normal(N)
        paths[:, t] = paths[:, t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

    avg_price = paths.mean(axis=1)
    if option_type == 'call':
        payoff = np.maximum(avg_price - K, 0)
    else:
        payoff = np.maximum(K - avg_price, 0)

    price = np.exp(-r * T) * np.mean(payoff)

    if return_paths:
        return price, avg_price
    else:
        return price


def barrier_option_price(S0, K, T, r, sigma, N, option_type='call', barrier_type="up-and-out", barrier_level=None, return_paths=False):
    np.random.seed(42)
    M = 252
    dt = T / M
    paths = np.zeros((N, M + 1))
    paths[:, 0] = S0

    for t in range(1, M + 1):
        z = np.random.standard_normal(N)
        paths[:, t] = paths[:, t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

    breached = np.zeros(N, dtype=bool)

    if "up" in barrier_type:
        breached = np.any(paths >= barrier_level, axis=1)
    elif "down" in barrier_type:
        breached = np.any(paths <= barrier_level, axis=1)

    if "out" in barrier_type:
        valid = ~breached
    else:
        valid = breached

    ST = paths[:, -1]
    if option_type == 'call':
        payoff = np.where(valid, np.maximum(ST - K, 0), 0)
    else:
        payoff = np.where(valid, np.maximum(K - ST, 0), 0)

    price = np.exp(-r * T) * np.mean(payoff)

    if return_paths:
        return price, ST
    else:
        return price

