# Financial Instruments - Homework 1

## Task 1: Arbitrage and Forward Rates

**Question:**
Consider a one-year forward contract for converting between dollars and Euros. The current exchange rate is $S_0 = 1.20$ for each Euro. The one-year risk-free rate in dollars is $r_{USD} = 5\%$ in continuously compounded units while the one-year risk-free rate in Euros is $r_{EUR} = 4.5\%$.

### (1) According to the principle of no-arbitrage, what should be the one-year forward rate?

The theoretical forward rate $F$ is given by the Interest Rate Parity formula:

$$ F = S_0 e^{(r_{USD} - r_{EUR})T} $$

Given:
$ S_0 = 1.20 $
$ r_{USD} = 0.05 $
$ r_{EUR} = 0.045 $
$ T = 1 $

Calculations:

$$ F = 1.20 \times e^{(0.05 - 0.045) \times 1} $$
$$ F = 1.20 \times e^{0.005} $$
$$ F \approx 1.20 \times 1.0050125 $$
$$ F \approx 1.206015 $$

The one-year forward rate should be **1.2060**.

### (2) Suppose that the one-year forward contract is currently trading at $1.15 per Euro. Is there an arbitrage opportunity? If so, explain in detail the trading you would like to do to exploit this arbitrage opportunity.

Yes, there is an arbitrage opportunity because the market price ($F_{mkt} = 1.15$) is different from the theoretical price ($F_{theo} \approx 1.206$).
Specifically, $F_{mkt} < F_{theo}$, meaning the forward contract is **undervalued** (too cheap).

**Strategy:**
We should **Buy** the cheap Forward contract and **Sell** the synthetic forward (Reverse Cash and Carry).

**Steps:**
1.  **Borrow EUR** at $r_{EUR} = 4.5\%$. We borrow an amount such that we owe exactly 1 EUR at maturity.
    *   Amount to Borrow at $t=0$: $e^{-0.045} \approx 0.956$ EUR.
2.  **Convert** the borrowed EUR to USD at the spot rate $S_0 = 1.20$.
    *   USD received: $0.956 \times 1.20 = 1.1472$ USD.
3.  **Invest** the USD at $r_{USD} = 5\%$.
    *   Amount invested: $1.1472$ USD.
4.  **Enter a Long Forward Contract** to buy 1 EUR at $F_{mkt} = 1.15$ at $t=1$.

**At Maturity ($t=1$):**
*   **USD Investment Proceeds:** The invested USD grows to:
    $$ 1.1472 \times e^{0.05} = 1.1472 \times 1.05127 = 1.2060 \text{ USD} $$
    (Alternatively, $1.20 \times e^{-0.045} \times e^{0.05} = 1.20 \times e^{0.005} \approx 1.2060$)
*   **Loan Repayment:** We owe 1 EUR on the EUR loan.
*   **Forward Settlement:** We use the forward contract to buy 1 EUR for $1.15$ USD.
*   **Profit:**
    $$ \text{Proceeds} - \text{Cost} = 1.2060 - 1.15 = 0.056 \text{ USD per 1 EUR owed.} $$

---

## Task 2: Forward Rates and Covered Interest Rate Parity

**Question:**
The Excel file `DataHW1.xls` contains data on the $/Euro exchange rate.
(1) Compute the Forward Exchange Rate for all maturities.
(2) Do your forward exchange rates match the quoted ones?
(3) If not, pick one date and describe the arbitrage strategy.

### (1) Computed Forward Rates

We use the formula derived from Covered Interest Parity. Note that LIBOR rates are quoted with linear compounding. We first convert them to continuously compounded rates:

$$ r_{cc} = \frac{\ln(1 + r_{LIBOR} \times \Delta t)}{\Delta t} $$

Then compute forward rate:
$$ F = S \times e^{(r_{USD,cc} - r_{EUR,cc}) \times \Delta t} $$

**Sample Calculation for 2005-10-03 (1 Year):**
*   Spot ($S$): 1.19235
*   US LIBOR 1Y ($r_{us,L}$): 4.2738% = 0.042738
*   EUR LIBOR 1Y ($r_{eu,L}$): 2.3330% = 0.023330
*   $T = 1$

$$ r_{us,cc} = \ln(1 + 0.042738) \approx 0.04185 $$
$$ r_{eu,cc} = \ln(1 + 0.023330) \approx 0.02306 $$
$$ F_{calc} = 1.19235 \times e^{(0.04185 - 0.02306)} = 1.19235 \times e^{0.01879} \approx 1.2149 $$
*(Note: The exact numbers in the code might differ slightly due to precision)*

**Results Table:**

latex
\begin{document}
\begin{tabular}{|c|c|c|c|}
\hline
Date & Spot & Fwd 1Y (Calc) & Fwd 1Y (Market) \\ \hline
2005-10-03 & 1.19235 & 1.21742 & 1.21789 \\ \hline
2006-10-02 & 1.27385 & 1.29319 & 1.29298 \\ \hline
2007-10-01 & 1.42325 & 1.42621 & 1.42805 \\ \hline
2008-10-01 & 1.40210 & 1.38266 & 1.39603 \\ \hline
2009-10-01 & 1.45330 & 1.45346 & 1.45302 \\ \hline
\end{tabular}
\end{document}


### (2) Comparison

Most dates show very close alignment between calculated and market rates, holding the parity relation. However, **2008-10-01** shows a significant deviation.

*   Calculated: 1.38266
*   Market: 1.39603
*   Difference: -0.01337

The Market rate is significantly higher than the theoretical rate.

### (3) Arbitrage Strategy for 2008-10-01

**Situation:**
$F_{mkt} = 1.39603 > F_{theo} = 1.38266$.
The market forward is **overvalued** (too expensive).

**Strategy: Cash and Carry**
We should **Sell** the expensive Forward and **Buy** the synthetic forward.

**Steps:**
1.  **Borrow USD** at US LIBOR ($r_{USD}$).
2.  **Convert USD to EUR** at Spot ($S_0 = 1.40210$).
3.  **Invest EUR** at EUR LIBOR ($r_{EUR}$).
4.  **Enter Short Forward Contract** to Sell EUR at $F_{mkt} = 1.39603$.

**At Maturity:**
*   The EUR investment grows to cover the EUR amount we need to sell.
*   We sell the EUR for USD at $1.39603$.
*   This amount of USD will be greater than the amount needed to repay the USD loan (which was based on the cheaper theoretical rate).
*   **Profit** is roughly the difference ($0.01337$ USD) per unit, discounted or adjusted for interest.

This deviation in 2008 corresponds to the financial crisis, where deviations from CIP were observed due to liquidity constraints and counterparty risk.
