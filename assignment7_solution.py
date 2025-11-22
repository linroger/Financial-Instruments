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
    # Default Prob vs Asset Value
    V = np.linspace(1500, 2500, 100)
    K = 1132 # D_im + K_opt approx from solution
    Sig_A = 0.035
    T = 1
    r = 0.02

    def calc_pd(V, K, Sig_A, T, r):
        d2 = (np.log(V/K) + (r - 0.5 * Sig_A**2) * T) / (Sig_A * np.sqrt(T))
        return norm.cdf(-d2)

    PD = calc_pd(V, K, Sig_A, T, r)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=V, y=PD, name='Default Probability'))
    fig.update_layout(title='Default Probability vs Asset Value', xaxis_title='Asset Value (V)', yaxis_title='PD')
    return K, PD, Sig_A, T, V, calc_pd, fig, r

@app.cell
def _(fig, mo):
    return mo.ui.plotly(fig)

if __name__ == "__main__":
    app.run()
