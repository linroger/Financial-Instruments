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
        # Financial Instruments Final Exam 2024 Solution
        """
    )
    return

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. Short Answer
        """
    )
    return

@app.cell
def _(mo):
    # 1(a) Monte Carlo vs Binomial
    # Advantages MC: Handles path dependence (Asian options) easily, handles multiple underlying assets easily (correlation).
    # Disadvantages MC: Hard to handle American options (early exercise) compared to Binomial. Slower convergence (1/sqrt(N)).

    # 1(b) ATM Call vs ATM Put
    # Put-Call Parity: C - P = S - K * exp(-rT).
    # If ATM (S=K): C - P = S - S * exp(-rT) = S * (1 - exp(-rT)).
    # If r > 0, C - P > 0, so Call > Put.
    # Call has higher theoretical value.

    # 1(c) Futures as Predictors
    # Futures price F = S * exp((r-q)T).
    # It reflects the cost of carry (interest rate differential), not necessarily expectation of future spot.
    # Under risk neutrality, F = E_Q[S_T]. Under physical measure, E_P[S_T] includes risk premium.
    return

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Swaps and Forwards
        """
    )
    return

@app.cell
def _(mo, np):
    # Parameters
    S0 = 1.1 # USD/EUR
    # Dollar Rates
    rD_05 = 0.04
    rD_10 = 0.04
    rD_15 = 0.04
    # Euro Rates
    rE_05 = 0.05
    rE_10 = 0.05
    rE_15 = 0.05

    T1 = 0.5; T2 = 1.0; T3 = 1.5

    # (a) Forward Rates
    # F = S * exp((rD - rE)T)
    F1 = S0 * np.exp((rD_05 - rE_05) * T1)
    F2 = S0 * np.exp((rD_10 - rE_10) * T2)
    F3 = S0 * np.exp((rD_15 - rE_15) * T3)

    # (b) Swap Rate
    # Swap Euros (Coupons + Principal) for Dollars (Fixed Rate).
    # Firm has EUR Bond: 100m Face, 5% Coupon (Annual rate, semi-annual pay).
    # Coupon per period = 100 * 0.05 / 2 = 2.5m EUR.
    # Principal = 100m EUR.
    # Payments: t=0.5 (2.5), t=1.0 (2.5), t=1.5 (102.5).

    # PV of EUR Payments (in EUR):
    # Since Coupon = rE (5%), and yield is 5% flat, Bond trades at Par.
    # PV_EUR = 100m EUR.
    # PV in USD = 100m * 1.1 = 110m USD.

    # Swap structure:
    # Pay USD coupons (Fixed C_USD) + Principal (Notional_USD) at end?
    # Usually swap principal matches initial exchange value.
    # Notional_USD = 110m.
    # We want to find Swap Rate c_USD such that PV(USD Flows) = 110m.
    # PV_USD = C_USD/2 * Sum(DF_USD) + Notional * DF_USD(T)
    # If yield is flat 4%, then par swap rate is 4%.
    # Let's verify.
    # 110 = (c * 110 / 2) * (D1+D2+D3) + 110 * D3.
    # Divide by 110: 1 = c/2 * Sum(D) + D3.
    # This implies c = (1 - D3) / (0.5 * Sum(D)).
    # Since yield is flat 4%, this will recover 4%.

    D1 = np.exp(-rD_05 * T1)
    D2 = np.exp(-rD_10 * T2)
    D3 = np.exp(-rD_15 * T3)
    sum_D = D1 + D2 + D3

    c_swap = (1.0 - D3) / (0.5 * sum_D)

    # (c) Off-Market Principal Swap
    # Swap coupons at c_swap (4%).
    # Swap Principal at Current Exchange Rate (1.1).
    # Receive: 2.5m EUR coupons, 100m EUR Principal.
    # Pay: USD Coupons (Fixed), USD Principal (converted at 1.1).
    # USD Principal Payment = 100m * 1.1 = 110m USD.
    # This is exactly what we assumed in (b).
    # The "Market" swap involves exchanging principal at maturity?
    # Standard Currency Swap involves:
    # Initial: Receive P_USD, Pay P_EUR.
    # Final: Pay P_USD, Receive P_EUR.
    # Here firm has EUR bond. Wants to "Swap payments in Euros for dollars".
    # Means: Firm Pays EUR to Bank, Bank Pays USD to Firm.
    # Firm uses Bank's USD to pay something else? Or converts liability?
    # Firm receives USD flows.
    # Value of EUR Leg (Given to Bank) = 110m USD.
    # Value of USD Leg (Received from Bank):
    # Coupons: c_swap on Notional? Principal: Notional.
    # If Notional = 110m, and Rate = 4%, Value = 110m.
    # Profit = 0. (Fair deal).

    # (d) Rates Move
    # New Rates: USD 4%, EUR 4%. (EUR drops).
    # Value of Swap to Firm (Receive USD, Pay EUR).
    # USD Leg Value: Rates same (4%). Value = 110m USD.
    # EUR Leg Value (Liability): Rates moved to 4%.
    # Bond (5% coupon) valued at 4% yield will trade Premium.
    # PV_EUR_New = 2.5 * D1_E + 2.5 * D2_E + 102.5 * D3_E.
    # Discount at 4%.
    # Value in EUR > 100m.
    # Value in USD = Value_EUR * S0 (assuming S0 same? or S changed? "yields... move... S not mentioned").
    # Usually S jumps if rates jump. Assuming S=1.1 constant.

    rE_new = 0.04
    D1_E = np.exp(-rE_new * T1)
    D2_E = np.exp(-rE_new * T2)
    D3_E = np.exp(-rE_new * T3)

    Val_EUR_Leg = 2.5 * D1_E + 2.5 * D2_E + 102.5 * D3_E
    Val_EUR_USD = Val_EUR_Leg * S0

    Swap_Value = 110.0 - Val_EUR_USD

    mo.md(
        f"""
        **Swap Analysis:**
        *   Forward Rates: 0.5yr={F1:.4f}, 1.0yr={F2:.4f}, 1.5yr={F3:.4f}.
        *   Swap Rate (USD): {c_swap:.4%}.
        *   (d) New EUR Leg Value: {Val_EUR_Leg:.4f} M EUR.
        *   Swap Value (Receive USD, Pay EUR): {Swap_Value:.4f} M USD.
        """
    )
    return (
        D1,
        D1_E,
        D2,
        D2_E,
        D3,
        D3_E,
        F1,
        F2,
        F3,
        S0,
        Swap_Value,
        T1,
        T2,
        T3,
        Val_EUR_Leg,
        Val_EUR_USD,
        c_swap,
        rD_05,
        rD_10,
        rD_15,
        rE_05,
        rE_10,
        rE_15,
        rE_new,
        sum_D,
    )

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Corporate Debt (Merton Model)
        """
    )
    return

@app.cell
def _(mo, norm, np):
    # Parameters
    V = 500.0
    sigma_V = 0.25
    r = 0.02
    T = 7.0
    Debt_Face = 400.0 * 1.0 # 400m
    Shares = 0.5 # 500,000 shares = 0.5 million shares

    # (a) Price of Stock (Call Option on V)
    d1 = (np.log(V/Debt_Face) + (r + 0.5 * sigma_V**2) * T) / (sigma_V * np.sqrt(T))
    d2 = d1 - sigma_V * np.sqrt(T)

    E_val = V * norm.cdf(d1) - Debt_Face * np.exp(-r * T) * norm.cdf(d2)
    Price_Per_Share = E_val / Shares

    # (b) Volatility of Equity
    # Sigma_E = N(d1) * (V / E) * Sigma_V
    Sigma_E = norm.cdf(d1) * (V / E_val) * sigma_V

    # (c) Debt Risk Premium
    # D_val = V - E_val
    D_val = V - E_val
    # Yield y: D = F * exp(-yT) => y = -ln(D/F)/T
    y = -np.log(D_val / Debt_Face) / T
    Spread = y - r

    # Prob Default (Risk Neutral) = N(-d2)
    PD = norm.cdf(-d2)

    # (d) Seniority
    # Senior Debt (K1 = 200). Junior Debt (K2 = 400 total? or K2=200 incremental?)
    # "Half of the debt... has senior claim".
    # Face Senior = 200. Face Junior = 200. Total = 400.
    # Senior Value D1: Riskless? No, firm V can drop below 200.
    # D1 is equivalent to Debt with Face 200 on V.
    # D1_val = V - Call(V, 200).

    K1 = 200.0
    d1_s = (np.log(V/K1) + (r + 0.5 * sigma_V**2) * T) / (sigma_V * np.sqrt(T))
    d2_s = d1_s - sigma_V * np.sqrt(T)
    E_hypothetical = V * norm.cdf(d1_s) - K1 * np.exp(-r * T) * norm.cdf(d2_s)
    D1_val = V - E_hypothetical

    # Junior Value D2 = Total Debt - D1
    D2_val = D_val - D1_val

    y1 = -np.log(D1_val / K1) / T
    y2 = -np.log(D2_val / (Debt_Face - K1)) / T

    # Probability of Default for Firm?
    # Default if V < 400. Same as before.
    # Default on Senior? V < 200.

    mo.md(
        f"""
        **Merton Model Results:**
        *   Stock Price: {Price_Per_Share:.2f}
        *   Equity Volatility: {Sigma_E:.2%}
        *   Debt Value: {D_val:.2f}, Yield: {y:.2%}, Spread: {Spread:.2%}
        *   Probability of Default: {PD:.2%}

        **Seniority:**
        *   Senior Debt Value: {D1_val:.2f}, Yield: {y1:.2%}
        *   Junior Debt Value: {D2_val:.2f}, Yield: {y2:.2%}
        """
    )
    return (
        D1_val,
        D2_val,
        D_val,
        Debt_Face,
        E_hypothetical,
        E_val,
        K1,
        PD,
        Price_Per_Share,
        Shares,
        Sigma_E,
        Spread,
        T,
        V,
        d1,
        d1_s,
        d2,
        d2_s,
        r,
        sigma_V,
        y,
        y1,
        y2,
    )

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4. Options and Dividends
        """
    )
    return

@app.cell
def _(mo, np):
    # 4(a) European Call 2yr
    S0 = 100
    u = 1.2
    d = 1.0/1.2
    r = 0.02
    T = 2 # years

    p_rn = (np.exp(r) - d) / (u - d)

    # Tree T=2
    # Nodes: UU, UD, DD
    Suu = S0 * u * u
    Sud = S0 * u * d
    Sdd = S0 * d * d

    K = 100
    Cuu = max(Suu - K, 0)
    Cud = max(Sud - K, 0)
    Cdd = max(Sdd - K, 0)

    # Discount
    # Node U
    Cu = np.exp(-r) * (p_rn * Cuu + (1-p_rn) * Cud)
    # Node D
    Cd = np.exp(-r) * (p_rn * Cud + (1-p_rn) * Cdd)
    # Node 0
    C0 = np.exp(-r) * (p_rn * Cu + (1-p_rn) * Cd)

    # 4(c) Special Dividend
    # Paid in period 2 (end of year 2).
    # If S_2 >= 100, Pay 10.
    # Option Maturity T=3.
    # Tree needs to go to T=3.
    # At t=2:
    # Calculate Pre-Div Price. Check condition. Subtract Div.
    # Then evolve to t=3.

    # Rebuild Tree nodes
    # t=2 nodes: UU, UD, DD.
    # Prices pre-div: Suu=144, Sud=100, Sdd=69.44.
    # Check Div:
    # Suu=144 >= 100. Pay 10. Post=134.
    # Sud=100 >= 100. Pay 10. Post=90.
    # Sdd=69.44 < 100. Pay 0. Post=69.44.

    # t=3 nodes:
    # From UU (Post 134): UUU (134*1.2), UUD (134*d).
    # From UD (Post 90): UDU (90*1.2), UDD (90*d).
    # From DD (Post 69.44): DDU, DDD.

    # American Option check at t=2, t=1, t=0.
    # Payoff max(S - K, 0).
    # Note: Holder of option does NOT receive dividend.
    # Stock drops. Call option holder hurt.
    # Early exercise at t=2 (Pre-Div)?
    # American Call on Dividend paying stock: Exercise right before ex-div if Cum-Div Intrinsic > Ex-Div Value.

    # t=3 Values (European)
    # V_3 = max(S_3 - K, 0)
    # Back to t=2.
    # Value_Continuation = exp(-r) * E[V_3].
    # Exercise Value at t=2 (Pre-Div): S_2_pre - K.
    # Compare.

    # Node UU (t=2): S_pre=144. Div=10. S_post=134.
    # Ex Value = 144 - 100 = 44.
    # Cont Value:
    # S_3_u = 134 * 1.2 = 160.8. V=60.8.
    # S_3_d = 134 / 1.2 = 111.66. V=11.66.
    # V_cont = exp(-0.02) * (p * 60.8 + (1-p) * 11.66).

    # Let's calculate numbers.
    p = p_rn
    df = np.exp(-r)

    # Node UU
    S_post_UU = 134.0
    V_cont_UU = df * (p * max(S_post_UU*u-K,0) + (1-p) * max(S_post_UU*d-K,0))
    V_ex_UU = 144.0 - K
    V_UU = max(V_cont_UU, V_ex_UU)

    # Node UD
    S_post_UD = 90.0
    V_cont_UD = df * (p * max(S_post_UD*u-K,0) + (1-p) * max(S_post_UD*d-K,0))
    V_ex_UD = 100.0 - K
    V_UD = max(V_cont_UD, V_ex_UD)

    # Node DD
    S_post_DD = Sdd
    V_cont_DD = df * (p * max(S_post_DD*u-K,0) + (1-p) * max(S_post_DD*d-K,0))
    V_ex_DD = Sdd - K # Negative, 0
    V_DD = max(V_cont_DD, 0)

    # t=1
    # Node U
    Su = S0 * u
    V_cont_U = df * (p * V_UU + (1-p) * V_UD)
    V_ex_U = Su - K
    V_U = max(V_cont_U, V_ex_U)

    # Node D
    Sd = S0 * d
    V_cont_D = df * (p * V_UD + (1-p) * V_DD)
    V_ex_D = Sd - K
    V_D = max(V_cont_D, 0) # Sd < K

    # t=0
    V_0_Am = df * (p * V_U + (1-p) * V_D) # S0=100 not exercised (ATM)

    mo.md(
        f"""
        **Option Results:**
        *   (a) European Call (2yr): {C0:.4f}
        *   (c) American Call (3yr, Special Div): {V_0_Am:.4f}
        *   Exercise Check Node UU (t=2): Cont={V_cont_UU:.2f}, Ex={V_ex_UU:.2f}. Exercise? {V_ex_UU > V_cont_UU}.
        """
    )
    return (
        C0,
        Cd,
        Cdd,
        Cud,
        Cu,
        Cuu,
        K,
        S0,
        S_post_DD,
        S_post_UD,
        S_post_UU,
        Sd,
        Sdd,
        Su,
        Sud,
        Suu,
        T,
        V_0_Am,
        V_D,
        V_DD,
        V_U,
        V_UD,
        V_UU,
        V_cont_D,
        V_cont_DD,
        V_cont_U,
        V_cont_UD,
        V_cont_UU,
        V_ex_D,
        V_ex_DD,
        V_ex_U,
        V_ex_UD,
        V_ex_UU,
        d,
        df,
        p,
        p_rn,
        r,
        u,
    )

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. Structured Product
        """
    )
    return

@app.cell
def _(go, mo, np):
    # Payoff
    # Index < 0 Return (S < 1000): 1000
    # 0 < Ret < 20% (1000 < S < 1200): 1000 + 1000 * 2 * Ret
    # Ret > 20% (S > 1200): 1400

    # Ret = (S - 1000) / 1000
    # Middle: 1000 + 2000 * (S - 1000)/1000 = 1000 + 2(S - 1000) = 2S - 1000.
    # At S=1000: 1000.
    # At S=1200: 2(1200) - 1000 = 1400. Matches cap.

    # Decomposition
    # 1. Bond (1000). Pays 1000 always.
    # 2. Plus Call Spread?
    #    If S > 1000: Payoff S - 1000?
    #    We need 2(S - 1000).
    #    So 2 * Call(1000).
    #    If S > 1200: 2 * Call(1000) pays 2(S - 1000).
    #    We want Cap 1400. Cap Gain = 400.
    #    2(S - 1000) - X = 400.
    #    At S=1200, 2(200) = 400.
    #    Above 1200, we want flat 400.
    #    So subtract 2 * Call(1200).
    #    Payoff: 2 * (S - 1200).
    #    Net: 2(S - 1000) - 2(S - 1200) = 2S - 2000 - 2S + 2400 = 400.
    # Decomposition: Bond(1000) + 2 * Call(1000) - 2 * Call(1200).

    # (b) Valuation using Puts
    # Given Put(1000) = 50, Put(1200) = 188.
    # Use Put-Call Parity to find Calls.
    # C - P = S - K * exp(-rT).
    # S = 1000. r = 0.02. T = 1.
    # Call(1000) = P(1000) + 1000 - 1000*exp(-0.02).
    # Call(1200) = P(1200) + 1000 - 1200*exp(-0.02).

    S_idx = 1000
    r = 0.02
    T = 1

    P_1000 = 50
    P_1200 = 188

    df = np.exp(-r*T)

    C_1000 = P_1000 + S_idx - 1000 * df
    C_1200 = P_1200 + S_idx - 1200 * df

    # Val = 1000 * df + 2 * C_1000 - 2 * C_1200
    Bond_Val = 1000 * df
    Struct_Val = Bond_Val + 2 * C_1000 - 2 * C_1200

    # Payoff Diagram
    S_grid = np.linspace(800, 1400, 100)
    Payoff = np.where(S_grid < 1000, 1000,
                      np.where(S_grid <= 1200, 2*S_grid - 1000, 1400))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_grid, y=Payoff, name='Payoff'))
    fig.update_layout(title='Structured Product Payoff', xaxis_title='Index', yaxis_title='Value')

    mo.md(
        f"""
        **Structured Product:**
        *   Decomposition: Bond + 2 Calls(1000) - 2 Calls(1200).
        *   Calculated Call(1000): {C_1000:.2f}
        *   Calculated Call(1200): {C_1200:.2f}
        *   Fair Value: {Struct_Val:.2f}
        """
    )
    return (
        Bond_Val,
        C_1000,
        C_1200,
        P_1000,
        P_1200,
        Payoff,
        S_grid,
        S_idx,
        Struct_Val,
        T,
        df,
        fig,
        r,
    )

@app.cell
def _(fig, mo):
    mo.ui.plotly(fig)
    return

if __name__ == "__main__":
    app.run()
