import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    from scipy.stats import norm
    from scipy.optimize import fsolve
    import plotly.graph_objects as go
    return fsolve, go, mo, norm, np, pd

@app.cell
def _(mo):
    mo.md(
        r"""
        # Financial Instruments - Homework 7 Solution
        """
    )
    return

@app.cell
def _(mo):
    mo.md(
        r"""
        ## Part 1: American Options (Binomial)
        """
    )
    return

@app.cell
def _(np):
    # Binomial Tree Logic
    S0 = 100.0
    K = 100.0
    u = 1.1
    d = 1.0/u
    T = 3
    r_cc = 0.02
    p_rn = (np.exp(r_cc) - d) / (u - d)

    def build_tree(S, u, d, N):
        tree = []
        for i in range(N + 1):
            level = [S * (u**j) * (d**(i-j)) for j in range(i + 1)]
            tree.append(level)
        return tree

    price_tree = build_tree(S0, u, d, T)

    def value_option(tree, K, r, p, type='call'):
        N = len(tree) - 1
        vals = []
        if type == 'call':
            vals = [max(s - K, 0) for s in tree[-1]]
        else:
            vals = [max(K - s, 0) for s in tree[-1]]

        for i in range(N - 1, -1, -1):
            new_vals = []
            for j in range(i + 1):
                cont = np.exp(-r) * (p * vals[j+1] + (1-p) * vals[j])
                s = tree[i][j]
                ex = max(s - K, 0) if type == 'call' else max(K - s, 0)
                new_vals.append(max(cont, ex))
            vals = new_vals
        return vals[0]

    val_call = value_option(price_tree, K, r_cc, p_rn, 'call')
    val_put = value_option(price_tree, K, r_cc, p_rn, 'put')

    return (
        K,
        S0,
        T,
        build_tree,
        d,
        p_rn,
        price_tree,
        r_cc,
        u,
        val_call,
        val_put,
        value_option,
    )

@app.cell
def _(val_call, val_put, mo):
    mo.md(
        f"""
        **Binomial Results:**
        *   American Call: {val_call:.4f}
        *   American Put: {val_put:.4f}
        """
    )
    return

@app.cell
def _(mo):
    mo.md(
        r"""
        ## Part 2: KMV Model
        """
    )
    return

@app.cell
def _(fsolve, norm, np):
    # KMV Logic
    Deposits = 780.343
    ShortTerm = 352.274
    LongTerm = 396.097
    Other = 395.693
    D_im = Deposits + ShortTerm
    L_opt = LongTerm + Other
    K_opt = L_opt

    # 10/10/2008
    P1 = 13.9
    Shares = 19.02 / 3.49
    E1 = P1 * Shares
    Sig_E1 = 0.75753
    r = 0.02
    T = 1.0

    def kmv_sys(x, E_obs, Sig_E_obs, D_im, K, T, r):
        V, Sig_A = x
        V_adj = V - D_im
        if V_adj <= 0: return [1e5, 1e5]
        d1 = (np.log(V_adj/K) + (r + 0.5*Sig_A**2)*T) / (Sig_A*np.sqrt(T))
        d2 = d1 - Sig_A*np.sqrt(T)
        E_mod = V_adj * norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
        Sig_E_mod = norm.cdf(d1) * (V / E_obs) * Sig_A
        return [E_mod - E_obs, Sig_E_mod - Sig_E_obs]

    root = fsolve(kmv_sys, [E1 + D_im + K_opt, Sig_E1 * E1/(E1+D_im+K_opt)], args=(E1, Sig_E1, D_im, K_opt, T, r))
    V1, Sig_A1 = root

    def calc_pd(V, K, Sig_A, T, r, D_im):
        V_adj = V - D_im
        d2 = (np.log(V_adj/K) + (r - 0.5*Sig_A**2)*T) / (Sig_A*np.sqrt(T))
        return norm.cdf(-d2)

    pd_val = calc_pd(V1, K_opt, Sig_A1, T, r, D_im)

    return (
        D_im,
        Deposits,
        E1,
        K_opt,
        L_opt,
        LongTerm,
        Other,
        P1,
        Shares,
        ShortTerm,
        Sig_A1,
        Sig_E1,
        T,
        V1,
        calc_pd,
        kmv_sys,
        pd_val,
        r,
        root,
    )

@app.cell
def _(V1, mo, pd_val):
    mo.md(
        f"""
        **KMV Results (10/10/2008):**
        *   Asset Value $V$: {V1:.2f}
        *   Default Probability: {pd_val:.4%}
        """
    )
    return

@app.cell
def _(D_im, K_opt, Sig_A1, T, calc_pd, go, mo, np, r):
    # Visualization
    V_range = np.linspace(1500, 2500, 100)
    PD_range = [calc_pd(v, K_opt, Sig_A1, T, r, D_im) for v in V_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=V_range, y=PD_range, name='Default Probability'))
    fig.update_layout(title='Default Probability Sensitivity to Asset Value', xaxis_title='Asset Value (V)', yaxis_title='PD')
    return PD_range, V_range, fig

@app.cell
def _(fig, mo):
    return mo.ui.plotly(fig)

if __name__ == "__main__":
    app.run()
