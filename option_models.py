# adjusted code with new dynamic inputs of spot, strike,expiry dates and heston model parameters

import mibian
import math
from scipy.stats import norm
import QuantLib as ql

# === USER INPUT ===
S = float(input("Spot price (S): "))
K = float(input("Strike price (K): "))
r = float(input("Risk-free rate (%) (e.g. 6): "))
T_days = int(input("Days to expiry (e.g. 7): "))
div_yield = float(input("Dividend yield (%) [0 if none]: "))

call_price = float(input("Call Option Market Price: "))
put_price = float(input("Put Option Market Price: "))

# Optional: Heston parameters
print("\n-- Heston Model Parameters --")
v0 = float(input("Initial variance v0 (e.g. 0.01): "))
kappa = float(input("Mean reversion speed κ (e.g. 2.0): "))
theta = float(input("Long-term variance θ (e.g. 0.02): "))
sigma = float(input("Volatility of volatility σ (e.g. 0.3): "))
rho = float(input("Correlation ρ (e.g. -0.5): "))

# === Convert rates ===
T = T_days / 365
r_decimal = r / 100
q = div_yield / 100

# === Step 1: Calculate IVs ===
call_iv_model = mibian.BS([S, K, r, T_days], callPrice=call_price)
put_iv_model = mibian.BS([S, K, r, T_days], putPrice=put_price)

call_iv = call_iv_model.impliedVolatility / 100 if call_iv_model.impliedVolatility else None
put_iv = put_iv_model.impliedVolatility / 100 if put_iv_model.impliedVolatility else None

print(f"\nCall IV: {call_iv * 100:.2f}%" if call_iv else "Call IV not available")
print(f"Put IV: {put_iv * 100:.2f}%" if put_iv else "Put IV not available")

# === Step 2: Greeks ===


def black_scholes_greeks(option_type, S, K, T, r, iv, q=0.0):
    d1 = (math.log(S / K) + (r - q + 0.5 * iv**2) * T) / (iv * math.sqrt(T))
    d2 = d1 - iv * math.sqrt(T)

    if option_type == 'call':
        delta = math.exp(-q * T) * norm.cdf(d1)
        theta = (-S * norm.pdf(d1) * iv * math.exp(-q * T) / (2 * math.sqrt(T))
                 - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
        rho = K * T * math.exp(-r * T) * norm.cdf(d2) / 100
    else:
        delta = -math.exp(-q * T) * norm.cdf(-d1)
        theta = (-S * norm.pdf(d1) * iv * math.exp(-q * T) / (2 * math.sqrt(T))
                 + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365
        rho = -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100

    gamma = math.exp(-q * T) * norm.pdf(d1) / (S * iv * math.sqrt(T))
    vega = S * math.exp(-q * T) * norm.pdf(d1) * math.sqrt(T) / 100
    return round(delta, 4), round(gamma, 4), round(theta, 4), round(vega, 4), round(rho, 4)


if call_iv:
    call_greeks = black_scholes_greeks('call', S, K, T, r_decimal, call_iv, q)
    print("Call Greeks: Δ={}, Γ={}, Θ={}, Vega={}, Rho={}".format(*call_greeks))
else:
    print("Call Greeks could not be calculated")

if put_iv:
    put_greeks = black_scholes_greeks('put', S, K, T, r_decimal, put_iv, q)
    print("Put Greeks: Δ={}, Γ={}, Θ={}, Vega={}, Rho={}".format(*put_greeks))
else:
    print("Put Greeks could not be calculated")

# === Step 3: Heston Model Pricing ===


def heston_model_price(spot, strike, maturity_days, risk_free_rate, dividend_yield,
                       v0, kappa, theta, sigma, rho, is_call=True):
    calendar = ql.India()
    today = ql.Date.todaysDate()
    maturity = today + maturity_days
    ql.Settings.instance().evaluationDate = today

    S_handle = ql.QuoteHandle(ql.SimpleQuote(spot))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, ql.Actual365Fixed()))
    dividend_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend_yield, ql.Actual365Fixed()))

    process = ql.HestonProcess(flat_ts, dividend_ts, S_handle, v0, kappa, theta, sigma, rho)
    model = ql.HestonModel(process)
    engine = ql.AnalyticHestonEngine(model)

    payoff = ql.PlainVanillaPayoff(ql.Option.Call if is_call else ql.Option.Put, strike)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.EuropeanOption(payoff, exercise)
    option.setPricingEngine(engine)

    price = option.NPV()
    return round(price, 4) if price else 0.0


heston_call = heston_model_price(S, K, T_days, r_decimal, q, v0, kappa, theta, sigma, rho, is_call=True)
heston_put = heston_model_price(S, K, T_days, r_decimal, q, v0, kappa, theta, sigma, rho, is_call=False)

print(f"\nHeston Call Price: ₹{heston_call}")
print(f"Heston Put Price: ₹{heston_put}")
