import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from scipy.stats import norm
    return go, mo, norm, np

@app.cell
def _(go, mo, norm, np):
    # BS Convexity
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

if __name__ == "__main__":
    app.run()
