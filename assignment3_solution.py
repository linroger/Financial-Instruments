import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    return mo, np, pd, go

@app.cell
def _(mo):
    mo.md(
        r"""
        # Financial Instruments - Homework 3 Solution
        """
    )
    return

@app.cell
def _(np, pd):
    # Part 1 Code from previous step (summarized)
    df_zcb = pd.read_excel("Assignments/Assignment 3/Greece_GS_table1.xls", header=None).iloc[2:]
    df_zcb.columns = ['NaN', 'Maturity', 'ZEU', 'ZUS']
    S0 = 0.8475
    pv_usd_leg = 0
    for idx, row in df_zcb.iterrows():
        t = row['Maturity']
        if t == 0: continue
        cf = 1.5 + (50 if t==10 else 0)
        pv_usd_leg += cf * row['ZUS']
    sum_zeu = df_zcb[df_zcb['Maturity']>0]['ZEU'].sum()
    zeu_T = df_zcb.iloc[-1]['ZEU']
    c_eur_fair = (pv_usd_leg / S0 - 59.0 * zeu_T) / (29.5 * sum_zeu)
    return S0, c_eur_fair, df_zcb, idx, pv_usd_leg, sum_zeu, zeu_T

@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. Hedging Payoff Diagrams
        """
    )
    return

@app.cell
def _(go, np):
    # Payoff Diagrams
    S = np.linspace(60, 140, 100)
    K = 105
    Premium_Call = 2.541

    # Straight Insurance (Long Call)
    Payoff_Call = np.maximum(S - K, 0) - Premium_Call

    # Implicit Short Fuel Position (Costs rise as S rises)
    # Relative to K=95 (Spot at t=0)?
    # "Payoff ... of the implicit short position"
    # Usually "Short Stock" payoff relative to initial price S0=95.
    # Payoff = S0 - S.
    S0_oil = 95
    Payoff_Short = S0_oil - S

    # Combined
    Payoff_Hedged = Payoff_Short + np.maximum(S - K, 0) - Premium_Call

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=Payoff_Short, name='Implicit Short (Fuel Need)'))
    fig.add_trace(go.Scatter(x=S, y=np.maximum(S - K, 0) - Premium_Call, name='Long Call (Insurance)'))
    fig.add_trace(go.Scatter(x=S, y=Payoff_Hedged, name='Hedged Position', line=dict(width=4)))

    fig.update_layout(title='Southwest Hedging Payoff (Straight Insurance)', xaxis_title='Oil Price at Maturity', yaxis_title='Payoff')
    return (
        K,
        Payoff_Call,
        Payoff_Hedged,
        Payoff_Short,
        Premium_Call,
        S,
        S0_oil,
        fig,
    )

@app.cell
def _(fig, mo):
    return mo.ui.plotly(fig)

if __name__ == "__main__":
    app.run()
