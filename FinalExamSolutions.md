# Financial Instruments Final Exam (2024) — Worked Solutions

## Question 1 – Conceptual
- **Monte Carlo vs. binomial:** Monte Carlo scales to many risk factors and path-dependent payoffs, whereas the binomial lattice is efficient for single-underlying vanilla or early-exercise options. Binomial trees provide hedge ratios at nodes; Monte Carlo requires variance reduction and regression for early exercise and converges at \(O(N^{-1/2})\).
- **ATM European call vs. put:** With no dividends and identical maturity/strike, put–call parity \(C - P = S_{0} - Ke^{-rT}\) implies near-equal prices at the money; neither option is systematically more valuable.
- **FX futures as predictors:** FX futures embed interest differentials and risk premia (cost-of-carry), so they reflect arbitrage pricing rather than an unbiased forecast of the future spot rate.

## Question 2 – FX Forwards and Currency Swap
Forward pricing uses
\[
F(T) = S_{0}e^{(r_{d}-r_{f})T}.
\]

```latex
\begin{document}
\begin{tabular}{|c|c|}
\hline
Maturity (years) & Forward USD/EUR \\ \hline
0.50 & 1.0945 \\ \hline
1.00 & 1.0891 \\ \hline
1.50 & 1.0836 \\ \hline
\end{tabular}
\end{document}
```

- Semi-annual euro cash flows: \(2.5, 2.5, 102.5\) million at \(T=0.5,1.0,1.5\).
- Fair fixed USD/EUR swap rate (single rate for coupons and principal): \(K \approx 1.0840\).
- If principal is exchanged at spot \(1.10\) while coupons use \(K\), PV gain to the firm \(\approx \$1.51\) million (receive euros, pay fewer dollars than fair forward).
- After both curves flatten to 4% (forwards collapse to spot), the mark-to-market of the original swap is \(+\$1.62\) million to the firm because fixed USD payments are above new forward-equivalent terms.

## Question 3 – Merton Structural Model
Equity viewed as a call on assets with strike equal to debt face \(D=400\) (million), \(A_{0}=500\), \(\sigma_{A}=25\%\), \(r=2\%\), \(T=7\).

```latex
\begin{document}
\begin{tabular}{|c|c|}
\hline
Metric & Value \\ \hline
Equity value (million) & 201.33 \\ \hline
Share price ($) & 0.0004 \\ \hline
Equity volatility & 0.5032 \\ \hline
Debt value (million) & 298.67 \\ \hline
Debt yield & 0.0417 \\ \hline
Risk-neutral $P(\text{default})$ & 0.4136 \\ \hline
Debt spread vs. $r$ & 0.0217 \\ \hline
\end{tabular}
\end{document}
```

For equal senior/subordinated halves (\(200\) face each):

```latex
\begin{document}
\begin{tabular}{|c|c|c|}
\hline
Tranche & Value (million) & Yield \\ \hline
Senior 200 & 178.26 & 0.0164 \\ \hline
Subordinated 200 & 129.18 & 0.0624 \\ \hline
\end{tabular}
\end{document}
```

The senior piece benefits from structural subordination and prices near risk-free; the subordinated piece absorbs most default risk and commands a higher spread. Default probability is unchanged because the asset process is unchanged—only loss allocation differs.

## Question 4 – Binomial Option Pricing
Parameters: \(S_{0}=100\), \(u=1.2\), \(d=1/1.2\), \(r=2\%\) (continuous, annual steps). Risk-neutral probability \(p = 0.5096\).

- Two-year European call (and American without dividends) \(\approx 10.98\).
- With a conditional \$10 dividend at end of year 2 if \(S_{2} \ge 100\), the 3-year American call values to \(\approx 10.95\).

Year-2 ex-dividend node prices:

```latex
\begin{document}
\begin{tabular}{|c|c|}
\hline
State & $S_{2}$ after dividend \\ \hline
$dd$ & 69.44 \\ \hline
$du$ & 90.00 \\ \hline
$ud$ & 90.00 \\ \hline
$uu$ & 134.00 \\ \hline
\end{tabular}
\end{document}
```

The dividend makes early exercise around the high node attractive; absent the dividend, American and European prices coincide. If the buyer will not exercise at year 2, the seller hedges to maturity using the year-3 European continuation values at each node.

## Question 5 – Structured Product
Payoff: principal-protected to \$1{,}000 for negative returns; linear participation \(2\times\) between 0–20% (\(1000 + 2000R = 2S_{T} - 1000\)); capped at \$1{,}400 above 20%. Static replication:
\[
\text{Payoff} = 1000\,e^{-rT} + 2C(K{=}1000) - 2C(K{=}1200).
\]

Given puts \(P_{1000}=50\), \(P_{1200}=188\) and \(r=2\%\):

```latex
\begin{document}
\begin{tabular}{|c|c|}
\hline
Component & Value \\ \hline
Call $K=1000$ & 69.80 \\ \hline
Call $K=1200$ & 11.76 \\ \hline
Structured product price & 1096.28 \\ \hline
\end{tabular}
\end{document}
```

Black–Scholes (\(\sigma=30\%\)) yields \(V_{\text{BS}}\approx 1116.68\), so selling at the replication price appears rich (model recommends selling).

Hedging (delta of short product = negative of below):

```latex
\begin{document}
\begin{tabular}{|c|c|c|}
\hline
Underlying & Product $\Delta$ & Beta approx. \\ \hline
1000 & 0.4758 & 0.3467 \\ \hline
1300 & 0.3536 & 0.3350 \\ \hline
\end{tabular}
\end{document}
```

The hedge mixes index units (per delta) and a financing leg in the risk-free asset. Delta shrinks as the index rallies because the position is capped.
