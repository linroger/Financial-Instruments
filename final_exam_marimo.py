import math
import marimo as mo
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

from final_exam_utils import (
    forward_rate,
    currency_swap_fixed_rate,
    currency_swap_value,
    merton_model,
    senior_subordinated_values,
    european_call_binomial,
    american_call_with_dividend,
    structured_product_price,
    structured_product_delta_beta,
)


def call_price_bs(S: float, K: float, r: float, sigma: float, T: float) -> float:
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


@mo.app()
def app():
    pd.set_option("display.float_format", lambda x: f"{x:,.4f}")

    # Question 2
    S0_fx = 1.1
    rd, rf = 0.04, 0.05
    maturities = [0.5, 1.0, 1.5]
    forwards = [forward_rate(S0_fx, rd, rf, t) for t in maturities]
    forward_df = pd.DataFrame({"Maturity": maturities, "Forward": forwards})
    cashflows_eur = [2.5, 2.5, 102.5]
    k_swap = currency_swap_fixed_rate(S0_fx, rd, rf, cashflows_eur, maturities)
    swap_summary = pd.DataFrame(
        {
            "Item": ["Swap rate", "Principal swapped at spot PV", "MTM when rates converge"],
            "USD": [
                k_swap,
                currency_swap_value([100], [1.5], rd, k_swap, S0_fx),
                currency_swap_value(cashflows_eur, maturities, 0.04, k_swap, S0_fx),
            ],
        }
    )

    fx_plot = px.line(forward_df, x="Maturity", y="Forward", markers=True, title="Forward FX curve")

    # Question 3
    asset_value = 500
    asset_vol = 0.25
    r = 0.02
    T = 7
    face_value = 400
    shares = 500_000
    merton_res = merton_model(asset_value, face_value, asset_vol, r, T, shares)
    equity_df = pd.DataFrame(
        {
            "Metric": [
                "Equity value", "Share price", "Equity volatility", "Debt value", "Debt yield", "Default probability", "Debt spread",
            ],
            "Value": [
                merton_res.equity_value,
                merton_res.share_price,
                merton_res.equity_vol,
                merton_res.debt_value,
                merton_res.debt_yield,
                merton_res.default_prob,
                merton_res.debt_yield - r,
            ],
        }
    )

    senior_val, sub_val = senior_subordinated_values(asset_value, face_value / 2, face_value / 2, asset_vol, r, T)
    senior_yield = -math.log(senior_val / (face_value / 2)) / T
    sub_yield = -math.log(sub_val / (face_value / 2)) / T
    tranche_df = pd.DataFrame(
        {
            "Tranche": ["Senior", "Subordinated"],
            "Value": [senior_val, sub_val],
            "Yield": [senior_yield, sub_yield],
            "Spread": [senior_yield - r, sub_yield - r],
        }
    )

    # Question 4
    S0 = 100
    u, d = 1.2, 1 / 1.2
    K = 100
    r_binom = 0.02
    p = (math.exp(r_binom) - d) / (u - d)
    call_euro_2y = european_call_binomial(S0, K, r_binom, u, d, 2)
    price_am_div, stock_tree = american_call_with_dividend(S0, K, r_binom, u, d, 3, dividend_time=2, dividend_amount=10, threshold=100)
    tree_df = pd.DataFrame({"State": ["dd", "du", "ud", "uu"], "Price after dividend": stock_tree[2]})
    payoff_plot = go.Figure()
    terminal_prices = np.linspace(50, 170, 200)
    payoff_plot.add_trace(go.Scatter(x=terminal_prices, y=np.maximum(terminal_prices - K, 0), name="Call payoff"))
    payoff_plot.update_layout(title="Call payoff", xaxis_title="Terminal price", yaxis_title="Payoff")

    # Question 5
    S0_idx = 1000
    r_idx = 0.02
    T_idx = 1
    put1, put2 = 50, 188
    K1, K2 = 1000, 1200
    product_price, call1, call2 = structured_product_price(S0_idx, r_idx, T_idx, put1, put2, K1, K2)

    prices_df = pd.DataFrame(
        {"Item": ["Call 1000", "Call 1200", "Structured price"], "Value": [call1, call2, product_price]}
    )

    index_grid = np.linspace(600, 1600, 240)
    returns = (index_grid - S0_idx) / S0_idx
    payoff = []
    for s, R in zip(index_grid, returns):
        if R < 0:
            payoff.append(1000)
        elif R <= 0.2:
            payoff.append(1000 + 2000 * R)
        else:
            payoff.append(1400)
    payoff_fig = go.Figure()
    payoff_fig.add_trace(go.Scatter(x=index_grid, y=payoff, name="Structured payoff"))
    payoff_fig.update_layout(title="Structured product payoff", xaxis_title="Index at maturity", yaxis_title="Payoff ($)")

    sigma = 0.30
    call1_theory = call_price_bs(S0_idx, K1, r_idx, sigma, T_idx)
    call2_theory = call_price_bs(S0_idx, K2, r_idx, sigma, T_idx)
    product_bs = math.exp(-r_idx * T_idx) * 1000 + 2 * call1_theory - 2 * call2_theory
    delta_1000, beta_1000 = structured_product_delta_beta(S0_idx, r_idx, sigma, T_idx, K1, K2)
    delta_1300, beta_1300 = structured_product_delta_beta(1300, r_idx, sigma, T_idx, K1, K2)

    hedge_df = pd.DataFrame(
        {
            "Underlying": ["1000", "1300"],
            "Delta": [delta_1000, delta_1300],
            "Beta": [beta_1000, beta_1300],
        }
    )

    return mo.vstack(
        [
            mo.md("# Financial Instruments Final Exam — compact marimo walkthrough"),
            mo.md("## Question 2: FX forwards and swap"),
            mo.ui.dataframe(forward_df),
            mo.ui.dataframe(swap_summary),
            mo.ui.plotly(fx_plot),
            mo.md("## Question 3: Structural model"),
            mo.ui.dataframe(equity_df),
            mo.ui.dataframe(tranche_df),
            mo.md("## Question 4: Binomial pricing with dividend"),
            mo.ui.dataframe(tree_df),
            mo.md(f"Risk-neutral probability p = {p:.4f}, European 2y call = {call_euro_2y:.4f}, American with dividend = {price_am_div:.4f}"),
            mo.ui.plotly(payoff_plot),
            mo.md("## Question 5: Structured product"),
            mo.ui.dataframe(prices_df),
            mo.ui.plotly(payoff_fig),
            mo.md(f"Black–Scholes valuation = {product_bs:.2f}"),
            mo.ui.dataframe(hedge_df),
        ]
    )


if __name__ == "__main__":
    mo.main()
