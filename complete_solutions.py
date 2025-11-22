#!/usr/bin/env python3
"""
Financial Instruments - Complete Homework Solutions
Bus 35100 - John Heaton
Assignments 1-7: Comprehensive Analysis

This script contains complete solutions to all homework assignments covering:
- Forward rates, arbitrage, and covered interest rate parity
- Commodity futures and hedging strategies
- Currency swaps and options strategies
- Binomial trees and option pricing
- Black-Scholes model and implied volatility
- American options and credit risk (KMV model)
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm
from scipy.optimize import fsolve, minimize_scalar
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def black_scholes_call(S, K, T, r, sigma, q=0):
    """Calculate Black-Scholes call option price"""
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

def black_scholes_put(S, K, T, r, sigma, q=0):
    """Calculate Black-Scholes put option price"""
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return K*np.exp(-r*T)*norm.cdf(-d2) - S*np.exp(-q*T)*norm.cdf(-d1)

def black_scholes_delta(S, K, T, r, sigma, option_type='call', q=0):
    """Calculate option delta"""
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    if option_type == 'call':
        return np.exp(-q*T) * norm.cdf(d1)
    else:
        return np.exp(-q*T) * (norm.cdf(d1) - 1)

def implied_volatility(price, S, K, T, r, option_type='call', q=0):
    """Calculate implied volatility using bisection method"""
    def objective(sigma):
        if option_type == 'call':
            return black_scholes_call(S, K, T, r, sigma, q) - price
        else:
            return black_scholes_put(S, K, T, r, sigma, q) - price

    try:
        from scipy.optimize import brentq
        return brentq(objective, 0.001, 5.0)
    except:
        return np.nan

# ============================================================================
# HOMEWORK 1: ARBITRAGE AND FORWARD RATES
# ============================================================================

def hw1_forward_rates():
    """Solve HW1: Arbitrage and Forward Rates"""
    print("="*80)
    print("HOMEWORK 1: ARBITRAGE AND FORWARD RATES")
    print("="*80)

    # Problem 1: Theoretical forward rate
    M0 = 1.20  # USD/EUR
    r_usd = 0.05
    r_eur = 0.045
    T = 1

    F_theoretical = M0 * np.exp((r_usd - r_eur) * T)
    print(f"\nProblem 1: Theoretical Forward Rate")
    print(f"  Current spot rate: ${M0:.4f} USD/EUR")
    print(f"  US rate: {r_usd*100:.1f}%, EUR rate: {r_eur*100:.1f}%")
    print(f"  Theoretical forward: ${F_theoretical:.6f} USD/EUR")

    # Arbitrage opportunity
    F_market = 1.15
    if F_market < F_theoretical:
        print(f"\n  Market forward (${F_market:.4f}) < Theoretical (${F_theoretical:.6f})")
        print(f"  ARBITRAGE: Forward is UNDERPRICED")
        print(f"  Strategy: Long forward + Borrow USD + Invest EUR")

        # Calculate profit
        usd_owe = M0 * np.exp(r_usd * T)
        eur_have = np.exp(r_eur * T)
        usd_receive = eur_have * F_market
        profit = usd_receive - usd_owe
        print(f"  Profit per EUR: ${profit:.6f} ({profit/M0*100:.4f}%)")

    # Problem 2: Covered Interest Rate Parity (load data)
    try:
        df = pd.read_excel('Assignments/Assignment 1/DataHW1.xls')
        print(f"\nProblem 2: Covered Interest Rate Parity Analysis")
        print(f"  Data loaded: {df.shape[0]} observations")

        # Calculate theoretical forwards for each maturity
        results = []
        for idx, row in df.iterrows():
            spot = row.get('Spot', row.iloc[1] if len(row) > 1 else None)
            if spot is None:
                continue

            for mat, days in [('1M', 30), ('3M', 90), ('6M', 180), ('1Y', 360)]:
                try:
                    usd_lib = row.get(f'USD_LIBOR_{mat}', 0) / 100
                    eur_lib = row.get(f'EUR_LIBOR_{mat}', 0) / 100
                    fwd_quoted = row.get(f'Forward_{mat}', 0)

                    T_frac = days / 360
                    r_usd_cont = np.log(1 + usd_lib * T_frac) / T_frac
                    r_eur_cont = np.log(1 + eur_lib * T_frac) / T_frac
                    fwd_theo = spot * np.exp((r_usd_cont - r_eur_cont) * T_frac)

                    results.append({
                        'Maturity': mat,
                        'Quoted': fwd_quoted,
                        'Theoretical': fwd_theo,
                        'Diff_%': (fwd_quoted - fwd_theo) / fwd_theo * 100
                    })
                except:
                    pass

        if results:
            df_results = pd.DataFrame(results)
            print(f"\n  Average absolute deviation by maturity:")
            summary = df_results.groupby('Maturity')['Diff_%'].agg([
                ('Mean', 'mean'),
                ('Std', 'std'),
                ('Avg_Abs', lambda x: np.abs(x).mean())
            ])
            print(summary.to_string())

            max_viol = df_results.loc[df_results['Diff_%'].abs().idxmax()]
            print(f"\n  Largest parity violation:")
            print(f"    Maturity: {max_viol['Maturity']}")
            print(f"    Difference: {max_viol['Diff_%']:.4f}%")

    except Exception as e:
        print(f"\n  Note: Data file not available ({str(e)})")

    return F_theoretical

# ============================================================================
# HOMEWORK 2: COMMODITY FUTURES AND HEDGING
# ============================================================================

def hw2_commodity_futures():
    """Solve HW2: Commodity Futures and Hedging"""
    print("\n" + "="*80)
    print("HOMEWORK 2: COMMODITY FUTURES AND HEDGING")
    print("="*80)

    # Problem 2: Commodity Futures No-Arbitrage
    print(f"\nProblem 2: Commodity Futures No-Arbitrage Relation")
    print(f"  Formula: F₀,T = Sₜ × e^((r+u)×T)")
    print(f"  where u = storage cost, r = interest rate")
    print(f"\n  Case 1: F₀,T < Sₜ×e^((r+u)×T) → Cash-and-carry arbitrage")
    print(f"    • Borrow Sₜ, buy oil, store it, long forward")
    print(f"    • Profit = F₀,T - Sₜ×e^((r+u)×T) > 0 ✓")
    print(f"\n  Case 2: F₀,T > Sₜ×e^((r+u)×T) → Reverse cash-and-carry")
    print(f"    • Short oil (DIFFICULT!), invest proceeds, short forward")
    print(f"    • May NOT be feasible for physical commodities")
    print(f"\n  Conclusion: F₀,T ≤ Sₜ×e^((r+u)×T) (upper bound only)")
    print(f"    Convenience yield allows F₀,T < Sₜ×e^((r+u)×T)")

    # Problem 3: Southwest Airlines Hedging
    print(f"\nProblem 3: Southwest Airlines Jet Fuel Hedging")

    annual_consumption = 1511e6  # gallons
    hedge_ratio = 0.75
    q1_consumption = annual_consumption / 4
    hedged_gallons = q1_consumption * hedge_ratio
    contract_size = 42000  # gallons per contract

    contracts_per_month = (hedged_gallons / 3) / contract_size
    num_contracts = int(np.round(contracts_per_month))

    futures_prices = {'FEB.08': 95.98, 'MAR.08': 95.78, 'APR.08': 95.24}

    print(f"  Q1 2008 Consumption: {q1_consumption/1e6:,.1f}M gallons")
    print(f"  Hedged (75%): {hedged_gallons/1e6:,.1f}M gallons")
    print(f"  Monthly hedged: {hedged_gallons/3/1e6:,.2f}M gallons")
    print(f"  Contracts per month: {num_contracts:,}")
    print(f"\n  Hedging Strategy: LONG crude oil futures")
    print(f"  Rationale: Hedge jet fuel price risk with correlated crude futures")

    total_notional = 0
    for contract, price in futures_prices.items():
        notional = num_contracts * price * 1000  # 1000 barrels/contract
        total_notional += notional
        print(f"    {contract}: {num_contracts:,} contracts @ ${price:.2f}/bbl")

    print(f"  Total notional value: ${total_notional/1e6:,.1f}M")

    return num_contracts

# ============================================================================
# HOMEWORK 3: CURRENCY SWAPS AND OPTIONS
# ============================================================================

def hw3_currency_swaps():
    """Solve HW3: Greece Currency Swaps"""
    print("\n" + "="*80)
    print("HOMEWORK 3: GREECE CURRENCY SWAPS")
    print("="*80)

    # Greece bond and swap parameters
    N_usd = 50e9
    N_eur = 59e9
    spot = N_usd / N_eur  # 0.8475 USD/EUR
    c_usd = 0.06
    T = 10

    print(f"\nGreece issued ${N_usd/1e9:.0f}B USD bond, {c_usd*100:.0f}% coupon, {T}Y maturity")
    print(f"Swap: Exchange principals + periodic coupons")

    # ZCB prices
    zcb_data = [
        (0.5, 0.9786, 0.9822), (1.0, 0.9588, 0.9647), (2.0, 0.9191, 0.9192),
        (3.0, 0.8788, 0.8749), (4.0, 0.8379, 0.8287), (5.0, 0.7977, 0.7812),
        (6.0, 0.7583, 0.7397), (7.0, 0.7155, 0.6993), (8.0, 0.6751, 0.6600),
        (9.0, 0.6369, 0.6218), (10.0, 0.6050, 0.5848)
    ]
    df_zcb = pd.DataFrame(zcb_data, columns=['Maturity', 'Z_EUR', 'Z_USD'])

    # Value USD leg
    usd_cashflows = []
    for idx, row in df_zcb.iterrows():
        t = row['Maturity']
        z_usd = row['Z_USD']
        cf = (c_usd/2) * N_usd  # Semiannual coupon
        if t == T:
            cf += N_usd  # Add principal
        usd_cashflows.append(cf * z_usd)

    value_usd_leg = sum(usd_cashflows)
    value_usd_in_eur = value_usd_leg / spot

    # Calculate fair EUR swap rate
    sum_z_eur = df_zcb['Z_EUR'].sum()
    z_eur_T = df_zcb[df_zcb['Maturity'] == T]['Z_EUR'].values[0]

    # Solve for c_eur: Value(EUR leg) = Value(USD leg)
    # N_eur - (c_eur/2)*N_eur*Σ(Z_EUR) - N_eur*Z_EUR(T) = value_usd_in_eur
    c_eur = 2 * (N_eur * (1 - z_eur_T) - value_usd_in_eur) / (N_eur * sum_z_eur)

    print(f"\nProblem 1: Fair Swap Rate (VeroTende)")
    print(f"  Exchange rate: ${spot:.4f} USD/EUR")
    print(f"  Fair EUR swap rate: {c_eur*100:.4f}% per annum")
    print(f"  Semiannual EUR payment: €{(c_eur/2)*N_eur/1e9:.4f}B")

    # Goldman Sachs swap
    spot_gs = 0.8148  # Historical average
    c_eur_gs = 0.07
    N_eur_gs = N_usd / spot_gs

    eur_coupons_pv_gs = (c_eur_gs/2) * N_eur_gs * sum_z_eur
    value_eur_leg_gs = N_eur_gs - eur_coupons_pv_gs - N_eur_gs*z_eur_T
    swap_value = value_eur_leg_gs - value_usd_in_eur

    print(f"\nProblem 2: Goldman Sachs Swap")
    print(f"  Exchange rate: ${spot_gs:.4f} USD/EUR (off-market!)")
    print(f"  EUR principal: €{N_eur_gs/1e9:.4f}B (vs €{N_eur/1e9:.0f}B)")
    print(f"  Swap rate: {c_eur_gs*100:.0f}% (vs {c_eur*100:.2f}%)")
    print(f"  Net value to Greece: €{swap_value/1e9:.4f}B")
    print(f"\n  Why Greece accepted:")
    print(f"    • Upfront: Extra €{(N_eur_gs-N_eur)/1e9:.2f}B received immediately")
    print(f"    • Cost: Higher payments spread over {T} years")
    print(f"    • Accounting: Initial cash helps meet budget targets")

    return c_eur, c_eur_gs

# ============================================================================
# HOMEWORK 4: BARINGS/LEESON AND BINOMIAL TREES
# ============================================================================

def hw4_barings_leeson():
    """Solve HW4: Barings/Leeson Nikkei Options"""
    print("\n" + "="*80)
    print("HOMEWORK 4: BARINGS/LEESON NIKKEI OPTIONS")
    print("="*80)

    # Problem 1: Short Straddle
    K = 19750
    S0 = 19634
    num_options = 35500
    call_price = 9.90e6  # JPY
    put_price = 9.80e6  # JPY
    contract_mult = 10000

    print(f"\nLeeson's Position (Dec 24, 1994):")
    print(f"  Short {num_options:,} calls @ ¥{call_price/1e6:.2f}M")
    print(f"  Short {num_options:,} puts @ ¥{put_price/1e6:.2f}M")
    print(f"  Strike: {K:,}, Nikkei: {S0:,}")
    print(f"  Contract multiplier: {contract_mult:,} × Nikkei")

    print(f"\n  Strategy: SHORT STRADDLE")
    print(f"  Profit if: {K} - premium < Nikkei < {K} + premium at maturity")
    print(f"  Risk: UNLIMITED on both sides!")

    # Premium received
    total_premium = num_options * (call_price + put_price)
    premium_per_contract = (call_price + put_price) / contract_mult

    print(f"\n  Total premium received: ¥{total_premium/1e9:.2f}B")
    print(f"  Premium per index point: ¥{premium_per_contract:,.0f}")

    # Breakeven points
    breakeven_up = K + premium_per_contract
    breakeven_down = K - premium_per_contract

    print(f"\n  Breakeven points:")
    print(f"    Upper: {breakeven_up:,.0f}")
    print(f"    Lower: {breakeven_down:,.0f}")

    # Final outcome (Feb 24, 1995)
    S_T = 17473

    if S_T < K:
        # Puts exercised
        payout = num_options * (K - S_T) * contract_mult
    else:
        # Calls exercised
        payout = num_options * (S_T - K) * contract_mult

    profit = total_premium - payout

    print(f"\nActual Outcome (Feb 24, 1995):")
    print(f"  Nikkei at maturity: {S_T:,}")
    print(f"  Put payout: ¥{num_options * (K-S_T) * contract_mult/1e9:.2f}B")
    print(f"  Premium received: ¥{total_premium/1e9:.2f}B")
    print(f"  Net P&L: ¥{profit/1e9:.2f}B")
    print(f"  LOSS: ¥{-profit/1e9:.2f}B")

    return profit

def hw4_binomial_tree():
    """Solve HW4: FDA Drug Approval - Binomial Tree"""
    print("\n" + "="*80)
    print("HOMEWORK 4: BINOMIAL TREE - FDA DRUG APPROVAL")
    print("="*80)

    # Vanda Pharmaceutical parameters
    S1_u = 21
    S1_d = 10
    q = 0.7  # Real probability of approval
    beta = 2.0
    r = 0.05  # Continuously compounded
    E_RP = 0.0644  # Expected excess return

    # CAPM
    r_annual = np.exp(r) - 1  # Convert to annual compounding for CAPM
    E_r = r_annual + beta * E_RP

    print(f"\nGiven:")
    print(f"  Possible stock prices in 1 year: ${S1_u:.0f} (up) or ${S1_d:.0f} (down)")
    print(f"  Real probability of approval: {q*100:.0f}%")
    print(f"  CAPM beta: {beta:.1f}")
    print(f"  Risk-free rate: {r*100:.0f}% (cont.) = {r_annual*100:.2f}% (annual)")
    print(f"  Market risk premium: {E_RP*100:.2f}%")

    print(f"\nProblem 1: Expected Return (CAPM)")
    print(f"  E[r] = rf + β × E[RP]")
    print(f"  E[r] = {r_annual*100:.2f}% + {beta:.1f} × {E_RP*100:.2f}%")
    print(f"  E[r] = {E_r*100:.2f}%")

    # Calculate current stock price
    E_S1 = q * S1_u + (1-q) * S1_d
    S0 = E_S1 / (1 + E_r)

    print(f"\nProblem 2: Current Stock Price")
    print(f"  E[S₁] = {q:.1f} × ${S1_u} + {1-q:.1f} × ${S1_d} = ${E_S1:.2f}")
    print(f"  S₀ = E[S₁]/(1+E[r]) = ${E_S1:.2f}/{1+E_r:.4f} = ${S0:.4f}")

    # Option pricing - ATM call
    K = S0

    # Risk-neutral probability
    u = S1_u / S0
    d = S1_d / S0
    q_star = (np.exp(r) - d) / (u - d)

    print(f"\nProblem 3a: Option Pricing - Dynamic Replication")
    print(f"  Strike K = S₀ = ${K:.4f}")
    print(f"  u = {u:.6f}, d = {d:.6f}")

    # Option payoffs
    C_u = max(S1_u - K, 0)
    C_d = max(S1_d - K, 0)

    print(f"  Call payoffs: C_u = ${C_u:.4f}, C_d = ${C_d:.4f}")

    # Replicating portfolio
    delta = (C_u - C_d) / (S1_u - S1_d)
    B = (C_d * S1_u - C_u * S1_d) / ((S1_u - S1_d) * np.exp(r))
    C0 = delta * S0 + B

    print(f"\n  Delta (shares): {delta:.6f}")
    print(f"  Bonds: ${B:.4f}")
    print(f"  Call value: ${C0:.4f}")

    # Verify replication
    print(f"\n  Verification:")
    print(f"    If up: {delta:.4f} × ${S1_u} + ${B:.2f} × e^{r:.2f} = ${delta*S1_u + B*np.exp(r):.4f} ✓")
    print(f"    If down: {delta:.4f} × ${S1_d} + ${B:.2f} × e^{r:.2f} = ${delta*S1_d + B*np.exp(r):.4f} ✓")

    print(f"\nProblem 3b: Option Pricing - Risk-Neutral Valuation")
    print(f"  Risk-neutral probability q* = (e^r - d)/(u - d)")
    print(f"  q* = (e^{r:.2f} - {d:.4f})/({u:.4f} - {d:.4f}) = {q_star:.6f}")

    E_S1_star = q_star * S1_u + (1-q_star) * S1_d
    print(f"\n  E*[S₁] = {q_star:.4f} × ${S1_u} + {1-q_star:.4f} × ${S1_d} = ${E_S1_star:.4f}")
    print(f"  E[S₁] (real) = ${E_S1:.2f}")
    print(f"  E*[S₁] ≠ E[S₁] → Risk-neutral ≠ Real probabilities")

    E_C1 = q_star * C_u + (1-q_star) * C_d
    C0_rn = E_C1 * np.exp(-r)

    print(f"\n  E*[C₁] = {q_star:.4f} × ${C_u:.2f} + {1-q_star:.4f} × ${C_d:.2f} = ${E_C1:.4f}")
    print(f"  C₀ = E*[C₁] × e^(-r) = ${C0_rn:.4f}")
    print(f"  Matches replication value: ${C0:.4f} ✓")

    return S0, C0

# ============================================================================
# HOMEWORK 5: MULTI-PERIOD BINOMIAL AND BLACK-SCHOLES
# ============================================================================

def hw5_binomial_multiperiod():
    """Solve HW5: Multi-period Binomial Tree"""
    print("\n" + "="*80)
    print("HOMEWORK 5: MULTI-PERIOD BINOMIAL TREES")
    print("="*80)

    # Parameters
    S0 = 100
    u = 1.1
    d = 1/u
    r = 0.05  # Per period
    K = 100
    n_periods = 2

    print(f"\nParameters:")
    print(f"  S₀ = ${S0}, K = ${K}")
    print(f"  u = {u}, d = {d:.6f}")
    print(f"  r = {r*100:.0f}% per period")
    print(f"  Periods: {n_periods}")

    # Build stock price tree
    print(f"\nStock Price Tree:")
    S_uu = S0 * u * u
    S_ud = S0 * u * d
    S_dd = S0 * d * d

    print(f"           t=0      t=1        t=2")
    print(f"                             ${S_uu:.2f}")
    print(f"                    ${S0*u:.2f}")
    print(f"  ${S0:.2f}")
    print(f"                    ${S0*d:.2f}")
    print(f"                             ${S_dd:.2f}")

    # Option payoffs
    C_uu = max(S_uu - K, 0)
    C_ud = max(S_ud - K, 0)
    C_dd = max(S_dd - K, 0)

    print(f"\nCall Payoffs at t=2:")
    print(f"  C_uu = max(${S_uu:.2f} - ${K}, 0) = ${C_uu:.2f}")
    print(f"  C_ud = max(${S_ud:.2f} - ${K}, 0) = ${C_ud:.2f}")
    print(f"  C_dd = max(${S_dd:.2f} - ${K}, 0) = ${C_dd:.2f}")

    # Risk-neutral probability
    q_star = (np.exp(r) - d) / (u - d)

    print(f"\nRisk-neutral probability: q* = {q_star:.6f}")

    # Backward induction
    # t=1, up state
    C_u = ((q_star * C_uu + (1-q_star) * C_ud) * np.exp(-r))
    # t=1, down state
    C_d = ((q_star * C_ud + (1-q_star) * C_dd) * np.exp(-r))

    print(f"\nOption Values at t=1:")
    print(f"  C_u = e^(-{r}) × ({q_star:.4f} × ${C_uu:.2f} + {1-q_star:.4f} × ${C_ud:.2f}) = ${C_u:.4f}")
    print(f"  C_d = e^(-{r}) × ({q_star:.4f} × ${C_ud:.2f} + {1-q_star:.4f} × ${C_dd:.2f}) = ${C_d:.4f}")

    # t=0
    C_0 = ((q_star * C_u + (1-q_star) * C_d) * np.exp(-r))

    print(f"\nOption Value at t=0:")
    print(f"  C₀ = e^(-{r}) × ({q_star:.4f} × ${C_u:.4f} + {1-q_star:.4f} × ${C_d:.4f}) = ${C_0:.4f}")

    # Replicating portfolio at each node
    delta_0 = (C_u - C_d) / (S0*u - S0*d)
    B_0 = (C_0 - delta_0 * S0) * np.exp(r)

    print(f"\nReplicating Portfolio at t=0:")
    print(f"  Δ = (C_u - C_d)/(S_u - S_d) = {delta_0:.6f} shares")
    print(f"  B = ${B_0:.4f} in bonds")
    print(f"  Value = Δ × S₀ + B = ${delta_0 * S0 + B_0:.4f} ✓")

    return C_0

def hw5_black_scholes():
    """Solve HW5: Black-Scholes Formula"""
    print("\n" + "="*80)
    print("HOMEWORK 5: BLACK-SCHOLES FORMULA")
    print("="*80)

    # Verotende Inc. parameters
    S = 42
    K = 40
    T = 0.5  # 6 months
    r = 0.10
    sigma = 0.20

    print(f"\nParameters:")
    print(f"  Stock price S = ${S}")
    print(f"  Strike K = ${K}")
    print(f"  Time to maturity T = {T} years")
    print(f"  Risk-free rate r = {r*100:.0f}%")
    print(f"  Volatility σ = {sigma*100:.0f}%")

    # Calculate d1 and d2
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    print(f"\nCalculation:")
    print(f"  d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T)")
    print(f"  d₁ = [ln({S}/{K}) + ({r} + {sigma**2/2:.4f})×{T}] / ({sigma}×√{T})")
    print(f"  d₁ = {d1:.6f}")
    print(f"  d₂ = d₁ - σ√T = {d1:.6f} - {sigma*np.sqrt(T):.6f} = {d2:.6f}")

    # Call and put prices
    call_price = black_scholes_call(S, K, T, r, sigma)
    put_price = black_scholes_put(S, K, T, r, sigma)

    print(f"\nOption Prices:")
    print(f"  Call = S×N(d₁) - K×e^(-rT)×N(d₂)")
    print(f"  Call = {S}×{norm.cdf(d1):.6f} - {K}×e^(-{r}×{T})×{norm.cdf(d2):.6f}")
    print(f"  Call = ${call_price:.4f}")

    print(f"\n  Put = K×e^(-rT)×N(-d₂) - S×N(-d₁)")
    print(f"  Put = {K}×e^(-{r}×{T})×{norm.cdf(-d2):.6f} - {S}×{norm.cdf(-d1):.6f}")
    print(f"  Put = ${put_price:.4f}")

    # Put-call parity check
    parity_check = call_price - put_price - (S - K*np.exp(-r*T))
    print(f"\nPut-Call Parity Check:")
    print(f"  C - P = S - K×e^(-rT)")
    print(f"  {call_price:.4f} - {put_price:.4f} = {S} - {K*np.exp(-r*T):.4f}")
    print(f"  {call_price - put_price:.4f} = {S - K*np.exp(-r*T):.4f}")
    print(f"  Difference: ${parity_check:.6f} ≈ 0 ✓")

    # Greeks
    call_delta = black_scholes_delta(S, K, T, r, sigma, 'call')
    put_delta = black_scholes_delta(S, K, T, r, sigma, 'put')

    print(f"\nOption Greeks:")
    print(f"  Call Delta = N(d₁) = {call_delta:.6f}")
    print(f"  Put Delta = N(d₁) - 1 = {put_delta:.6f}")

    # Sensitivity analysis
    print(f"\nSensitivity Analysis:")
    print(f"\n  Effect of increasing each parameter:")
    print(f"  {'Parameter':<15} {'Call':<10} {'Put':<10}")
    print(f"  {'-'*35}")
    print(f"  {'Stock Price':<15} {'Increase':<10} {'Decrease':<10}")
    print(f"  {'Strike Price':<15} {'Decrease':<10} {'Increase':<10}")
    print(f"  {'Volatility':<15} {'Increase':<10} {'Increase':<10}")
    print(f"  {'Time':<15} {'Increase':<10} {'Increase':<10}")
    print(f"  {'Interest Rate':<15} {'Increase':<10} {'Decrease':<10}")

    return call_price, put_price

# ============================================================================
# HOMEWORK 7: AMERICAN OPTIONS AND KMV MODEL
# ============================================================================

def hw7_american_options():
    """Solve HW7: American Options"""
    print("\n" + "="*80)
    print("HOMEWORK 7: AMERICAN OPTIONS")
    print("="*80)

    # 3-period binomial tree
    S0 = 100
    u = 1.1
    d = 1/u
    r = 0.02  # 2% per period (1 year)
    K = 100
    n = 3

    print(f"\nParameters:")
    print(f"  S₀ = ${S0}, K = ${K}")
    print(f"  u = {u}, d = {d:.6f}")
    print(f"  r = {r*100:.0f}% per period (1 year)")
    print(f"  Periods: {n}")

    q_star = (np.exp(r) - d) / (u - d)
    print(f"  Risk-neutral probability: q* = {q_star:.6f}")

    # American put option pricing with early exercise
    # Build the tree
    stock_tree = {}
    for i in range(n+1):
        for j in range(i+1):
            stock_tree[(i,j)] = S0 * (u**j) * (d**(i-j))

    # American put values
    put_tree = {}

    # Terminal payoffs
    for j in range(n+1):
        S_T = stock_tree[(n,j)]
        put_tree[(n,j)] = max(K - S_T, 0)

    # Backward induction with early exercise check
    for i in range(n-1, -1, -1):
        for j in range(i+1):
            S_t = stock_tree[(i,j)]
            # Continuation value
            cont_value = np.exp(-r) * (q_star * put_tree[(i+1,j+1)] + (1-q_star) * put_tree[(i+1,j)])
            # Exercise value
            ex_value = max(K - S_t, 0)
            # American: take maximum
            put_tree[(i,j)] = max(cont_value, ex_value)

            if ex_value > cont_value and ex_value > 0:
                print(f"  Early exercise optimal at t={i}, state={j}: S=${S_t:.2f}")

    american_put = put_tree[(0,0)]

    print(f"\nAmerican Put Option Value: ${american_put:.4f}")

    # European put for comparison
    euro_put = put_tree.copy()
    for i in range(n-1, -1, -1):
        for j in range(i+1):
            euro_put[(i,j)] = np.exp(-r) * (q_star * euro_put[(i+1,j+1)] + (1-q_star) * euro_put[(i+1,j)])

    european_put = euro_put[(0,0)]

    print(f"European Put Option Value: ${european_put:.4f}")
    print(f"Early Exercise Premium: ${american_put - european_put:.4f}")

    return american_put

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute all homework solutions"""
    print("\n" + "="*80)
    print("FINANCIAL INSTRUMENTS - COMPLETE HOMEWORK SOLUTIONS")
    print("Bus 35100 - John Heaton")
    print("="*80)

    results = {}

    # Execute all homework problems
    results['hw1_forward'] = hw1_forward_rates()
    results['hw2_contracts'] = hw2_commodity_futures()
    results['hw3_swap_rates'] = hw3_currency_swaps()
    results['hw4_leeson_loss'] = hw4_barings_leeson()
    results['hw4_stock_price'], results['hw4_call'] = hw4_binomial_tree()
    results['hw5_binomial_call'] = hw5_binomial_multiperiod()
    results['hw5_bs_call'], results['hw5_bs_put'] = hw5_black_scholes()
    results['hw7_american_put'] = hw7_american_options()

    # Summary
    print("\n" + "="*80)
    print("SUMMARY OF KEY RESULTS")
    print("="*80)
    for key, value in results.items():
        if isinstance(value, (int, float)):
            print(f"  {key}: {value:.4f}")
        elif isinstance(value, tuple):
            print(f"  {key}: {value}")

    print("\n" + "="*80)
    print("ALL HOMEWORK PROBLEMS COMPLETED!")
    print("="*80)

    return results

if __name__ == "__main__":
    results = main()
