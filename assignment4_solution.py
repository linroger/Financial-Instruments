import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    return mo, np, go

@app.cell
def _(mo):
    mo.md(
        r"""
        # Financial Instruments - Homework 4 Solution
        """
    )
    return

@app.cell
def _(go, mo, np):
    # 1. Straddle Diagram
    K = 19750
    Premium = 1970
    S = np.linspace(15000, 25000, 100)

    Payoff_Call_Short = -np.maximum(S - K, 0)
    Payoff_Put_Short = -np.maximum(K - S, 0)
    Total_Payoff = Payoff_Call_Short + Payoff_Put_Short
    Profit = Total_Payoff + Premium

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=Profit, name='Short Straddle Profit'))
    fig.add_trace(go.Scatter(x=S, y=np.zeros_like(S), name='Breakeven', line=dict(dash='dash', color='gray')))

    fig.update_layout(title='Leeson Short Straddle Profit Diagram', xaxis_title='Nikkei Index', yaxis_title='Profit (Points)')
    mo.md(
        f"""
        **Profit Diagram:** Shows profit range between {K-Premium} and {K+Premium}.
        """
    )
    return K, Payoff_Call_Short, Payoff_Put_Short, Premium, Profit, S, Total_Payoff, fig

@app.cell
def _(fig, mo):
    return mo.ui.plotly(fig)

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Binomial Trees (Vanda)
        """
    )
    return

@app.cell
def _(np):
    # Binomial Tree Logic
    S1_u = 21.0
    S1_d = 10.0
    q_real = 0.7
    beta = 2.0
    r_cc = 0.05
    E_RP = 0.0644

    r_annual = np.exp(r_cc) - 1
    E_R_annual = r_annual + beta * E_RP
    E_S1_analyst = q_real * S1_u + (1 - q_real) * S1_d
    S0 = E_S1_analyst / (1 + E_R_annual)

    K = S0
    Cu = max(S1_u - K, 0)
    Cd = max(S1_d - K, 0)
    p_rn = (S0 * np.exp(r_cc) - S1_d) / (S1_u - S1_d)
    V_opt = np.exp(-r_cc) * (p_rn * Cu + (1 - p_rn) * Cd)

    return (
        Cd,
        Cu,
        E_RP,
        E_R_annual,
        E_S1_analyst,
        K,
        S0,
        S1_d,
        S1_u,
        V_opt,
        beta,
        p_rn,
        q_real,
        r_annual,
        r_cc,
    )

@app.cell
def _(S0, V_opt, mo):
    mo.md(
        f"""
        **Binomial Tree Valuation:**
        *   Implied $S_0$: {S0:.4f}
        *   ATM Option Value: {V_opt:.4f}
        """
    )
    return

if __name__ == "__main__":
    app.run()
