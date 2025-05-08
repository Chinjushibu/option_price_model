
# 📈 Option Pricing & Greeks Analysis Tool

A Python-based tool for calculating Implied Volatility (IV), Option Greeks (Delta, Gamma, Theta, Vega, Rho), and theoretical option prices using both the **Black-Scholes** and **Heston** stochastic volatility models.

---

## 🔧 Features

- ✅ Dynamic user input support for:
  - Spot price
  - Strike price
  - Interest rate
  - Time to expiry
  - Option prices
- 📊 IV calculation using **Mibian** for both calls and puts
- 📉 Black-Scholes Greeks calculator
- ⚙️ Heston model pricing using **QuantLib**
- 📦 Modular and easy-to-read codebase

---

## 📁 Project Structure



option\_analysis/
│
├── option\_models.py       # Main script with dynamic input and calculations
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignored files
└── README.md              # This file





## 🖥️ How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/option-analysis.git
   cd option-analysis

2. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script**:

   ```bash
   python option_models.py
   ```

---

## ⚙️ Requirements

* Python 3.8+
* [QuantLib](https://www.quantlib.org/)
* [Mibian](https://pypi.org/project/mibian/)
* SciPy, NumPy

To install manually:

```bash
pip install mibian QuantLib-Python scipy numpy
```

---

## 📌 Example Use Case

Given:

* Spot Price: ₹24,401.2
* Strike Price: ₹23,000
* Call Price: ₹1429.37
* Put Price: ₹1.72
* Risk-Free Rate: 6%
* Time to Expiry: 7 Days

The script will output:

* Implied Volatility for both call and put
* Black-Scholes Greeks
* Heston model prices

---

## 📈 Why Use the Heston Model?

Unlike Black-Scholes, the Heston model:

* Allows for **stochastic volatility** (volatility can change over time)
* Is more realistic for pricing options in volatile markets
* Provides better alignment with market-observed option prices

---

## 🧠 Author

**Chinju Shibu**
Python Developer & ML Enthusiast
📧 [chinjushibu912@gmail.com](mailto:chinjushibu912@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/chinju-shibu-aba059218/)

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---
