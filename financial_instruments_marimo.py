import marimo
import pandas as pd
import numpy as np
import math
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go


app = marimo.App()


def libor_simple_to_continuous(rate_percent, tenor_years):
    rate = rate_percent / 100.0
    return math.log(1 + rate * tenor_years) / tenor_years


def forward_fx(spot, r_dom_cc, r_for_cc, tenor_years):
    return spot * math.exp((r_dom_cc - r_for_cc) * tenor_years)


@app.cell
def __():
    intro = "Financial Instruments solutions rendered with marimo."
    return intro


@app.cell
def __():
    spot = 1.20
    r_us_cc = 0.05
    r_eu_cc = 0.045
    f_theoretical = forward_fx(spot, r_us_cc, r_eu_cc, 1)
    k_market = 1.15
    arbitrage = "Forward underpriced" if k_market < f_theoretical else "Forward overpriced"
    return f_theoretical, k_market, arbitrage


@app.cell
def __(Path=Path, libor_simple_to_continuous=libor_simple_to_continuous, forward_fx=forward_fx, pd=pd, px=px):
    hw1_path = Path('Assignments/Assignment 1/DataHW1.xls')
    raw = pd.read_excel(hw1_path, sheet_name='FX_Forwards_and_Rates', header=0)
    clean = raw.iloc[1:].copy()
    clean.columns = ['Date','Spot','Fwd1M','Fwd3M','Fwd6M','Fwd1Y','US1M','US3M','US6M','US1Y','EU1M','EU3M','EU6M','EU1Y']
    clean['Date'] = pd.to_datetime(clean['Date'], errors='coerce')
    clean = clean.dropna(subset=['Date'])
    maturities = {'Fwd1M':1/12,'Fwd3M':3/12,'Fwd6M':6/12,'Fwd1Y':1}
    rows = []
    for _, row in clean.iterrows():
        for col, tenor in maturities.items():
            r_us = libor_simple_to_continuous(row[f'US{int(tenor*12)}M' if tenor<1 else 'US1Y'], tenor)
            r_eu = libor_simple_to_continuous(row[f'EU{int(tenor*12)}M' if tenor<1 else 'EU1Y'], tenor)
            rows.append({
                'Date': row['Date'],
                'Tenor': col,
                'Theoretical': forward_fx(row['Spot'], r_us, r_eu, tenor),
                'Quoted': row[col]
            })
    df = pd.DataFrame(rows)
    fig = px.bar(df, x='Tenor', y=df['Quoted']-df['Theoretical'], color=df['Date'].dt.year.astype(str), title='Forward deviations')
    return df, fig


@app.cell
def __(Path=Path, libor_simple_to_continuous=libor_simple_to_continuous, forward_fx=forward_fx, pd=pd, px=px):
    hw2_path = Path('Assignments/Assignment 2/DataHW2_2024.xls')
    arb = pd.read_excel(hw2_path, sheet_name='ForwardArbitrage', header=2)
    arb.columns = ['Date','MaturityYears','Spot','Fwd1M','Fwd3M','Fwd6M','Fwd1Y','US1M','US3M','US6M','US1Y','EU1M','EU3M','EU6M','EU1Y']
    arb['Date'] = pd.to_datetime(arb['Date'], errors='coerce')
    arb = arb.dropna(subset=['Date'])
    init = arb.iloc[0]
    after = arb.iloc[1]
    k_forward = init['Fwd1Y']
    fair = forward_fx(init['Spot'], libor_simple_to_continuous(init['US1Y'],1), libor_simple_to_continuous(init['EU1Y'],1), 1)
    t_remain = after['MaturityYears']
    fair_t = forward_fx(after['Spot'], libor_simple_to_continuous(after['US6M'],t_remain), libor_simple_to_continuous(after['EU6M'],t_remain), t_remain)
    value_short = (k_forward - fair_t) * math.exp(-libor_simple_to_continuous(after['US6M'],t_remain)*t_remain)
    return arb, value_short


@app.cell
def __(pd=pd, Path=Path, px=px):
    hw2_path = Path('Assignments/Assignment 2/DataHW2_2024.xls')
    raw_prices = pd.read_excel(hw2_path, sheet_name='Light Crude fut. prices', header=None)
    header_row = 3
    cols = raw_prices.iloc[header_row].tolist()
    data = raw_prices.iloc[header_row+1:, :len(cols)].copy()
    data.columns = cols
    data = data.dropna(subset=['Day']).copy()
    data['Day'] = pd.to_datetime(data['Day'], errors='coerce')
    fig = px.line(data, x='Day', y=['FEB. 08','MAR. 08','APR. 08','Fuel price per gallon'], title='Futures and jet fuel')
    return data, fig


@app.cell
def __(pd=pd, Path=Path, libor_simple_to_continuous=libor_simple_to_continuous, forward_fx=forward_fx):
    zcb = pd.read_excel('Assignments/Assignment 3/Greece_GS_table1.xls', sheet_name='Sheet1', header=None, names=['blank','T','ZEU','ZUS']).dropna(subset=['T'])
    freq=2
    times=[i/freq for i in range(1,20)]
    zeu=dict(zip(zcb['T'], zcb['ZEU']))
    zus=dict(zip(zcb['T'], zcb['ZUS']))
    pv_eur=sum(zeu[t] for t in times if t in zeu)
    pv_us=sum(0.06/freq*50*zus[t]*0.8475 for t in times if t in zus)+50*0.8475*zus[10]
    rate=pv_us/(59*pv_eur)*freq
    return rate


@app.cell
def __(np=np, go=go):
    k=19750
    premium=9.9+9.8
    contract=10000
    prices=np.linspace(12000,26000,40)
    profit=[(-max(s-k,0)-max(k-s,0)+premium)*contract for s in prices]
    fig=go.Figure(go.Scatter(x=prices,y=profit))
    fig.update_layout(title='Short straddle P&L',xaxis_title='Nikkei',yaxis_title='JPY')
    return fig


@app.cell
def __(math=math):
    S_u=21;S_d=10;q=0.7;beta=2;r_cc=0.05;rp=0.0644
    r_disc=math.exp(r_cc)-1
    S0=(q*S_u+(1-q)*S_d)/(1+ r_disc+beta*rp)
    u=S_u/S0;d=S_d/S0
    p_star=(math.exp(r_cc)-d)/(u-d)
    call=math.exp(-r_cc)*(p_star*max(S_u-S0,0)+(1-p_star)*max(S_d-S0,0))
    return S0, call


@app.cell
def __():
    notional=10; leverage=3; cap=11.9; s0=1329.51
    return notional, leverage, cap, s0


if __name__ == "__main__":
    app.run()
