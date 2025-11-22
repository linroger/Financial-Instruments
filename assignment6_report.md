# Financial Instruments - Homework 6

## 1. Implied Volatility

**Assumptions:**
*   **Spot Price ($S_0$):** 5022.0 (Feb 12, 2024).
*   **Maturity ($T$):** June 21, 2024 (130 days / 365 = 0.356 years).
*   **Risk-Free Rate ($r$):** 5.4% (4-month T-Bill).
*   **Dividend Yield ($q$):** 1.5%.

**Result:**
For the ATM Call ($K \approx 5020$), the Implied Volatility is calculated in the notebook (typically around 12-15% for SPX in early 2024, code computes exact value).

## 2. Valuing a Structured Security (PLUS)

**Decomposition:**
The PLUS note (Principal \$10, 300% Upside, Cap 11.90, 1 Year) can be decomposed into:
1.  **Long 1 Unit of Index** (Downside exposure, normalized to $10).
    *   Value: $10 \times e^{-qT}$. (Discounted due to no dividends).
2.  **Long 2 ATM Calls** (Leverage).
    *   Strike $S_0$. Notional $10 \times (1/S_0) \times 2$.
3.  **Short 3 OTM Calls** (Cap).
    *   Strike $K_{cap} = S_0 \times (1 + 19\%/3) \approx 1.0633 S_0$.
    *   Notional $10 \times (1/S_0) \times 3$.

**Valuation:**
Using the Implied Volatility from Part 1 (assuming constant term structure/smile):
*   The Fair Value is computed in the notebook.
*   It is typically less than \$10 (Par) due to fees and issuer profit margin built in.
*   The value comes from: $V_{stock} + V_{LongCalls} - V_{ShortCalls}$.

**Par Value Adjustment:**
To bring the value to Par ($10) today:
*   **Increase the Cap:** This pushes the strike of the Short Calls higher (Shorting cheaper options), increasing net value.
*   **Increase Participation:** Not possible if value is low? No, increasing participation increases value.
*   **Decrease Fees?**

**Sensitivity (Beta):**
*   **Beta ($\beta$):** Percentage change in PLUS value for percentage change in Index.
*   $\beta = \frac{\partial V}{\partial S} \times \frac{S}{V} = \Delta_{plus} \times \frac{S}{V}$.
*   $\Delta_{plus} = \Delta_{stock} + 2 \Delta_{C1} - 3 \Delta_{C2}$.
    *   $\Delta_{stock} \approx 10/S_0 \times e^{-qT}$? (Unit delta). No, Value is $10 S/S_0$. Delta wrt $S$ is $10/S_0$.
*   **Behavior:**
    *   **Low S:** Delta is 1 (Downside tracking). Beta $\approx 1$.
    *   **Medium S:** Delta is $1 + 2 \times 1 = 3$. Beta $\approx 3$.
    *   **High S (above Cap):** Delta is $1 + 2 - 3 = 0$. Beta $\approx 0$.
*   Beta is dynamic.
