import math
import mibian
import QuantLib as ql
from  scipy.stats import norm

# Black-Scholes model for Greeks


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

# Implied volatility using mibian


def get_implied_volatility(S, K, T, r, option_price, option_type):
    if option_type == 'call':
        option = mibian.BS([S, K, r * 100, T * 365], callPrice=option_price)
    elif option_type == 'put':
        option = mibian.BS([S, K, r * 100, T * 365], putPrice=option_price)
    return option.impliedVolatility

# Heston model using QuantLib


def heston_option_price(option_type, S, K, T, r, sigma):
    # Dates setup
    calendar = ql.TARGET()
    today = ql.Date.todaysDate()
    ql.Settings.instance().evaluationDate = today
    maturity_date = today + int(T * 365)

    # Option setup
    payoff = ql.PlainVanillaPayoff(ql.Option.Call if option_type == 'call' else ql.Option.Put, K)
    exercise = ql.EuropeanExercise(maturity_date)
    european_option = ql.VanillaOption(payoff, exercise)

    # Heston process setup (basic example)
    v0 = sigma**2     # Initial variance
    kappa = 2.0       # Speed of mean reversion
    theta = sigma**2  # Long-term variance
    sigma_v = 0.5     # Vol of variance
    rho = -0.75       # Correlation

    spot_handle = ql.QuoteHandle(ql.SimpleQuote(S))
    rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, r, ql.Actual365Fixed()))
    div_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.0, ql.Actual365Fixed()))
    heston_process = ql.HestonProcess(rate_handle, div_handle, spot_handle, v0, kappa, theta, sigma_v, rho)
    heston_model = ql.HestonModel(heston_process)
    engine = ql.AnalyticHestonEngine(heston_model)

    european_option.setPricingEngine(engine)
    return european_option.NPV()

# Main


def main():
    # Inputs
    S = 24756.75          # Spot price
    K = 24750             # Strike price
    T = 2 / 365           # Time to maturity (2 days)
    r = 0.05             # Risk-free rate (9%)
    call_price = 177.15
    put_price = 214.35

    # Get IVs
    call_iv = get_implied_volatility(S, K, T, r, call_price, 'call')
    put_iv = get_implied_volatility(S, K, T, r, put_price, 'put')
    print(f"Implied Volatility (Call): {call_iv:.2f}%")
    print(f"Implied Volatility (Put): {put_iv:.2f}%")

    # Greeks
    #
    delta_c, gamma_c, theta_c, vega_c, rho_c = black_scholes_greeks( 'call', S, K, T, r, call_iv / 100 )
    delta_p, gamma_p, theta_p, vega_p, rho_p = black_scholes_greeks( 'put', S, K, T, r, put_iv / 100 )

    print("\nBlack-Scholes Greeks (Call):")
    print(f"Delta: {delta_c:.2f}, Gamma: {gamma_c:.5f}, Theta: {theta_c:.2f}, Vega: {vega_c:.2f}, Rho : {rho_c:.2f}")
    print("\nBlack-Scholes Greeks (Put):")
    print(f"Delta: {delta_p:.2f}, Gamma: {gamma_p:.5f}, Theta: {theta_p:.2f}, Vega: {vega_p:.2f}, Rho : {rho_p:.2f}")

    # Heston Model Price
    call_heston = heston_option_price('call', S, K, T, r, call_iv / 100)
    put_heston = heston_option_price('put', S, K, T, r, put_iv / 100)

    print(f"\nHeston Model Call Price : {call_heston :.2f}")
    print(f"Heston Model Put Price : {put_heston :.2f}")


if __name__ == "__main__":
    main()
