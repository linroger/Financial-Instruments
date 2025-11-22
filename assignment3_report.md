# Financial Instruments - Homework 3

## 1. The Goldman Sachs - Greece Currency Swap

**1.1 Compute the fair swap rate.**

Using the Zero Coupon Bond prices provided:
*   $PV(USD\_Leg) = \sum CF_{USD} \times Z_{US}(t)$.
    *   Coupons: 1.5 billion USD (semiannual).
    *   Principal: 50 billion USD.
*   $PV(EUR\_Leg) = \sum CF_{EUR} \times Z_{EU}(t)$.
    *   Coupons: $c \times 59 / 2$.
    *   Principal: 59 billion EUR.
*   Equation: $PV(USD\_Leg) = S_0 \times PV(EUR\_Leg)$. ($S_0 = 0.8475$).

**Result:**
Fair Rate $c_{EUR} \approx 5.05\%$. (Calculated in notebook).

**1.2 Value of Goldman Sachs Deal.**
*   Exchange Rate used: 0.8148 (Off-market).
*   Greece receives more EUR initially: $50 / 0.8148 = 61.36$ billion EUR.
*   Market Value of EUR received: $61.36 \times 0.8475 = 52.00$ billion USD.
*   Greece pays 50 billion USD.
*   **Upfront Gain:** 2.00 billion USD.
*   Swap Rate: 7.00%.
*   PV of Liabilities (EUR Leg): Calculated using 7% on 61.36b base.
*   PV of Assets (USD Leg): Same as above.
*   **Net Value:** Likely positive at inception (approx 2 billion), effectively a loan disguised as a swap.

## 2. Hedging with Options: Southwest

**2.1 Straight Insurance**
*   Buy Call Options (Strike 105).
*   Protects against prices rising above 105.
*   Cost: Premium paid upfront.
*   Payoff: $\max(S_T - 105, 0) - Premium$.

**2.2 Zero-Cost Collar**
*   Buy Call 105 (Price 2541).
*   Sell Put with matching price.
*   Looking at table, Put Strike 88.61 has price 2541.
*   **Strategy:** Buy Call 105, Sell Put 88.61.
*   **Net Cost:** 0.
*   **Payoff:**
    *   If $S_T > 105$: Protected (Gain on Call).
    *   If $88.61 < S_T < 105$: Pay Market Price (No option payoff).
    *   If $S_T < 88.61$: Loss on Put (Must buy at 88.61, worse than market). But implicit gain on fuel cost.

**2.3 Implied Interest Rate**
Using Put-Call Parity for Strike 105:
$$ C - P = S - K e^{-rT} $$
$$ 2.541 - 11.366 = 95 - 105 e^{-r(0.25)} $$
$$ -8.825 = 95 - 105 D $$
$$ 105 D = 103.825 $$
$$ D = 0.9888 $$
$$ r = -\ln(0.9888) / 0.25 \approx 0.045 $$
**Implied Rate: ~4.5%**
