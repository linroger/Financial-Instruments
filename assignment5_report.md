# Financial Instruments - Homework 5

## 1. Multiperiod Binomial Tree

**1.1 Replicating Portfolio ($S_0 = 100$)**
We used a two-period binomial tree with $u=1.1, d=1/1.1, r=5\%$.
*   **Option Value:** $V_0 \approx 10.38$.
*   **Delta:** $\Delta_0 \approx 0.773$.
*   **Borrowing:** $B_0 \approx -66.92$.

**1.1 (b) Convexity**
The relationship between the Replicating Portfolio Value and $S_0$ is **Convex**.
As $S_0$ increases, Delta increases (Gamma is positive).

**1.1 (c) Self-Financing**
The cost of establishing the new portfolio at $t=1$ matches the value of the old portfolio carried forward. No external cash injection needed.

**1.1 (d) Profit/Loss**
Since the portfolio replicates the option exactly, the net P&L is zero (assuming fair pricing).

**1.1 (e) Dividend Yield (5%)**
Dividends reduce the stock price at each node. The tree structure changes ($S_u = S_0 u (1-y)$).
Option value decreases because Call options are less valuable when dividends are paid (stock price drops).

**1.1 (f) Fixed Dividend ($5)**
Fixed dividend subtraction can make the tree non-recombining ($S_{ud} \neq S_{du}$ if subtracted after move? Or $u$ applies to ex-div price? Standard binomial usually handles yield better).
Option value decreases.

## 2. Black-Scholes (Verotende)

**2.1 Prices**
Using BS Formula ($S=42, K=40, T=0.5, \sigma=0.2, r=0.1$):
*   **Call Price:** ~4.76
*   **Put Price:** ~0.81

**2.2 Convexity**
Both Call and Put prices are convex with respect to Stock Price ($S$).

**2.3 Sensitivity Table**
*   **Stock Price (Up):** Call Up, Put Down.
*   **Strike Price (Up):** Call Down, Put Up.
*   **Volatility (Up):** Call Up, Put Up (Vega positive for both).
*   **Maturity (Up):** Call Up, Put Up (usually).
*   **Risk-free Rate (Up):** Call Up, Put Down (Rho).

**2.4 Hedging Short Put**
*   A Short Put position has a positive Delta ($1 - N(d_1)$).
*   To hedge this position (make the portfolio Delta-neutral), one must offset the positive Delta with a negative Delta.
*   **Action:** Sell (Short) Shares.

## 3. Big Binomial Tree

As $N$ increases, the Binomial Tree price converges to the Black-Scholes price.
For $N=250$, the error is negligible.
