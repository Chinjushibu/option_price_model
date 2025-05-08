# 📈 Option Pricing Models: Mibian, Black-Scholes, and Heston

This Python project dynamically calculates **Implied Volatility (IV)**, **Greeks**, and **option prices** using:
- 📊 Mibian (Black-Scholes IV)
- 🔬 Manual Black-Scholes for Greeks
- 🧠 QuantLib’s Heston stochastic volatility model

---

## ⚙️ Features

- Dynamically accepts inputs (Spot, Strike, IV, etc.)
- Calculates IV for call & put using **Mibian**
- Computes option Greeks (Δ, Γ, Θ, Vega, Rho)
- Calculates theoretical prices using **Heston model**
- Fully modular and reusable

---

## 🚀 Setup Instructions

### 1. 🔁 Clone this repository

git clone https://github.com/yourusername/option-pricing-models.git
cd option-pricing-models
2. 🧪 Create Virtual Environment (Recommended)


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. 📦 Install Required Libraries

pip install mibian scipy QuantLib-Python
🧠 How It Works
Input Parameters:
You can provide these interactively or hardcoded:

Spot Price (S)

Strike Price (K)

Call & Put Market Price

Risk-free Interest Rate (r)

Dividend Yield

Days to Expiry

Output:
Call & Put Implied Volatility (IV)

Call & Put Greeks

Heston Call & Put Prices

▶️ Usage
Run the main file:

python option_models.py
You’ll be prompted to enter:

Spot price

Strike price

Call & Put price

Days to expiry

Risk-free rate

🧪 Example Output

Call IV: 18.62%
Put IV: 22.14%
Call Greeks: Δ=0.66, Γ=0.0002, Θ=-3.14, Vega=0.84, Rho=7.91
Put Greeks: Δ=-0.34, Γ=0.0002, Θ=-2.88, Vega=0.84, Rho=-6.82
Heston Call Price: ₹1428.94
Heston Put Price: ₹2.01
🛠️ File Structure

option-pricing-models/
│
├── option_models.py      # Main script
├── README.md             # This documentation
└── .gitignore            # Python & env exclusions

🧠 Why Use the Heston Model?
While Black-Scholes assumes constant volatility, the Heston model adds a stochastic process to volatility. It’s more accurate in real markets, especially near expiry or with skewed IVs.

👨‍💻 Author
Chinju Shibu
Python Developer | AI-ML Enthusiast
LinkedIn
📧 chinjushibu912@gmail.com

📜 License
This project is open-source under the MIT License.


