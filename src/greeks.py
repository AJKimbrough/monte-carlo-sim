import numpy as np
from scipy.stats import norm

def compute_greeks(S0, K, T, r, sigma, option_type='call'):
    """
    Compute the Greeks for a European option using the Black-Scholes model.

    Returns a dictionary with Delta, Gamma, Vega, Theta, and Rho.
    """
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        delta = norm.cdf(d1)
        theta = (- (S0 * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * norm.cdf(d2))
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:
        delta = -norm.cdf(-d1)
        theta = (- (S0 * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 + r * K * np.exp(-r * T) * norm.cdf(-d2))
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    gamma = norm.pdf(d1) / (S0 * sigma * np.sqrt(T))
    vega = S0 * norm.pdf(d1) * np.sqrt(T)

    return {
        'delta': delta,
        'gamma': gamma,
        'vega': vega / 100,   #vega per 1% change in volatility
        'theta': theta / 365, #theta per day
        'rho': rho / 100      #rho per 1% change in rate
    }