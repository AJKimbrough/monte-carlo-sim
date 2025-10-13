# 📈 Monte Carlo Option Pricing Simulator

An interactive Streamlit-based web application to simulate and price European options using Monte Carlo methods and compare the results with the Black-Scholes analytical model. This dashboard also calculates core option Greeks and visualizes the distribution of terminal prices.

---

## 🚀 Features

- 🧠 **Monte Carlo simulation** for European call and put options
- 📘 **Black-Scholes formula** benchmark for accuracy comparison
- 🧮 **Option Greeks**: Delta, Gamma, Vega, Theta, Rho
- 📊 **Interactive histogram** of simulated end prices ($S_T$)
- 📥 **Downloadable CSV** of simulated prices
- 💡 **Collapsible sections** for input help and result interpretation

---

## 🖥️ Live Demo

▶️ **Coming soon via Streamlit Cloud**  
*(Will be linked here once deployed)*

---

## 🛠️ Installation

Clone this repo and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/monte-carlo-option-pricing.git
cd monte-carlo-option-pricing
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
streamlit run app/dashboard.py
```

The app will launch in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
monte-carlo-option-pricing/
├── app/
│   └── dashboard.py          # Main Streamlit app
├── src/
│   ├── monte_carlo.py        # Monte Carlo engine
│   ├── black_scholes.py      # Black-Scholes pricing
│   └── greeks.py             # Greeks calculation
├── .streamlit/
│   └── config.toml           # Theme settings
├── plots/                    # (optional) output histograms
├── requirements.txt
└── README.md
```

---

## 📘 How to Use

1. Input your simulation parameters in the sidebar
2. Click **🔄 Run Simulation**
3. View:
   - Monte Carlo and Black-Scholes prices
   - Option Greeks
   - Histogram of simulated prices
4. Download results as CSV

---

## 📈 Option Greeks Explained

| Greek   | Meaning                             |
|---------|-------------------------------------|
| Delta   | Sensitivity to underlying price     |
| Gamma   | Sensitivity of delta                |
| Vega    | Sensitivity to volatility           |
| Theta   | Time decay of the option            |
| Rho     | Sensitivity to interest rate        |

All computed using the Black-Scholes model.

---

## 📘 License

This project is licensed under the MIT License.

---

## ✍️ Author

**Amber Kimbrough**  
Quant-minded Software Engineer and HWPO Training Ambassador  
[LinkedIn](https://www.linkedin.com/in/amber-kimbrough) | [GitHub](https://github.com/AJKimbrough)

---

## 📌 TODO / Roadmap

- [ ] Add support for Asian and Barrier options
- [ ] Add Yahoo Finance integration for live S₀ / σ
- [ ] Deploy to Streamlit Cloud
- [ ] Add dark/light theme toggle
