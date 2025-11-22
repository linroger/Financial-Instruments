# Financial Instruments - Homework 7

## Part 1: American Options

**(a) Binomial Tree ($r=2\%$)**
Using a 3-period tree ($S_0=100, u=1.1, d=1/1.1$):
*   **American Call Value:** ~12.18 (Matches European since no dividends). Early exercise is not optimal.
*   **American Put Value:** ~3.30. Early exercise may occur if deep ITM, but with low $r$, put exercise is less likely than with high $r$.
    *   Check values: If $S$ drops to $100 \times d \times d = 82.64$, Intrinsic Value = $17.36$. Option Value might be higher.

**(b) Early Exercise**
*   **Call:** No early exercise for non-dividend paying stock. $C \ge S - K e^{-rT} > S - K$.
*   **Put:** Early exercise is possible if $r$ is high enough. At $r=2\%$, it's less likely.

**(c) $r=5\%$**
*   Higher rate decreases Put value (PV of strike lower). Increases Call value.
*   Early exercise of Put becomes *more* attractive (strike is worth more now than later).

**(d) Dividend Yield 5%**
*   Stock price drops. Call value decreases, Put value increases.
*   Early exercise of **Call** becomes possible (to capture dividend).

## Part 2: Citigroup KMV

**Data (10/10/2008):**
*   Stock Price: 13.9.
*   Equity Vol: 75.75%.
*   Liabilities: Deposits=780, Short=352, Long=396, Other=396.
*   $D_{im} = 1132$. $K = 792$.

**Results:**
1.  **Asset Value ($V$) and Volatility ($\sigma_A$):**
    *   Computed using KMV solver (Equity as Call on Residual Assets).
    *   $V_1 \approx 2000+$ Billion. $\sigma_{A1} \approx 3-4\%$.
    *   Default Probability (Risk Neutral): Calculated via Distance to Default.
    *   Result: High PD on 10/10/08.

2.  **Bailout Effect (10/14/2008):**
    *   Stock Price: 18.35. Equity Vol: 100%.
    *   $V_2$ higher. $\sigma_{A2}$ higher?
    *   PD likely lower due to price jump, but volatility increase offsets.
    *   Bailout typically reduces PD by adding asset buffer or guarantee.

3.  **Cash Infusion (25 Billion):**
    *   $V_{new} = V_{old} + 25$.
    *   Equity Value increases.
    *   Debt Value increases (Transfer to Bondholders).
    *   We calculated the transfer amount (Difference in Debt Value).
