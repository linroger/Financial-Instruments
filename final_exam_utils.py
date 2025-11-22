import math
from dataclasses import dataclass
from typing import List, Tuple

from scipy.stats import norm


def forward_rate(spot: float, rd: float, rf: float, maturity: float) -> float:
    """Compute forward FX rate using continuous compounding."""
    return spot * math.exp((rd - rf) * maturity)


def currency_swap_fixed_rate(spot: float, rd: float, rf: float, cashflows: List[float], times: List[float]) -> float:
    """Fair dollar-per-euro rate to exchange euro cash flows for dollars."""
    discounts = [math.exp(-rd * t) for t in times]
    forwards = [forward_rate(spot, rd, rf, t) for t in times]
    numerator = sum(c * f * d for c, f, d in zip(cashflows, forwards, discounts))
    denominator = sum(c * d for c, d in zip(cashflows, discounts))
    return numerator / denominator


def currency_swap_value(cashflows: List[float], times: List[float], rd: float, receive_rate: float, new_forward: float) -> float:
    """Value (USD) of paying fixed dollars at receive_rate vs receiving euros converted at new_forward."""
    return sum(cf * (new_forward - receive_rate) * math.exp(-rd * t) for cf, t in zip(cashflows, times))


@dataclass
class MertonResult:
    equity_value: float
    share_price: float
    equity_vol: float
    debt_value: float
    debt_yield: float
    default_prob: float


def merton_model(asset_value: float, debt_face: float, asset_vol: float, r: float, maturity: float, shares_outstanding: float) -> MertonResult:
    sigma_a = asset_vol
    A = asset_value
    D = debt_face
    T = maturity
    d1 = (math.log(A / D) + (r + 0.5 * sigma_a ** 2) * T) / (sigma_a * math.sqrt(T))
    d2 = d1 - sigma_a * math.sqrt(T)
    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)

    equity_value = A * N_d1 - D * math.exp(-r * T) * N_d2
    share_price = equity_value / shares_outstanding
    equity_vol = (A / equity_value) * N_d1 * sigma_a
    debt_value = A - equity_value
    debt_yield = -math.log(debt_value / D) / T
    default_prob = norm.cdf(-d2)
    return MertonResult(
        equity_value=equity_value,
        share_price=share_price,
        equity_vol=equity_vol,
        debt_value=debt_value,
        debt_yield=debt_yield,
        default_prob=default_prob,
    )


def senior_subordinated_values(asset_value: float, senior_face: float, sub_face: float, asset_vol: float, r: float, maturity: float) -> Tuple[float, float]:
    """Value senior and subordinated zero-coupon debt using Black-Scholes style formulas."""
    sigma_a = asset_vol
    T = maturity
    d1_s = (math.log(asset_value / senior_face) + (r + 0.5 * sigma_a ** 2) * T) / (sigma_a * math.sqrt(T))
    d2_s = d1_s - sigma_a * math.sqrt(T)
    put_senior = asset_value * norm.cdf(-d1_s) - senior_face * math.exp(-r * T) * norm.cdf(-d2_s)
    senior_value = senior_face * math.exp(-r * T) - put_senior

    total_face = senior_face + sub_face
    d1_total = (math.log(asset_value / total_face) + (r + 0.5 * sigma_a ** 2) * T) / (sigma_a * math.sqrt(T))
    d2_total = d1_total - sigma_a * math.sqrt(T)
    call_at_senior = asset_value * norm.cdf(d1_s) - senior_face * math.exp(-r * T) * norm.cdf(d2_s)
    call_at_total = asset_value * norm.cdf(d1_total) - total_face * math.exp(-r * T) * norm.cdf(d2_total)
    subordinate_value = call_at_senior - call_at_total
    return senior_value, subordinate_value


def binomial_parameters(u: float, d: float, r: float, dt: float = 1.0) -> float:
    return (math.exp(r * dt) - d) / (u - d)


def european_call_binomial(S0: float, K: float, r: float, u: float, d: float, steps: int) -> float:
    dt = 1.0
    p = binomial_parameters(u, d, r, dt)
    discount = math.exp(-r * dt)
    prices = [S0 * (u ** j) * (d ** (steps - j)) for j in range(steps + 1)]
    payoffs = [max(s - K, 0.0) for s in prices]
    for _ in range(steps):
        payoffs = [discount * (p * payoffs[i + 1] + (1 - p) * payoffs[i]) for i in range(len(payoffs) - 1)]
    return payoffs[0]


def american_call_with_dividend(
    S0: float,
    K: float,
    r: float,
    u: float,
    d: float,
    steps: int,
    dividend_time: int,
    dividend_amount: float,
    threshold: float,
) -> Tuple[float, List[List[float]]]:
    """Price American call with conditional cash dividend using a non-recombining tree."""
    p = binomial_parameters(u, d, r)
    discount = math.exp(-r)

    prices: List[List[float]] = [[S0]]
    for step in range(1, steps + 1):
        prev = prices[-1]
        level: List[float] = []
        for price in prev:
            down = price * d
            up = price * u
            level.extend([down, up])
        if step == dividend_time:
            level = [price - dividend_amount if price >= threshold else price for price in level]
        prices.append(level)

    option_values = [max(price - K, 0.0) for price in prices[-1]]

    for step in range(steps, 0, -1):
        prev_prices = prices[step - 1]
        new_values: List[float] = []
        for i, price in enumerate(prev_prices):
            down_val = option_values[2 * i]
            up_val = option_values[2 * i + 1]
            continuation = discount * ((1 - p) * down_val + p * up_val)
            intrinsic = max(price - K, 0.0)
            new_values.append(max(intrinsic, continuation))
        option_values = new_values
    return option_values[0], prices


def structured_product_price(S0: float, r: float, T: float, put1: float, put2: float, K1: float, K2: float) -> Tuple[float, float, float]:
    """Price structured product using put prices and call-put parity."""
    disc = math.exp(-r * T)
    call1 = put1 + S0 - K1 * disc
    call2 = put2 + S0 - K2 * disc
    price = disc * 1000 + 2 * call1 - 2 * call2
    return price, call1, call2


def structured_product_delta_beta(S: float, r: float, sigma: float, T: float, K1: float, K2: float) -> Tuple[float, float]:
    """Compute delta and approximate beta-like measure for structured product."""
    from math import log, sqrt

    def call_delta(K: float) -> float:
        d1 = (log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
        return norm.cdf(d1)

    price, _, _ = structured_product_price(S, r, T, 0, 0, K1, K2)
    call1_delta = call_delta(K1)
    call2_delta = call_delta(K2)
    product_delta = 2 * call1_delta - 2 * call2_delta
    beta = product_delta * S / price if price else float('nan')
    return product_delta, beta
