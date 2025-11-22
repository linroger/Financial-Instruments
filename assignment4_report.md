# Financial Instruments - Homework 4

## 1. Barings / Leeson Position

**(1) Strategy Name**
Short Straddle (or Top Straddle). Leeson sold both Calls and Puts at the same strike.

**(2) Profitability**
Profitable if the market stays stable (low volatility). The index must remain within the range $[K - Premium, K + Premium]$.
Risks: Infinite downside (if market rallies) and significant downside (if market crashes). Short Vega (exposed to volatility increase).

**(3) Profit Diagram (Single Unit)**
*   Total Premium Received: $990 + 980 = 1970$ index points.
*   Breakeven Points:
    *   Lower: $19750 - 1970 = 17780$.
    *   Upper: $19750 + 1970 = 21720$.
*   At maturity, if $S_T = 19750$, profit is max (1970 points).

**(4) Entire Strategy**
35,500 contracts. Multiplier 10,000.
Max Profit: $1970 \times 10,000 \times 35,500 \approx 700$ billion JPY.

**(5) Effect of Volatility**
Increase in volatility decreases the value of the position (Short Vega). More chance of ending up ITM on either leg.
After the earthquake, volatility spiked, hurting the position.

**(6) Final P&L (Feb 24 1995)**
*   Index: 17,473.
*   Put is ITM. Call is OTM.
*   Payoff to holder: $19750 - 17473 = 2277$ points.
*   Premium received: 1970 points.
*   Net Loss per unit: $2277 - 1970 = 307$ points.
*   Total Loss: $307 \times 10,000 \times 35,500 \approx 109$ billion JPY.

## 2. Binomial Trees - Vanda Pharmaceutical

**(1) CAPM Expected Return**
$r_f$ (annual) $= e^{0.05} - 1 \approx 5.127\%$.
$E[R] = 5.127\% + 2.0 \times 6.44\% = 18.007\%$.

**(2) Stock Price $S_0$**
$E[S_1] = 0.7 \times 21 + 0.3 \times 10 = 14.7 + 3 = 17.7$.
$S_0 = 17.7 / (1 + 0.18007) = 15.00$.

**(3) ATM Call Value ($K=15.00$)**
*   **Parameters:** $u = 21$, $d = 10$.
*   **Payoffs:** $C_u = 6$, $C_d = 0$.
*   **Replication:**
    *   $\Delta = (C_u - C_d) / (S_u - S_d) = (6 - 0) / (21 - 10) \approx 0.5455$.
    *   $B = (C_u - \Delta S_u) e^{-r} = (6 - 0.5455 \times 21) \times e^{-0.05} \approx -5.18$.
    *   $V_0 = \Delta S_0 + B = 0.5455 \times 15 - 5.18 \approx 3.00$.
*   **Risk Neutral Methodology:**
    *   $p_{rn} = (S_0 e^r - d) / (u - d) \approx 0.5245$.
    *   $V_0 = e^{-r} (p_{rn} C_u + (1-p_{rn}) C_d) \approx 3.00$.
*   Both methods yield the same value.

**(4) Sensitivity**
If $q$ changes to 80%, $S_0$ changes.
If $S_0$ changes, $p_{rn}$ changes (because tree bounds are fixed values 10 and 21, not multiplicative $u,d$ factors relative to $S_0$).
New $S_0$ leads to different Option Value.

**(5) Put Value**
Use Put-Call Parity or Tree.

**(6) ATM Forward**
Value $= S_0 - K e^{-rT}$. If $K=S_0$, Value $= S_0(1 - e^{-rT})$.
Positive value.
