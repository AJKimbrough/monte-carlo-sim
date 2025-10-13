from monte_carlo import monte_carlo_option_price
from black_scholes import black_scholes_price
from portfolio_config import portfolio
from visualize import plot_distribution

print("\n--- Monte Carlo Option Pricing Simulator ---\n")
for asset in portfolio:
    mc_price, ST = monte_carlo_option_price(
        S0=asset['S0'],
        K=asset['K'],
        T=asset['T'],
        r=asset['r'],
        sigma=asset['sigma'],
        option_type=asset['type']
    )
    bs_price = black_scholes_price(
        S0=asset['S0'],
        K=asset['K'],
        T=asset['T'],
        r=asset['r'],
        sigma=asset['sigma'],
        option_type=asset['type']
    )

    print(f"{asset['ticker']} ({asset['type'].upper()}):")
    print(f"  Monte Carlo Price  = ${mc_price:.4f}")
    print(f"  Black-Scholes Price = ${bs_price:.4f}")
    print()

    plot_distribution(ST, asset['K'], asset['ticker'])
