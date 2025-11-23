# Financial Instruments Solutions Overview

This document rewrites each task succinctly and records the step-by-step reasoning, math, and outputs produced in the accompanying notebooks.

## Homework 1
1. **Price a 1-year USD/EUR forward with \(S_{0}=1.20\), \(r_{USD}=5\%\), \(r_{EUR}=4.5\%\).**  
   Using covered interest parity, \(F_{0,T}=S_{0}e^{(r_{d}-r_{f})T}=1.2060\). The market quote of 1.15 is underpriced, so arbitrage borrows USD, converts to EUR, invests in EUR, and goes long the forward to lock in cheap repurchase of USD.
2. **Check covered interest parity across historical LIBOR/forward quotes.**  
   LIBOR quotes were converted from simple to continuously compounded rates, forward parities computed, and deviations plotted. The largest violation occurs on 2008-10-01 for the 1Y tenor.

Forward versus quoted (sample observations):
```latex
\begin{document}
\begin{tabular}{|c|c|c|c|c|}
\hline
Date & Tenor & Theoretical & Quoted & Deviation \\ \hline
2008-10-01 & 1Y & 1.3827 & 1.3960 & 0.0134 \\ \hline
2006-10-02 & 1Y & 1.2932 & 1.2930 & -0.0002 \\ \hline
2009-10-01 & 1Y & 1.4535 & 1.4530 & -0.0004 \\ \hline
\end{tabular}
\end{document}
```

## Homework 2
1. **Revisit the Oct 1, 2008 forward arbitrage.**  
   The quoted 1Y forward (1.4103) exceeded the fair value (1.3827). After six months, the forward’s value given new spot/rates is computed via \(V_{short}=(K-F_{t})e^{-r_{d}(T-t)}\), yielding a modest positive PV for the short leg. The synthetic long forward PV is compared to confirm arbitrage profitability.
2. **Southwest jet-fuel hedge via crude futures.**  
   Cleaned daily FEB/MAR/APR-08 futures and jet-fuel series; matched nearest settlement dates; computed contract needs for a 75% hedge and the implicit fuel cost after futures P&L. Plotly lines compare crude and fuel paths.
3. **Calendar spread (Amaranth) discussion.**  
   Daily P&L is obtained by multiplying price changes by contract counts; cumulative cash needs follow from margin rules.

## Homework 3
1. **Greece currency swap.**  
   With USD coupons at 6% on USD 50B vs. EUR receipts on EUR 59B, discounting ZCB curves implies an equilibrium semi-annual EUR rate near 6.43%. Using Goldman’s historical FX (0.8148) and 7% EUR coupon produces a positive PV for Greece due to favorable principal exchange.
2. **Jet-fuel option hedges.**  
   105-strike calls: ~26,982 contracts (per 1,000-barrel lots) hedge 75% of Q1 fuel. Zero-cost collars trade off put strikes; payoff diagrams in the notebook compare insurance vs. collar structures.

## Homework 4
1. **Barings/Leeson short straddle.**  
   Shorting ATM Nikkei call+put at 19,750 generates premium income but large downside. Final Nikkei at 17,473 implies a sizable loss; payoff curves illustrate the unlimited risk of the strategy.
2. **Binomial intuition for FDA approval.**  
   Stock pricing under CAPM and replication/risk-neutral methods yield consistent call/put prices, showing how probability and discount-rate shifts change option values.

## Homework 5
1. **FDA drug approval binomial tree.**  
   CAPM-implied \(S_{0}\approx15.53\); risk-neutral probability \(p^{*}=0.63\); ATM 1-year call ≈ 3.00 and put ≈ 0.77 (rounded). Sensitivity to approval probability and beta is discussed in-line.

## Homework 6
1. **PLUS structured note payoff.**  
   Visualized the capped leveraged upside (300% participation up to $11.90) and full downside exposure. The plot clarifies how leverage plus cap alters the payoff versus linear equity exposure.

## Homework 7
1. **American options on a 3-period tree.**  
   With \(u=1.1\), \(d=1/u\), \(p=0.6\), \(r=2\%\), ATM American call ≈ 10.80 and put ≈ 4.39; early exercise is optimal only for the put at low nodes.
2. **KMV-style default estimate for Citigroup.**  
   Using balance-sheet items (deposits, long-term debt, assets) and an assumed 30% asset volatility, the distance to default is computed to gauge 1-year PD; the bailout announcement effect can be recomputed by shocking assets/volatility in the notebook sliders.

---

Both the Jupyter notebook (`financial_instruments.ipynb`) and the marimo app (`financial_instruments_marimo.py`) contain full code, calculations, and Plotly visualizations.
