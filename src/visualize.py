import matplotlib.pyplot as plt

def plot_distribution(ST, K, ticker):
    """
    Plot histogram of simulated terminal prices with strike price overlay.
    """
    plt.figure(figsize=(8, 5))
    plt.hist(ST, bins=100, alpha=0.6, label='Simulated $S_T$')
    plt.axvline(K, color='red', linestyle='--', label=f'Strike = {K}')
    plt.title(f"Simulated Distribution of {ticker} at Expiry")
    plt.xlabel("Price at Maturity ($S_T$)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"plots/{ticker}_dist.png")
    plt.close()
