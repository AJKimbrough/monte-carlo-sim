import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from monte_carlo import monte_carlo_option_price, asian_option_price, barrier_option_price
from black_scholes import black_scholes_price
from greeks import compute_greeks

st.set_page_config(page_title="Alea Optionum", layout="wide")
st.markdown("<h1 style='text-align: center;'> Alea Optionum - Monte Carlo Option Pricing Simulator</h1>", unsafe_allow_html=True)

# -- Helper function to visualize sample paths --
def plot_simulated_paths(S0, T, r, sigma, model="vanilla", steps=252, paths=10):
    dt = T / steps
    np.random.seed(42)
    Z = np.random.standard_normal((paths, steps))
    S = np.zeros_like(Z)
    S[:, 0] = S0
    for t in range(1, steps):
        S[:, t] = S[:, t - 1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t])

    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(paths):
        ax.plot(np.linspace(0, T, steps), S[i], linewidth=1)
    ax.set_title(f"Sample Simulated Paths ($S_t$ over Time) – {model.title()} Option")
    ax.set_xlabel("Time (Years)")
    ax.set_ylabel("Simulated Price ($S_t$)")
    ax.grid(True, linestyle='--', alpha=0.3)
    return fig

# -- Usage Guide --
with st.expander("How to Use This Dashboard", expanded=True):
    st.markdown("""
    Use the **sidebar** to set your option pricing simulation parameters:

    - **Initial Stock Price (S₀)** – Current price of the asset  
    - **Strike Price (K)** – Exercise price of the option  
    - **Time to Maturity (T)** – In years (e.g. 0.5 = 6 months)  
    - **Risk-free Rate (r)** – Annualized interest rate (e.g., 0.05)  
    - **Volatility (σ)** – As a decimal (e.g., 0.2 for 20%)  
    - **Option Type** – 'Call' or 'Put'  
    - **Simulations** – Number of Monte Carlo paths to run  
    - **Model Type** – Vanilla, Asian, or Barrier Option Pricing

    After entering inputs, click **🔄 Run Simulation** to:
    - Get a simulated option price (Monte Carlo, Asian, or Barrier)
    - Compare to Black-Scholes price (if applicable)
    - View the distribution of final simulated prices ($S_T$)
    - View option Greeks: Delta, Gamma, Vega, Theta, Rho
    """)

# --- Sidebar Inputs ---
st.sidebar.header("Simulation Parameters")
ticker = st.sidebar.text_input("Ticker Symbol (pulls S₀ & σ from Yahoo Finance)", value="AAPL")
use_yahoo = st.sidebar.checkbox("Use Yahoo Finance data", value=True)

if use_yahoo:
    try:
        data = yf.Ticker(ticker).history(period="1y")
        S0 = data["Close"].iloc[-1]
        sigma = np.std(np.log(data["Close"] / data["Close"].shift(1)).dropna()) * np.sqrt(252)
    except Exception as e:
        st.sidebar.warning("⚠️ Failed to retrieve data from Yahoo Finance. Please check the ticker.")
        S0, sigma = 100.0, 0.2
else:
    S0 = st.sidebar.number_input("Initial Stock Price (S₀)", value=100.0, min_value=0.01)
    sigma = st.sidebar.number_input("Volatility (σ)", value=0.2, format="%.4f")

K = st.sidebar.number_input("Strike Price (K)", value=100.0, min_value=0.01)
T = st.sidebar.number_input("Time to Maturity (T in years)", value=1.0, min_value=0.01)
r = st.sidebar.number_input("Risk-free Rate (r)", value=0.05, format="%.4f")
option_type = st.sidebar.radio("Option Type", ["call", "put"], horizontal=True)
N = st.sidebar.slider("Number of Simulations", min_value=1000, max_value=500000, value=100000, step=10000)
model_type = st.sidebar.selectbox("Model Type", ["vanilla", "asian", "barrier"])
show_paths = st.sidebar.checkbox("📉 Show Sample Simulated Paths", value=True)

# Barrier inputs only if selected
if model_type == "barrier":
    barrier_type = st.sidebar.selectbox("Barrier Type", ["up-and-in", "up-and-out", "down-and-in", "down-and-out"])
    barrier_level = st.sidebar.number_input("Barrier Level", value=S0 * 1.1)

# --- Run Simulation ---
if st.sidebar.button("🔄 Run Simulation"):
    with st.spinner("Simulating..."):
        if model_type == "asian":
            mc_price, ST = asian_option_price(S0, K, T, r, sigma, N, option_type, return_paths=True)
        elif model_type == "barrier":
            mc_price, ST = barrier_option_price(S0, K, T, r, sigma, N, option_type, barrier_type, barrier_level, return_paths=True)
        else:
            mc_price, ST = monte_carlo_option_price(S0, K, T, r, sigma, N, option_type, return_paths=True)

        bs_price = black_scholes_price(S0, K, T, r, sigma, option_type) if model_type == "vanilla" else None
        greeks = compute_greeks(S0, K, T, r, sigma, option_type)

        col1, col2 = st.columns([1, 1])
        col1.metric(label="Monte Carlo Price", value=f"${mc_price:.4f}")
        if bs_price:
            col2.metric(label="Black-Scholes Price", value=f"${bs_price:.4f}")

        st.markdown("### Option Greeks")
        gcol1, gcol2, gcol3 = st.columns(3)
        gcol1.metric("Delta", f"{greeks['delta']:.4f}")
        gcol1.metric("Gamma", f"{greeks['gamma']:.4f}")
        gcol2.metric("Vega", f"{greeks['vega']:.4f}")
        gcol2.metric("Theta", f"{greeks['theta']:.4f}")
        gcol3.metric("Rho", f"{greeks['rho']:.4f}")

        st.divider()
        st.markdown("#### Distribution of Simulated Terminal Prices")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(ST, bins=100, color="#1f77b4", alpha=0.7, edgecolor='white')
        ax.axvline(K, color='red', linestyle='--', label=f'Strike Price (K = {K})')
        ax.set_title("Histogram of $S_T$ (Simulated Prices at Maturity)")
        ax.set_xlabel("Simulated Price at Expiry ($S_T$)")
        ax.set_ylabel("Frequency")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)

        st.download_button(
            label="📥 Download Simulated Prices (CSV)",
            data=pd.DataFrame({"Simulated $S_T$": ST}).to_csv(index=False),
            file_name="simulated_prices.csv",
            mime="text/csv"
        )

        if show_paths:
            st.markdown("#### Sample Simulated Paths ($S_t$ over Time)")
            fig2 = plot_simulated_paths(S0, T, r, sigma, model_type)
            st.pyplot(fig2)

        with st.expander("How to Interpret the Results", expanded=False):
            st.markdown("""
            **Monte Carlo Price**  
            - Estimated using simulated future price paths under geometric Brownian motion.  
            - Reflects the average payoff discounted to today’s value.

            **Black-Scholes Price**  
            - Calculated using a closed-form formula (vanilla options).  
            - Acts as a benchmark.

            **Option Greeks**  
            - **Delta**: How much the option price changes with a $1 move in the stock price.  
            - **Gamma**: Rate of change of delta.  
            - **Vega**: Sensitivity to volatility.  
            - **Theta**: Time decay of the option’s value.  
            - **Rho**: Sensitivity to interest rates.

            **Distribution Histogram**  
            - The shape shows how asset prices might evolve over time.  
            - The **red dashed line** marks the **strike price (K)**.
              - For **calls**: More prices above K → higher payoff.  
              - For **puts**: More prices below K → higher payoff.

            **Volatility Impact**  
            - Higher volatility widens the curve — more upside and downside potential.

            **Simulation Count**  
            - Larger numbers make the estimate more stable (law of large numbers), but slower.
            """)
