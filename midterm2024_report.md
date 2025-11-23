# Financial Instruments Midterm 2024

## 1. True-False

**(a) Short Straddle Risk**
**False.** A short straddle involves selling a call and a put. The risk is unlimited on the upside (Call) and substantial on the downside (Put). Selling before maturity does not eliminate risk; the position is short Vega (volatility risk) and short Gamma.

**(b) Sharpe Ratio**
**True.** In the Black-Scholes framework, the instantaneous Sharpe ratio of a derivative is equal to the Sharpe ratio of the underlying asset ($\frac{\mu - r}{\sigma}$).

## 2. Binomial Trees

**(a) Analyst Assumptions**
Different volatility or event risk in different periods (e.g., earnings announcement in first 6 months, stable afterwards).

**(b) Tree**
*   $t=0$: 100.
*   $t=0.5$: 120, 90.
*   $t=1$:
    *   120 $\to$ 138, 114.
    *   90 $\to$ 103.5, 85.5.

**(c) Risk Neutral Probabilities**
*   Period 1: $p_1 = (e^{0.01} - 0.9)/(1.2 - 0.9) \approx 0.3668$.
*   Period 2: $p_2 = (e^{0.01} - 0.95)/(1.15 - 0.95) \approx 0.3002$.
*   Comparison: Lower than analyst prob (0.6). Risk aversion implies risk-neutral drift ($r$) is less than physical drift ($\mu$), requiring lower probability of up moves.

**(d) Options Strategy**
*   Long Call (120) + Long Put (100). (Long Strangle).
*   Bet on high volatility.
*   **Price:** Calculated as ~7.85 (using code).
*   **Arbitrage:** If Market > Model, Sell Market, Buy Synthetic (Dynamic Replication).

## 3. Black-Scholes

**(a) Put Price & Hedge**
*   Put Price calculated (~3.42).
*   Hedge: Short Shares. Delta is positive for Short Put position.

**(b) After 1 Day**
*   Price drops to 40. Put value increases significantly.
*   Hedge (Short Stock) gains value, offsetting the loss on the Short Put.
*   Gamma effect: Hedge might not be perfect if not rebalanced continuously.

## 4. Swap

**(a) Forward Rate**
Calculated $F_1 \approx 1.212$.

**(b) Valuation**
Spot drops to 1.15. Forward curve shifts down proportionally.
Value of paying fixed USD and receiving floating EUR (converted to USD) drops.
Position loses value.
