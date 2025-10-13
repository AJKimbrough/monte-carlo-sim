import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from monte_carlo import monte_carlo_option_price
from black_scholes import black_scholes_price

st.set_page_config(page_title="Option Pricing Simulator", layout="wide")
st.markdown("<h1 style='text-align: center;'>Monte Carlo Option Pricing Simulator</h1>", unsafe_allow_html=True)
st.markdown("### Simulate and compare European option prices using Monte Carlo and Black-Scholes models.")

with st.expander("🧪 How to Use This Dashboard", expanded=False):
    st.markdown("""
    Use the **sidebar** to set your option pricing simulation parameters:

    - **Initial Stock Price (S₀)** – Current price of the asset  
    - **Strike Price (K)** – Exercise price of the option  
    - **Time to Maturity (T)** – In years (e.g. 0.5 = 6 months)  
    - **Risk-free Rate (r)** – Annualized interest rate (e.g., 0.05)  
    - **Volatility (σ)** – As a decimal (e.g., 0.2 for 20%)  
    - **Option Type** – 'Call' or 'Put'  
    - **Simulations** – Number of Monte Carlo paths to run

    After entering inputs, click **🔄 Run Simulation** to:
    - Get a simulated option price (Monte Carlo)
    - Compare to Black-Scholes price
    - View the distribution of final simulated prices ($S_T$)
    """)



# --- Sidebar / Inputs ---
st.sidebar.header("Simulation Parameters")

S0 = st.sidebar.number_input("Initial Stock Price (S₀)", value=100.0, min_value=0.01)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, min_value=0.01)
T = st.sidebar.number_input("Time to Maturity (T in years)", value=1.0, min_value=0.01)
r = st.sidebar.number_input("Risk-free Rate (r)", value=0.05, format="%.4f")
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2, format="%.4f")
option_type = st.sidebar.radio("Option Type", ["call", "put"], horizontal=True)
N = st.sidebar.slider("Number of Simulations", min_value=1000, max_value=500000, value=100000, step=10000)

if st.sidebar.button("🔄 Run Simulation"):
    with st.spinner("Simulating..."):
        mc_price, ST = monte_carlo_option_price(S0, K, T, r, sigma, N, option_type)
        bs_price = black_scholes_price(S0, K, T, r, sigma, option_type)

        col1, col2 = st.columns(2)
        col1.metric(label="Monte Carlo Price", value=f"${mc_price:.4f}")
        col2.metric(label="Black-Scholes Price", value=f"${bs_price:.4f}")

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

        with st.expander("How to Interpret the Results", expanded=False):
            st.markdown("""
            **Monte Carlo Price**  
            - Estimated using simulated future price paths under geometric Brownian motion.
            - Reflects the average payoff discounted to today’s value.

            **Black-Scholes Price**  
            - Calculated using a closed-form formula.
            - Acts as a benchmark — if your Monte Carlo estimate is close, your model is behaving as expected.

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



        st.caption("Simulation assumes geometric Brownian motion with risk-neutral drift.")
