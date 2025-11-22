import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    return go, mo, np

@app.cell
def _(go, mo, np):
    # PLUS Payoff
    S0 = 100
    S = np.linspace(50, 150, 100)

    # Components
    # 1. Stock component (Downside only? No, PLUS pays 10 * S/S0 if S < S0)
    Payoff_Down = np.where(S <= S0, 10 * S/S0, 0)

    # 2. Upside
    # 10 + 30 * (S-S0)/S0, Capped at 11.90
    Payoff_Up = np.where(S > S0, np.minimum(10 + 30 * (S - S0)/S0, 11.90), 0)

    Payoff_Total = Payoff_Down + Payoff_Up

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=Payoff_Total, name='PLUS Payoff'))
    fig.add_trace(go.Scatter(x=S, y=np.full_like(S, 10), name='Principal', line=dict(dash='dash')))

    fig.update_layout(title='Morgan Stanley PLUS Payoff Diagram', xaxis_title='Index Level', yaxis_title='Redemption Amount')
    return Payoff_Down, Payoff_Total, Payoff_Up, S, S0, fig

@app.cell
def _(fig, mo):
    return mo.ui.plotly(fig)

if __name__ == "__main__":
    app.run()
