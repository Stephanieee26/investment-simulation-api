from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel
import pandas as pd
import itertools
import yfinance as yf
from fastapi.responses import JSONResponse
import traceback

app = FastAPI(title="定期定額策略報酬率 API")

def load_price_data(symbol, start_date, end_date):
    df_raw = yf.download(symbol, start=start_date, end=end_date, group_by='ticker', auto_adjust=True)
    df_raw.columns = df_raw.columns.droplevel(0)
    df = df_raw.reset_index()
    df.columns = df.columns.str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.to_period('M')
    return df

def simulate_strategy(df, dates, monthly_investment=10000, split=False):
    monthly_groups = df.groupby('month')
    results = []
    for month, group in monthly_groups:
        invest_days = [group[group['day'] == d] for d in dates]
        invest_days = [g.iloc[0] for g in invest_days if not g.empty]
        if split and len(invest_days) == 2:
            shares = sum((monthly_investment / 2) / row['close'] for row in invest_days)
        elif not split and len(invest_days) == 1:
            shares = monthly_investment / invest_days[0]['close']
        else:
            continue
        results.append({
            'month': str(month),
            'shares': shares,
            'invested': monthly_investment
        })
    return pd.DataFrame(results)

def run_strategies(df, single_days, monthly_investment=10000):
    single_results = {}
    for d in single_days:
        res = simulate_strategy(df, [d], monthly_investment, split=False)
        single_results[f"{d:02d}日"] = res

    double_results = {}
    for combo in itertools.combinations(single_days, 2):
        name = f"{combo[0]:02d}+{combo[1]:02d}"
        res = simulate_strategy(df, list(combo), monthly_investment, split=True)
        double_results[name] = res

    return single_results, double_results

def summarize_results(results_dict, latest_price):
    summary = []
    for name, df_r in results_dict.items():
        total_invested = float(df_r['invested'].sum())
        total_shares = float(df_r['shares'].sum())
        value = total_shares * float(latest_price)
        return_rate = (value - total_invested) / total_invested
        summary.append({
            '策略': str(name),
            '總投入': round(total_invested, 2),
            '總持股': round(total_shares, 4),
            '期末市值': round(value, 2),
            '報酬率 (%)': round(return_rate * 100, 2)
        })
    return sorted(summary, key=lambda x: x['報酬率 (%)'], reverse=True)

@app.get("/simulate")
def simulate_etf(
    symbol: str = Query("0050.TW", description="股票或ETF代碼"),
    start_date: str = Query(..., description="起始日期，格式為 yyyy-mm-dd"),
    end_date: str = Query(..., description="結束日期，格式為 yyyy-mm-dd"),
    single_dates: List[int] = Query([1, 8, 15, 22, 28], description="每月定期定額的日期，1-31(可多選)"),
    monthly_investment: int = Query(10000, description="每月定期定額投資金額"),
):
    try:
        df = load_price_data(symbol, start_date, end_date)
        latest_price = df.iloc[-1]['close']
        single_results, double_results = run_strategies(df, single_dates, monthly_investment)
        single_summary = summarize_results(single_results, latest_price)
        double_summary = summarize_results(double_results, latest_price)
        return {
            "單日策略": single_summary,
            "雙日策略": double_summary
        }
    except Exception as e:
        traceback_str = traceback.format_exc()
        print("❌ 程式發生錯誤：", e)
        print(traceback_str)
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": traceback_str}
        )
