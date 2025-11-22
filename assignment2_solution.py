
import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    from datetime import datetime
    return datetime, go, mo, np, pd

@app.cell
def _(mo):
    mo.md(
        r"""
        # Financial Instruments - Assignment 2 Solution
        """
    )
    return

@app.cell
def _(np, pd):
    # Load Data Correctly with Headers
    file_path = "Assignments/Assignment 2/DataHW2_2024.xls"

    # Sheet: ForwardArbitrage
    df_arb = pd.read_excel(file_path, sheet_name='ForwardArbitrage', header=3)
    df_arb.columns = [c.strip() if isinstance(c, str) else c for c in df_arb.columns]

    # Sheet: Oil
    df_oil_raw = pd.read_excel(file_path, sheet_name=0, header=None)
    # Q3.2 (Rows 4-60 approx)
    q3_1 = df_oil_raw.iloc[4:60, [0, 1, 2, 3, 6]].copy()
    q3_1.columns = ['Date', 'FEB.08', 'MAR.08', 'APR.08', 'FuelPrice']
    q3_1['Date'] = pd.to_datetime(q3_1['Date'], errors='coerce')
    q3_1 = q3_1.dropna(subset=['Date'])

    return df_arb, df_oil_raw, file_path, q3_1

@app.cell
def _(df_arb, mo, np):
    # 1. Arbitrage
    d0 = df_arb.iloc[0]
    d1 = df_arb.iloc[1]

    # Parameters
    T = 1.0
    S0 = d0['$/EURO SPOT']
    F0 = d0['$/EURO FORWARD']
    rUS_0 = d0['US LIBOR'] / 100.0
    rEU_0 = d0['EURO LIBOR'] / 100.0

    rUS_0_cc = np.log(1 + rUS_0 * T) / T
    rEU_0_cc = np.log(1 + rEU_0 * T) / T

    t = 0.5
    rem_T = 0.5

    St = d1['$/EURO SPOT']
    Ft = d1['$/EURO FORWARD']
    rUS_t = d1['US LIBOR'] / 100.0
    rEU_t = d1['EURO LIBOR'] / 100.0

    rUS_t_cc = np.log(1 + rUS_t * rem_T) / rem_T
    rEU_t_cc = np.log(1 + rEU_t * rem_T) / rem_T

    # Valuations
    val_short_fwd = (F0 - Ft) * np.exp(-rUS_t_cc * rem_T)
    val_asset = St * np.exp(-rEU_t_cc * rem_T)
    D0 = S0 * np.exp(-rEU_0_cc * T)
    N = D0 * np.exp(rUS_0_cc * T)
    val_liab = N * np.exp(-rUS_t_cc * rem_T)

    val_synth = val_asset - val_liab
    total = val_short_fwd + val_synth

    mo.md(
        f"""
        **Arbitrage Results:**
        *   Start Date: {d0['Date']}
        *   Total P&L: {total:.5f}
        """
    )
    return (
        D0,
        F0,
        Ft,
        N,
        S0,
        St,
        T,
        d0,
        d1,
        rEU_0,
        rEU_0_cc,
        rEU_t,
        rEU_t_cc,
        rUS_0,
        rUS_0_cc,
        rUS_t,
        rUS_t_cc,
        rem_T,
        t,
        total,
        val_asset,
        val_liab,
        val_short_fwd,
        val_synth,
    )

@app.cell
def _(go, pd, q3_1):
    # 3. Southwest Hedging Visualization

    # Calculate P&L per contract per month
    n_contracts = 2249
    contract_size = 1000

    months = ['FEB.08', 'MAR.08', 'APR.08']
    start_prices = [95.98, 95.78, 95.24]

    gains = []
    final_prices = []
    dates = []

    for col, p0 in zip(months, start_prices):
        series = q3_1[['Date', col]].dropna()
        pT = series.iloc[-1][col]
        dt = series.iloc[-1]['Date']
        gain = (pT - p0) * contract_size * n_contracts
        gains.append(gain)
        final_prices.append(pT)
        dates.append(dt)

    # Visualization
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=gains,
        name='Hedging Gain ($)'
    ))
    fig.update_layout(title='Southwest Hedging Gains by Contract', yaxis_title='Gain ($)')
    return contract_size, dates, dt, fig, final_prices, gain, gains, months, n_contracts, p0, pT, series, start_prices

@app.cell
def _(fig, mo):
    return mo.ui.plotly(fig)


if __name__ == "__main__":
    app.run()
