import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from scipy.stats import norm
    import pandas as pd
    return go, mo, norm, np, pd

@app.cell
def _(mo):
    mo.md(
        r"""
        # Financial Instruments - Homework 5 Solution
        """
    )
    return

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. Multiperiod Binomial Tree
        """
    )
    return

@app.cell
def _(np):
    # 1.1 Replicating Portfolio
    S0 = 100.0
    u = 1.1
    d = 1/u
    r = 0.05
    K = 100.0
    p = (1 + r - d) / (u - d)

    # Prices at t=2
    Suu = S0 * u**2
    Sud = S0 * u * d
    Sdd = S0 * d**2

    # Payoffs
    Cuu = max(Suu - K, 0)
    Cud = max(Sud - K, 0)
    Cdd = max(Sdd - K, 0)

    # t=1
    Vu = (p * Cuu + (1 - p) * Cud) / (1 + r)
    Vd = (p * Cud + (1 - p) * Cdd) / (1 + r)

    # t=0
    V0 = (p * Vu + (1 - p) * Vd) / (1 + r)

    # Hedge
    Su = S0 * u
    Sd = S0 * d
    Delta_0 = (Vu - Vd) / (Su - Sd)
    B_0 = (Vu - Delta_0 * Su) / (1 + r)

    return (
        B_0,
        Cdd,
        Cud,
        Cuu,
        Delta_0,
        K,
        S0,
        Sd,
        Sdd,
        Su,
        Sud,
        Suu,
        V0,
        Vd,
        Vu,
        d,
        p,
        r,
        u,
    )

@app.cell
def _(B_0, Delta_0, V0, mo):
    mo.md(
        f"""
        **Binomial Tree Results:**
        *   Option Price $V_0$: {V0:.4f}
        *   Delta $\Delta_0$: {Delta_0:.4f}
        *   Bond $B_0$: {B_0:.4f}
        """
    )
    return

@app.cell
def _(go, mo, norm, np):
    # 2. Black-Scholes Convexity
    S = np.linspace(20, 70, 100)
    K = 40
    T = 0.5
    r = 0.1
    sigma = 0.2

    def bs_price(S, K, T, r, sigma, type='call'):
        d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if type == 'call':
            return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
        else:
            return K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    C = bs_price(S, K, T, r, sigma, 'call')
    P = bs_price(S, K, T, r, sigma, 'put')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=C, name='Call Price'))
    fig.add_trace(go.Scatter(x=S, y=P, name='Put Price'))
    fig.update_layout(title='Option Price Convexity', xaxis_title='Stock Price', yaxis_title='Option Price')
    return C, K, P, S, T, bs_price, fig, r, sigma

@app.cell
def _(fig, mo):
    return mo.ui.plotly(fig)

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. Convergence
        """
    )
    return

@app.cell
def _(K, S0, T, bs_price, np, pd, r, sigma):
    # Convergence Table
    steps = [2, 5, 10, 25, 50, 125, 250]
    results = []

    # BS Price
    bs_val = bs_price(S0, K, T, r, sigma, 'call') # Note: S0=100 from prev block used here? Or 42?
    # Actually Assignment 5 Q2 uses S=42. Q1 uses S=100.
    # Let's use Q2 params for convergence if implied.
    # Q3 says "Use BinomialTree.xls...". Usually Q2 and Q3 are linked in context or standard convergence.
    # Let's use Q2 params (S=42, K=40, T=0.5).
    S_conv = 42.0
    K_conv = 40.0
    T_conv = 0.5

    bs_val = bs_price(S_conv, K_conv, T_conv, r, sigma, 'call')

    for N in steps:
        dt = T_conv / N
        u_b = np.exp(sigma * np.sqrt(dt))
        d_b = 1 / u_b
        p_b = (np.exp(r * dt) - d_b) / (u_b - d_b)

        j = np.arange(0, N + 1)
        ST = S_conv * (u_b ** j) * (d_b ** (N - j))
        C = np.maximum(ST - K_conv, 0)

        for i in range(N - 1, -1, -1):
            C = np.exp(-r * dt) * (p_b * C[1:] + (1 - p_b) * C[:-1])

        results.append({'N': N, 'Tree Price': C[0], 'Error': C[0] - bs_val})

    df_conv = pd.DataFrame(results)
    return (
        C,
        K_conv,
        N,
        ST,
        S_conv,
        T_conv,
        bs_val,
        d_b,
        df_conv,
        dt,
        i,
        j,
        p_b,
        results,
        steps,
        u_b,
    )

@app.cell
def _(df_conv, mo):
    mo.ui.table(df_conv)
    return

if __name__ == "__main__":
    app.run()
