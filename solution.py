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
        # Financial Instruments - Homework 1

        ## Task 1: Arbitrage and Forward Rates

        Consider a one-year forward contract for converting between dollars and Euros.
        The current exchange rate is $S_0 = 1.20$ for each Euro.
        The one-year risk-free rate in dollars is $r_{USD} = 5\%$ in continuously compounded units.
        The one-year risk-free rate in Euros is $r_{EUR} = 4.5\%$ in continuously compounded units.

        **(1) According to the principle of no-arbitrage, what should be the one-year forward rate?**
        """
    )
    return


@app.cell
def _():
    # Parameters
    S0 = 1.20
    r_usd_cc = 0.05
    r_eur_cc = 0.045
    T = 1.0

    # Formula: F = S * exp((r_usd - r_eur) * T)
    F_theoretical = S0 * np.exp((r_usd_cc - r_eur_cc) * T)
    return F_theoretical, S0, T, r_eur_cc, r_usd_cc


@app.cell
def _(F_theoretical, mo):
    mo.md(
        f"""
        The theoretical forward rate is calculated as:
        $$
        F = S_0 e^{{(r_{{USD}} - r_{{EUR}})T}} = 1.20 e^{{(0.05 - 0.045) \\times 1}} = 1.20 e^{{0.005}} \\approx {F_theoretical:.6f}
        $$

        So, the one-year forward rate should be **{F_theoretical:.6f}**.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        **(2) Suppose that the one-year forward contract is currently trading at $1.15 per Euro. Is there an arbitrage opportunity? If so, explain in detail the trading you would like to do to exploit this arbitrage opportunity.**
        """
    )
    return


@app.cell
def _(F_theoretical, mo):
    F_market = 1.15
    arbitrage_exists = F_market != F_theoretical

    # Since F_market (1.15) < F_theoretical (~1.206), the forward is "cheap".
    # We should BUY the forward (Long EUR forward).
    # To hedge, we SELL EUR spot (Short EUR spot).

    mo.md(
        f"""
        Yes, there is an arbitrage opportunity because $F_{{market}} = {F_market} \\neq F_{{theoretical}} \\approx {F_theoretical:.4f}$.

        Since $F_{{market}} < F_{{theoretical}}$, the Forward contract is undervalued (too cheap).
        Strategy: **Buy Low (Forward), Sell High (Synthetically)**.

        **Arbitrage Strategy (Reverse Cash and Carry):**
        1.  **Borrow EUR** at $r_{{EUR}} = 4.5\\%$. Borrow $e^{{-0.045}} \\approx 0.956$ EUR today so that we owe exactly 1 EUR at maturity (or borrow 1 EUR and owe $e^{{0.045}}$ EUR). Let's normalize to owing $e^{{0.045}}$ EUR at $T=1$.
            - Borrow 1 EUR at $t=0$.
            - Repayment at $t=1$ will be $e^{{0.045}}$ EUR.
        2.  **Convert EUR to USD** at Spot Rate $S_0 = 1.20$.
            - Receive $1.20$ USD at $t=0$.
        3.  **Invest USD** at $r_{{USD}} = 5\\%$.
            - Invest $1.20$ USD.
            - Value at $t=1$: $1.20 e^{{0.05}} \\approx 1.2615$ USD.
        4.  **Enter Long Forward Contract** to buy EUR at $F_{{market}} = 1.15$.
            - Contract to buy $e^{{0.045}}$ EUR at $t=1$.
            - Price to pay: $e^{{0.045}} \\times 1.15$ USD.

        **Cash Flow Verification at $T=1$:**
        - Proceeds from USD Investment: $1.20 e^{{0.05}} = 1.26152$ USD.
        - Cost to buy EUR via Forward to repay loan: $e^{{0.045}} \\times 1.15 = 1.04603 \\times 1.15 = 1.20293$ USD.
        - **Profit**: $1.26152 - 1.20293 = \\mathbf{{0.05859}}$ USD per 1 EUR borrowed.
        """
    )
    return F_market, arbitrage_exists


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Task 2: Forward Rates and Covered Interest Rate Parity

        **(1) For each date, use the Forward Rate formula... to compute the Forward Exchange Rate...**

        We load the data from `DataHW1.xls`.
        """
    )
    return


@app.cell
def _(np, pd):
    # Load Data
    df_raw = pd.read_excel("Assignments/Assignment 1/DataHW1.xls", header=None)

    # Extract Data
    # Row 2 (index 2) onwards is data
    data = df_raw.iloc[2:].copy()
    data.columns = [
        'Date', 'Spot',
        'Fwd_1M', 'Fwd_3M', 'Fwd_6M', 'Fwd_1Y',
        'USL_1M', 'USL_3M', 'USL_6M', 'USL_1Y',
        'EUL_1M', 'EUL_3M', 'EUL_6M', 'EUL_1Y'
    ]

    # Drop empty rows (like the source footnote)
    data = data.dropna(subset=['Date'])
    data = data[data['Date'] != 'Data Source: Bloomberg'] # Clean up if needed

    # Reset index
    data.reset_index(drop=True, inplace=True)

    # Convert types
    cols_to_numeric = data.columns[1:]
    for col in cols_to_numeric:
        data[col] = pd.to_numeric(data[col])

    # Maturities
    maturities = {
        '1M': 1/12,
        '3M': 3/12,
        '6M': 6/12,
        '1Y': 1.0
    }

    results = []

    for idx, row in data.iterrows():
        date_val = row['Date']
        spot = row['Spot']

        row_res = {'Date': date_val, 'Spot': spot}

        for m in ['1M', '3M', '6M', '1Y']:
            t = maturities[m]

            # Get LIBOR rates (divide by 100)
            r_us_L = row[f'USL_{m}'] / 100.0
            r_eu_L = row[f'EUL_{m}'] / 100.0

            # Convert to Continuously Compounded
            # r_cc = ln(1 + r_L * t) / t
            r_us_cc = np.log(1 + r_us_L * t) / t
            r_eu_cc = np.log(1 + r_eu_L * t) / t

            # Calculate Forward Rate
            # F = S * exp((r_us - r_eu) * t)
            fwd_calc = spot * np.exp((r_us_cc - r_eu_cc) * t)

            fwd_mkt = row[f'Fwd_{m}']

            row_res[f'Fwd_{m}_Calc'] = fwd_calc
            row_res[f'Fwd_{m}_Mkt'] = fwd_mkt
            row_res[f'Diff_{m}'] = fwd_calc - fwd_mkt

        results.append(row_res)

    df_results = pd.DataFrame(results)
    return cols_to_numeric, data, df_raw, df_results, idx, maturities, results, row, row_res


@app.cell
def _(df_results, mo):
    mo.ui.table(df_results)
    return


@app.cell
def _(df_results, mo):
    mo.md(
        r"""
        **(2) Do your forward exchange rates match (approximately) the quoted ones?**

        Let's visualize the difference.
        """
    )
    return


@app.cell
def _(df_results, go):
    fig = go.Figure()

    # Plot Differences for 1Y as an example
    fig.add_trace(go.Bar(
        x=df_results['Date'],
        y=df_results['Diff_1Y'],
        name='Diff (Calc - Mkt) 1Y'
    ))

    fig.update_layout(title='Difference between Calculated and Market Forward Rates (1Y)',
                      yaxis_title='Difference')
    return fig,


@app.cell
def _(df_results, mo):
    mo.md(
        r"""
        Looking at the results:
        """
    )
    return


@app.cell
def _(df_results):
    # Show the differences
    cols_diff = ['Date', 'Diff_1M', 'Diff_3M', 'Diff_6M', 'Diff_1Y']
    print(df_results[cols_diff])
    return cols_diff,


@app.cell
def _(mo):
    mo.md(
        r"""
        Most differences are small, but there is a significant deviation on **2008-10-01**.

        **(3) If not, pick one particular date in which the parity is violated, and describe the arbitrage strategy you would undertake.**

        Date: **2008-10-01**
        """
    )
    return


@app.cell
def _(df_results, mo):
    # Analyze 2008-10-01
    row_2008 = df_results[df_results['Date'] == '2008-10-01'].iloc[0]

    spot_2008 = row_2008['Spot']
    calc_1y = row_2008['Fwd_1Y_Calc']
    mkt_1y = row_2008['Fwd_1Y_Mkt']
    diff = row_2008['Diff_1Y']

    explanation = ""
    if mkt_1y > calc_1y:
        explanation = "Market Forward is HIGHER than Theoretical. Buy Theoretical (Synthetically), Sell Market."
    else:
        explanation = "Market Forward is LOWER than Theoretical. Buy Market, Sell Theoretical (Synthetically)."

    mo.md(
        f"""
        On 2008-10-01:
        - Spot: {spot_2008}
        - Calculated 1Y Forward: {calc_1y:.5f}
        - Market 1Y Forward: {mkt_1y:.5f}
        - Difference: {diff:.5f}

        The Market Forward ($1.396$) is **higher** than the Theoretical Forward ($1.383$).
        This means the Market Forward is "expensive".

        **Strategy: Sell High (Forward), Buy Low (Synthetic).**

        **Arbitrage Steps (Cash and Carry):**
        1.  **Borrow USD** at US LIBOR.
        2.  **Convert to EUR** at Spot.
        3.  **Invest EUR** at EUR LIBOR.
        4.  **Sell EUR Forward** (Short Forward) at Market Rate.

        Since $F_{{market}} > F_{{theoretical}}$, we want to Sell EUR at $F_{{market}}$.
        """
    )
    return calc_1y, diff, explanation, mkt_1y, row_2008, spot_2008


if __name__ == "__main__":
    app.run()
