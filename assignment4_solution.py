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

if __name__ == "__main__":
    app.run()
