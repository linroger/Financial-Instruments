import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import numpy as np
    from scipy.stats import norm
    import plotly.graph_objects as go
    return go, mo, norm, np

@app.cell
def _(mo):
    mo.md(
        r"""
        # Financial Instruments Midterm 2024 Solution
        """
    )
    return

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. True-False
        """
    )
    return

@app.cell
def _(mo):
    # 1.1 Short Straddle Risk
    # False. A short straddle involves selling a call and a put.
    # If the market moves significantly in either direction, losses can be unlimited (Call) or substantial (Put).
    # Selling before maturity exposes you to Vega risk and Gamma risk. If volatility spikes or price jumps, you lose.

    # 1.2 Sharpe Ratio
    # True (mostly). In the Black-Scholes world (continuous hedging, no arbitrage), the option is a redundant asset.
    # The instantaneous Sharpe ratio of any derivative equals the Sharpe ratio of the underlying.
    # (Expected Return - Risk Free) / Volatility * Elasticity / Elasticity = Same?
    # Let's verify: mu_option = r + Omega * (mu_stock - r).
    # Sharpe_opt = (mu_opt - r) / sigma_opt = Omega * (mu_stock - r) / (Omega * sigma_stock) = Sharpe_stock.
    # Yes.
    return

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Binomial Trees
        """
    )
    return

@app.cell
def _(go, mo, np):
    # Parameters
    S0 = 100.0
    r_cc = 0.02
    dt = 0.5 # 6 months

    # Period 1 (0 to 0.5)
    u1 = 1.20
    d1 = 0.90 # 1 - 0.10

    # Period 2 (0.5 to 1.0)
    u2 = 1.15
    d2 = 0.95 # 1 - 0.05

    # (b) Tree
    # Nodes:
    # t=0: 100
    # t=0.5: 120, 90
    # t=1:
    #   From 120: 120*1.15 = 138, 120*0.95 = 114
    #   From 90: 90*1.15 = 103.5, 90*0.95 = 85.5

    # (c) Risk Neutral Probabilities
    # p = (exp(r*dt) - d) / (u - d)
    # Period 1
    p1 = (np.exp(r_cc * dt) - d1) / (u1 - d1)
    # Period 2
    p2 = (np.exp(r_cc * dt) - d2) / (u2 - d2)

    # Probabilities of reaching terminal nodes from t=0 (Risk Neutral)
    # Nodes at T=1: [138, 114, 103.5, 85.5]
    # Path UU: p1 * p2
    # Path UD: p1 * (1-p2)
    # Path DU: (1-p1) * p2
    # Path DD: (1-p1) * (1-p2)

    # Analyst probs (Real World): q = 0.6
    q = 0.6
    # Path UU (Analyst): 0.6 * 0.6 = 0.36

    # (d) Options
    # Call K=120, Put K=100. Maturity 1 year.
    # Payoffs at t=1:
    # Node 138: C=18, P=0. Total=18.
    # Node 114: C=0, P=0. Total=0.
    # Node 103.5: C=0, P=0. Total=0.
    # Node 85.5: C=0, P=14.5. Total=14.5.

    # (ii) Price
    # Discounted Expected Value under Q
    V_UU = 18
    V_UD = 0
    V_DU = 0
    V_DD = 14.5

    E_V = p1*p2*V_UU + p1*(1-p2)*V_UD + (1-p1)*p2*V_DU + (1-p1)*(1-p2)*V_DD
    Price = E_V * np.exp(-r_cc * 1.0)

    # (iii) Arbitrage
    # Market Price = Price + 1.
    # Sell Strategy (Short Market, Long Synthetic).
    # Replicate at each node.

    mo.md(
        f"""
        **Binomial Tree Results:**
        *   $p_1$ (Risk Neutral, Period 1): {p1:.4f}
        *   $p_2$ (Risk Neutral, Period 2): {p2:.4f}
        *   Analyst Prob (Up): 0.6

        **Option Strategy:**
        *   Theoretical Price: {Price:.4f}
        *   Strategy if Market Price is {Price + 1:.4f}: Sell the package, Replicate.
        """
    )
    return (
        E_V,
        Price,
        S0,
        V_DD,
        V_DU,
        V_UD,
        V_UU,
        d1,
        d2,
        dt,
        p1,
        p2,
        q,
        r_cc,
        u1,
        u2,
    )

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Black-Scholes Hedging
        """
    )
    return

@app.cell
def _(mo, norm, np):
    # Parameters
    S = 50
    sigma = 0.30
    mu = 0.15
    r = 0.05
    T = 360/365.0 # 1 year approx? "one year to maturity (360 days)". Usually use T=1 or 360/365.
    # Let's assume T=1 roughly or exact fraction.
    T_days = 360
    T_years = T_days / 365.0
    K = 50 # ATM
    Shares = 1000

    # (a) Price and Hedge
    # Put Option Price
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T_years) / (sigma * np.sqrt(T_years))
    d2 = d1 - sigma * np.sqrt(T_years)

    Put_Price = K * np.exp(-r * T_years) * norm.cdf(-d2) - S * norm.cdf(-d1)
    Total_Value = Put_Price * Shares

    # Hedge (Short Put)
    # Delta of Short Put = - (Delta of Long Put) = - (N(d1) - 1) = 1 - N(d1).
    # Wait, Put Delta is N(d1) - 1. (Negative).
    # We sold the put. We are Short Put.
    # Our position delta is: -1 * (N(d1) - 1) = 1 - N(d1). (Positive).
    # To hedge (Delta Neutral), we need Negative Delta.
    # Sell Shares.
    # Number of shares to sell = Delta_Pos * 1000.

    Delta_Long_Put = norm.cdf(d1) - 1
    Delta_Short_Put = -Delta_Long_Put
    Shares_To_Sell = Delta_Short_Put * Shares

    # (b) 1 Day later
    S_new = 40
    T_new_days = 259
    # Wait, "after a day... now 259 days"?
    # 360 -> 359? Maybe typo in question "259"?
    # Or maybe huge time jump. "maintain the position ... over the first full day but after a day ... now 259 days".
    # That's a jump of 101 days?
    # "after a day" implies 1 day passed.
    # If T_new = 259, then time passed = 101 days.
    # Assuming question text is literal: T_new = 259/365.

    T_new_years = 259 / 365.0

    # New Price
    d1_new = (np.log(S_new/K) + (r + 0.5 * sigma**2) * T_new_years) / (sigma * np.sqrt(T_new_years))
    d2_new = d1_new - sigma * np.sqrt(T_new_years)

    Put_Price_New = K * np.exp(-r * T_new_years) * norm.cdf(-d2_new) - S_new * norm.cdf(-d1_new)

    # Value of Hedge
    # Portfolio: Short Put + Short Stock (Shares_To_Sell) + Cash (Proceeds from Short Stock + Option Premium)
    # Initial Cash = Total_Value + (Shares_To_Sell * S)
    # Interest on Cash for period (360 - 259 = 101 days).
    # Value_Hedge_t = Cash * exp(r * dt) - Shares_To_Sell * S_new - Put_Price_New * Shares

    dt = (360 - 259) / 365.0
    Cash_0 = Total_Value + Shares_To_Sell * S
    Cash_t = Cash_0 * np.exp(r * dt)

    Liability_Stock = Shares_To_Sell * S_new
    Liability_Option = Put_Price_New * Shares

    Net_Value = Cash_t - Liability_Stock - Liability_Option

    mo.md(
        f"""
        **Black-Scholes Results:**
        *   Initial Put Price: {Put_Price:.4f}
        *   Shares to Sell (Hedge): {Shares_To_Sell:.4f}
        *   New Put Price (S=40): {Put_Price_New:.4f}
        *   Hedge Performance (Net Value): {Net_Value:.4f}
        """
    )
    return (
        Cash_0,
        Cash_t,
        Delta_Long_Put,
        Delta_Short_Put,
        K,
        Liability_Option,
        Liability_Stock,
        Net_Value,
        Put_Price,
        Put_Price_New,
        S,
        S_new,
        Shares,
        Shares_To_Sell,
        T,
        T_days,
        T_new_days,
        T_new_years,
        T_years,
        Total_Value,
        d1,
        d1_new,
        d2,
        d2_new,
        dt,
        mu,
        r,
        sigma,
    )

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Swaps and Forwards
        """
    )
    return

@app.cell
def _(mo, np):
    # 4(a) Forward Rate
    # Current Spot S0 = 1.20 USD/EUR
    # Swap Price = 0.
    # Swap Rate = 1.209 (Fixed USD paid for 1 EUR received?)
    # "exchange a fixed 1.209 dollars for each euro".
    # Usually Swap Rate is the fixed rate.
    # Payoffs: (F_t - K) or (K - F_t).
    # If Value is 0, PV(Fixed) = PV(Floating/Forward).
    # Dates: 0.5, 1.0.
    # Fwd_0.5 = 1.206.
    # r_0.5 = 5%. r_1.0 = 6%.
    # Calculate Fwd_1.0.

    # PV(Fixed Flows) = 1.209 * exp(-0.05*0.5) + 1.209 * exp(-0.06*1.0)
    # PV(Floating Flows) = 1.206 * exp(-0.05*0.5) + Fwd_1 * exp(-0.06*1.0)
    # Equate and solve for Fwd_1.

    swap_rate = 1.209
    fwd_05 = 1.206
    r_05 = 0.05
    r_10 = 0.06

    df_05 = np.exp(-r_05 * 0.5)
    df_10 = np.exp(-r_10 * 1.0)

    # 1.209 * df_05 + 1.209 * df_10 = 1.206 * df_05 + F_1 * df_10
    # 1.209 * (df_05 + df_10) = 1.206 * df_05 + F_1 * df_10
    # F_1 * df_10 = 1.209 * (df_05 + df_10) - 1.206 * df_05
    # F_1 = (1.209 * (df_05 + df_10) - 1.206 * df_05) / df_10

    numerator = 1.209 * (df_05 + df_10) - 1.206 * df_05
    F_1 = numerator / df_10

    # 4(b) Value after Spot Move
    # Spot moves to 1.15 (from 1.20).
    # No yield curve change.
    # Forward rates change?
    # Yes, F = S * exp((r_d - r_f)T).
    # If S changes, F changes proportionally (assuming r_d, r_f constant).
    # So F_new = F_old * (S_new / S_old).

    S_old = 1.20
    S_new = 1.15
    ratio = S_new / S_old

    F_05_new = fwd_05 * ratio
    F_10_new = F_1 * ratio

    # Contract: Sell Dollars for Euros?
    # "exchange a fixed 1.209 dollars for each euro".
    # "enter ... to sell dollars for Euros".
    # Sell USD, Buy EUR.
    # Receive EUR (Value S_new), Pay Fixed USD (1.209).
    # Actually, usually swap is defined on Notional. Assuming 1 Euro notional per period.
    # Cash Flow at t: S_t - 1.209 (in USD terms).
    # Value = PV(F_new_t - 1.209).

    val_05 = (F_05_new - swap_rate) * df_05
    val_10 = (F_10_new - swap_rate) * df_10

    total_val = val_05 + val_10

    mo.md(
        f"""
        **Swap Results:**
        *   1-Year Forward Rate: {F_1:.4f}
        *   Value after Spot Drop (per EUR Notional): {total_val:.4f} USD.
        """
    )
    return (
        F_05_new,
        F_1,
        F_10_new,
        S_new,
        S_old,
        df_05,
        df_10,
        fwd_05,
        numerator,
        r_05,
        r_10,
        ratio,
        swap_rate,
        total_val,
        val_05,
        val_10,
    )

if __name__ == "__main__":
    app.run()
