# Financial Instruments Final Exam 2024

## 1. Short Answer

**(a) Monte Carlo vs Binomial**
*   **Advantages of MC:** Can easily handle path-dependent options (like Asians, Lookbacks) where the payoff depends on the history of the price, not just the terminal value or current node. Handles multiple underlying assets (high dimensionality) well.
*   **Disadvantages of MC:** Difficult to handle American options (early exercise optimization) compared to the backward induction of Binomial Trees. Convergence is slower ($1/\sqrt{N}$ vs $1/N$).

**(b) Call vs Put Value**
For ATM European options ($S=K$):
$C - P = S - K e^{-rT} = S (1 - e^{-rT})$.
If interest rates are positive ($r > 0$), $C > P$.
Reason: You pay strike later for Call (advantage), receive strike later for Put (disadvantage).

**(c) Futures Forecasting**
Futures prices are determined by arbitrage (Cost of Carry), not by expectations. $F = S e^{(r-q)T}$. They reflect the spot price adjusted for interest and dividends, not necessarily the market's forecast of future spot prices (unless Risk Neutral = Physical Measure, i.e., zero risk premium, which is rare).

## 2. Swap

**(a) Forward Rates**
Calculated:
*   6m: $1.1 \times e^{(0.04-0.05) \times 0.5} \approx 1.0945$.
*   1y: $1.1 \times e^{-0.01} \approx 1.0891$.
*   18m: $1.1 \times e^{-0.015} \approx 1.0836$.

**(b) Swap Rate**
Par Swap Rate for USD (paying fixed USD, receiving USD equivalent flows) given flat 4% yield curve is 4%.
Equation: $PV_{Fixed} = PV_{Float} = Notional$.
Swap Rate = 4%.

**(c) Off-Market Principal**
Exchanging principal at 1.1 (current spot) at maturity is standard for currency swaps.
Assuming fair pricing, value is zero.

**(d) Yield Shift**
If Euro yields drop to 4% (same as USD), the value of the liability (Paying Euros) increases (discount rate drops).
The swap (Pay EUR, Receive USD) loses value for the firm.

## 3. Merton Model

**(a) Stock Price**
Using Black-Scholes call formula on Assets ($V=500, K=400, \sigma=25\%, r=2\%, T=7$).
*   Equity Value $E \approx 197.55$ million.
*   Price per Share ($N=0.5$m): $\$395.10$.

**(b) Equity Volatility**
$\sigma_E = \frac{V}{E} N(d_1) \sigma_V \approx 47.5\%$.

**(c) Debt**
*   Debt Value $D = V - E \approx 302.45$.
*   Yield $y = -\ln(302.45/400)/7 \approx 4.00\%$.
*   Spread = 2.00%.
*   PD = $N(-d_2) \approx 31\%$.

## 4. Options

**(a) European Call**
Binomial Tree ($u=1.2, d=1/1.2, T=2$).
Price calculated.

**(c) Special Dividend**
American Call. Check early exercise at nodes before dividend payment.
If dividend is large, early exercise might be optimal.

## 5. Structured Product

**(b) Valuation**
Decomposition: Bond + 2 ATM Calls - 2 OTM Calls ($K=1200$).
Using market prices:
*   Call(1000) derived from Put(1000): $C = 50 + 1000 - 1000 e^{-0.02} \approx 69.8$.
*   Call(1200) derived from Put(1200): $C = 188 + 1000 - 1200 e^{-0.02} \approx 11.8$.
*   Value = $1000 e^{-0.02} + 2(69.8) - 2(11.8) \approx 980 + 116 = 1096$.

**(c) Decision**
If BS Model with $\sigma=30\%$ gives a lower price than Market (1096), you should Sell.
If Market implies lower vol, sell Market, hedge with Model?
Usually if Model Price < Market Price, Asset is Overvalued -> Sell.

**(d) Hedging**
Delta Hedge using Index and Bonds.
$\Delta = 2 \Delta_{C1} - 2 \Delta_{C2}$.
Hold $\Delta$ units of Index. Borrow remaining amount.
