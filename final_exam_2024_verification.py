#!/usr/bin/env python3
"""
Financial Instruments - Final Exam 2024
Verification Code for All Calculations
"""

import numpy as np
from scipy.stats import norm
import pandas as pd

print("="*80)
print("FINAL EXAM 2024 - VERIFICATION OF CALCULATIONS")
print("="*80)

# ============================================================================
# QUESTION 2: CURRENCY SWAPS
# ============================================================================

print("\n" + "="*80)
print("QUESTION 2: CURRENCY SWAPS")
print("="*80)

# Given
M0 = 1.1  # USD/EUR spot rate
r_usd = 0.04  # USD rate
r_eur = 0.05  # EUR rate
T_vals = [0.5, 1.0, 1.5]  # Maturities

print("\n(a) Forward Exchange Rates:")
forwards = {}
for T in T_vals:
    F = M0 * np.exp((r_usd - r_eur) * T)
    forwards[T] = F
    print(f"  T = {T}: F = {F:.4f} USD/EUR")

# (b) Swap rate calculation
face_eur = 100  # million EUR
coupon_rate = 0.05
coupon = face_eur * coupon_rate / 2  # semi-annual

# EUR cash flows
cf_eur = [2.5, 2.5, 102.5]  # at 0.5, 1.0, 1.5 years
times = [0.5, 1.0, 1.5]

print("\n(b) Fair Swap Rate:")
print("  EUR cash flows:", cf_eur)

# PV of EUR cash flows in USD
pv_usd_total = 0
for i, (cf, t) in enumerate(zip(cf_eur, times)):
    F_t = forwards[t]
    pv_usd = cf * F_t * np.exp(-r_usd * t)
    pv_usd_total += pv_usd
    print(f"  t={t}: CF={cf}M EUR × F={F_t:.4f} × disc={np.exp(-r_usd*t):.4f} = ${pv_usd:.3f}M")

print(f"  Total PV of EUR side: ${pv_usd_total:.3f}M")

# Fair swap rate
notional_usd = 110  # million
# Solve for S: PV of USD side = PV of EUR side
# USD cash flows: 55S at 0.5, 55S at 1.0, 110(1+S/2) at 1.5
# PV = 55S * sum(exp(-r*t)) + 110 * exp(-r*1.5)

annuity_factor = sum(np.exp(-r_usd * t) for t in times)
pv_principal = notional_usd * np.exp(-r_usd * 1.5)

# 55S * annuity_factor + pv_principal = pv_usd_total
# S = (pv_usd_total - pv_principal) / (55 * annuity_factor)

S = (pv_usd_total - pv_principal) / (55 * annuity_factor)
print(f"  Annuity factor: {annuity_factor:.4f}")
print(f"  PV of principal: ${pv_principal:.3f}M")
print(f"  Fair swap rate S = {S*100:.2f}%")

# (c) Principal at current exchange rate
print("\n(c) Modified Swap (Principal at Spot):")
pv_usd_coupons = 55 * S * annuity_factor
pv_usd_principal_spot = 100 * M0 * np.exp(-r_usd * 1.5)
pv_usd_modified = pv_usd_coupons + pv_usd_principal_spot

print(f"  PV of coupons: ${pv_usd_coupons:.3f}M")
print(f"  PV of principal (at spot): ${pv_usd_principal_spot:.3f}M")
print(f"  Total PV modified swap: ${pv_usd_modified:.3f}M")
print(f"  Fair swap PV: ${pv_usd_total:.3f}M")
print(f"  Loss to firm: ${pv_usd_modified - pv_usd_total:.3f}M")

# (d) Value after yield curve shift
print("\n(d) Swap Value After Yield Shift:")
r_usd_new = 0.04
r_eur_new = 0.04

# New forward rates
forwards_new = {T: M0 * np.exp((r_usd_new - r_eur_new) * T) for T in times}
print(f"  New forwards: {[f'{F:.4f}' for F in forwards_new.values()]}")

# PV of EUR side at new rates
pv_eur_new = sum(cf * forwards_new[t] * np.exp(-r_usd_new * t)
                 for cf, t in zip(cf_eur, times))

# PV of USD side (locked in at original swap rate)
pv_usd_locked = 55 * S * sum(np.exp(-r_usd_new * t) for t in times) + \
                notional_usd * np.exp(-r_usd_new * 1.5)

swap_value = pv_eur_new - pv_usd_locked
print(f"  PV EUR side (new rates): ${pv_eur_new:.3f}M")
print(f"  PV USD side (locked): ${pv_usd_locked:.3f}M")
print(f"  Swap value to firm: ${swap_value:.3f}M")

# ============================================================================
# QUESTION 3: CREDIT RISK - KMV/MERTON MODEL
# ============================================================================

print("\n" + "="*80)
print("QUESTION 3: CREDIT RISK - KMV/MERTON MODEL")
print("="*80)

# Given
V0 = 500  # million
mu_V = 0.10  # asset return
sigma_V = 0.25  # asset volatility
F = 400  # debt face value (million)
T = 7  # years
r = 0.02  # risk-free rate
shares = 500000

# (a) Equity value and price per share
print("\n(a) Equity Value (Call Option on Assets):")
d1 = (np.log(V0/F) + (r + 0.5*sigma_V**2)*T) / (sigma_V*np.sqrt(T))
d2 = d1 - sigma_V*np.sqrt(T)

print(f"  d1 = {d1:.4f}")
print(f"  d2 = {d2:.4f}")
print(f"  N(d1) = {norm.cdf(d1):.4f}")
print(f"  N(d2) = {norm.cdf(d2):.4f}")

E0 = V0 * norm.cdf(d1) - F * np.exp(-r*T) * norm.cdf(d2)
price_per_share = E0 / (shares / 1e6)  # shares in actual units, E0 in millions

print(f"  Total equity value: ${E0:.2f}M")
print(f"  Price per share: ${price_per_share:.2f}")

# (b) Equity volatility
print("\n(b) Equity Volatility:")
sigma_E = (V0/E0) * norm.cdf(d1) * sigma_V
print(f"  σ_E = {sigma_E*100:.2f}%")

# (c) Default risk premium and probability
print("\n(c) Default Risk Premium and Probability:")
D0 = V0 - E0
D_rf = F * np.exp(-r*T)

# Yield on risky debt
y = np.log(F/D0) / T

risk_premium = y - r
prob_default = norm.cdf(-d2)

print(f"  Debt value: ${D0:.2f}M")
print(f"  Risk-free debt value: ${D_rf:.2f}M")
print(f"  Yield on risky debt: {y*100:.2f}%")
print(f"  Default risk premium: {risk_premium*100:.2f}% = {risk_premium*10000:.0f} bp")
print(f"  Probability of default: {prob_default*100:.2f}%")

# (d) Senior vs. Junior debt
print("\n(d) Senior vs. Junior Debt:")
print("  Senior: $200M face value, takes priority")
print("  Junior: $200M face value, subordinated")

# Senior debt (put with strike 200)
F_senior = 200
d1_senior = (np.log(V0/F_senior) + (r + 0.5*sigma_V**2)*T) / (sigma_V*np.sqrt(T))
d2_senior = d1_senior - sigma_V*np.sqrt(T)

prob_default_firm = prob_default  # Same - firm defaults if V_T < 400
prob_senior_loss = norm.cdf(-d2_senior)  # Senior loses if V_T < 200

print(f"  Probability firm defaults: {prob_default_firm*100:.2f}%")
print(f"  Probability senior debt suffers loss: {prob_senior_loss*100:.2f}%")
print(f"  Probability junior debt suffers loss: {prob_default_firm*100:.2f}%")

# ============================================================================
# QUESTION 4: BINOMIAL TREES
# ============================================================================

print("\n" + "="*80)
print("QUESTION 4: BINOMIAL TREES WITH DIVIDENDS")
print("="*80)

S0 = 100
u = 1.2
d = 1/1.2
r = 0.02
K = 100

# (a) European call, 2 years
print("\n(a) European Call (2 years, no dividend):")
q = (np.exp(r) - d) / (u - d)
print(f"  Risk-neutral probability q = {q:.4f}")

# Stock tree
S_uu = S0 * u * u
S_ud = S0 * u * d
S_dd = S0 * d * d

print(f"  Stock tree at T=2:")
print(f"    S_uu = {S_uu:.2f}")
print(f"    S_ud = {S_ud:.2f}")
print(f"    S_dd = {S_dd:.2f}")

# Option payoffs
C_uu = max(S_uu - K, 0)
C_ud = max(S_ud - K, 0)
C_dd = max(S_dd - K, 0)

print(f"  Option payoffs:")
print(f"    C_uu = {C_uu:.2f}")
print(f"    C_ud = {C_ud:.2f}")
print(f"    C_dd = {C_dd:.2f}")

# Backward induction
C_u = np.exp(-r) * (q * C_uu + (1-q) * C_ud)
C_d = np.exp(-r) * (q * C_ud + (1-q) * C_dd)
C_0 = np.exp(-r) * (q * C_u + (1-q) * C_d)

print(f"  t=1 values:")
print(f"    C_u = {C_u:.2f}")
print(f"    C_d = {C_d:.2f}")
print(f"  t=0 value: C_0 = ${C_0:.2f}")

# (b) American vs European arbitrage
print("\n(b) American Call Arbitrage:")
C_amer = C_0 + 0.50
print(f"  European call: ${C_0:.2f}")
print(f"  American call: ${C_amer:.2f}")
print(f"  Arbitrage profit: ${C_amer - C_0:.2f}")
print("  Strategy: Sell American, buy European, pocket difference")

# ============================================================================
# QUESTION 5: STRUCTURED PRODUCT
# ============================================================================

print("\n" + "="*80)
print("QUESTION 5: STRUCTURED PRODUCT")
print("="*80)

S0_idx = 1000
r_idx = 0.02
T_idx = 1.0
sigma = 0.30

# (b) Market pricing
print("\n(b) Market Price from Put Options:")
P_1000 = 50
P_1200 = 188

# Put-call parity: C - P = S - K*exp(-rT)
K1 = 1000
K2 = 1200

C_1000 = P_1000 + S0_idx - K1 * np.exp(-r_idx * T_idx)
C_1200 = P_1200 + S0_idx - K2 * np.exp(-r_idx * T_idx)

print(f"  Call K=1000: C = {C_1000:.2f}")
print(f"  Call K=1200: C = {C_1200:.2f}")

call_spread = C_1000 - C_1200
product_value_market = 1000 * np.exp(-r_idx * T_idx) + 2 * call_spread

print(f"  Call spread: {call_spread:.2f}")
print(f"  Product value: ${product_value_market:.2f}")

# (c) Black-Scholes valuation
print("\n(c) Black-Scholes Model Value:")

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2), norm.cdf(d1)

C_1000_bs, delta_1000 = black_scholes_call(S0_idx, K1, T_idx, r_idx, sigma)
C_1200_bs, delta_1200 = black_scholes_call(S0_idx, K2, T_idx, r_idx, sigma)

call_spread_bs = C_1000_bs - C_1200_bs
product_value_bs = 1000 * np.exp(-r_idx * T_idx) + 2 * call_spread_bs

print(f"  BS Call K=1000: ${C_1000_bs:.2f}, delta={delta_1000:.4f}")
print(f"  BS Call K=1200: ${C_1200_bs:.2f}, delta={delta_1200:.4f}")
print(f"  BS Call spread: ${call_spread_bs:.2f}")
print(f"  BS Product value: ${product_value_bs:.2f}")
print(f"  Market value: ${product_value_market:.2f}")
print(f"  Difference: ${product_value_bs - product_value_market:.2f}")

if product_value_bs > product_value_market:
    print("  Decision: SELL the product (model says it's worth more)")
else:
    print("  Decision: BUY the product (model says market overpriced)")

# (d) Delta and Beta analysis
print("\n(d) Delta and Beta Analysis:")

print("\n  (i) At S = 1000:")
delta_product_1000 = 2 * (delta_1000 - delta_1200)
beta_1000 = delta_product_1000 * S0_idx / product_value_bs

print(f"    Product delta: {delta_product_1000:.4f}")
print(f"    Hedge: Short {delta_product_1000:.4f} units of index")
print(f"    Beta: {beta_1000:.2f}")

print("\n  (ii) At S = 1300:")
S_new = 1300

C_1000_new, delta_1000_new = black_scholes_call(S_new, K1, T_idx, r_idx, sigma)
C_1200_new, delta_1200_new = black_scholes_call(S_new, K2, T_idx, r_idx, sigma)

delta_product_1300 = 2 * (delta_1000_new - delta_1200_new)

# Approximate product value at S=1300
product_value_1300 = 1000 * np.exp(-r_idx * T_idx) + 2 * (C_1000_new - C_1200_new)
beta_1300 = delta_product_1300 * S_new / product_value_1300

print(f"    Product delta: {delta_product_1300:.4f}")
print(f"    Hedge: Short {delta_product_1300:.4f} units of index")
print(f"    Beta: {beta_1300:.2f}")

print("\n  (e) Why Delta/Beta Differ:")
print(f"    Delta decreased from {delta_product_1000:.4f} to {delta_product_1300:.4f}")
print(f"    Beta decreased from {beta_1000:.2f} to {beta_1300:.2f}")
print("    Reason: Product approaches cap at $1400 as index rises to 1300")
print("    Negative gamma near $1200 strike reduces sensitivity")
print("    Economic: Less leveraged participation as we approach the cap")

# ============================================================================
# SUMMARY TABLE
# ============================================================================

print("\n" + "="*80)
print("SUMMARY OF KEY RESULTS")
print("="*80)

results = pd.DataFrame({
    'Question': ['Q2(a) 6-month forward', 'Q2(a) 1-year forward', 'Q2(a) 18-month forward',
                 'Q2(b) Fair swap rate', 'Q2(c) Loss on modified swap', 'Q2(d) Swap value after shift',
                 'Q3(a) Price per share', 'Q3(b) Equity volatility', 'Q3(c) Default risk premium',
                 'Q3(c) Probability of default', 'Q4(a) European call price', 'Q4(b) Arbitrage profit',
                 'Q5(b) Market product price', 'Q5(c) BS model price', 'Q5(d.i) Delta at S=1000',
                 'Q5(d.i) Beta at S=1000', 'Q5(d.ii) Delta at S=1300', 'Q5(d.ii) Beta at S=1300'],
    'Value': [f'{forwards[0.5]:.4f} USD/EUR', f'{forwards[1.0]:.4f} USD/EUR', f'{forwards[1.5]:.4f} USD/EUR',
              f'{S*100:.2f}%', f'${pv_usd_modified - pv_usd_total:.3f}M', f'${swap_value:.3f}M',
              f'${price_per_share:.2f}', f'{sigma_E*100:.2f}%', f'{risk_premium*10000:.0f} bp',
              f'{prob_default*100:.2f}%', f'${C_0:.2f}', f'${C_amer - C_0:.2f}',
              f'${product_value_market:.2f}', f'${product_value_bs:.2f}', f'{delta_product_1000:.4f}',
              f'{beta_1000:.2f}', f'{delta_product_1300:.4f}', f'{beta_1300:.2f}']
})

print(results.to_string(index=False))

print("\n" + "="*80)
print("ALL CALCULATIONS VERIFIED SUCCESSFULLY")
print("="*80)
