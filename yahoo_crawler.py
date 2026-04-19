#!/usr/bin/env python3
"""
Yahoo Finance Configurable Data Crawler
Author: Grok (for you)
Last updated: 2026
"""

import argparse
import json
from pathlib import Path
from typing import Union, Dict, Any

import pandas as pd
import yfinance as yf


def make_serializable(obj: Any) -> Any:
    """Convert pandas objects to JSON-serializable dicts."""
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="records")
    if isinstance(obj, pd.Series):
        return obj.to_dict()
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    return obj


def fetch_data(args) -> Union[pd.DataFrame, Dict]:
    tickers = [t.strip().upper() for t in args.tickers.split(",")]

    if args.data_type == "history":
        kwargs = {
            "period": args.period,
            "interval": args.interval,
        }
        if args.start:
            kwargs["start"] = args.start
        if args.end:
            kwargs["end"] = args.end

        data: pd.DataFrame = yf.download(tickers, **kwargs, auto_adjust=False, progress=False)

        # Filter specific columns if requested
        if args.fields:
            field_list = [f.strip() for f in args.fields.split(",")]
            if isinstance(data.columns, pd.MultiIndex):
                # Multiple tickers -> MultiIndex columns
                data = data.loc[:, data.columns.get_level_values(0).isin(field_list)]
            else:
                # Single ticker -> flat columns
                data = data[[col for col in field_list if col in data.columns]]

        return data

    # All other data types use individual Ticker objects
    results: Dict = {}
    for ticker_symbol in tickers:
        ticker = yf.Ticker(ticker_symbol)

        if args.data_type == "info":
            info = ticker.info
            if args.fields:
                field_list = [f.strip() for f in args.fields.split(",")]
                results[ticker_symbol] = {k: info.get(k) for k in field_list}
            else:
                results[ticker_symbol] = info

        elif args.data_type == "financials":
            results[ticker_symbol] = ticker.financials
        elif args.data_type == "balance-sheet":
            results[ticker_symbol] = ticker.balance_sheet
        elif args.data_type == "cashflow":
            results[ticker_symbol] = ticker.cashflow
        elif args.data_type == "earnings":
            results[ticker_symbol] = ticker.earnings
        elif args.data_type == "holders":
            results[ticker_symbol] = {
                "institutional": ticker.institutional_holders,
                "major": ticker.major_holders,
            }
        elif args.data_type == "actions":
            results[ticker_symbol] = ticker.actions

    return results


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Configurable Yahoo Finance data crawler",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--tickers", required=True,
                        help="Comma-separated tickers (e.g. AAPL,GOOGL,MSFT,VNM.VN,^VNINDEX)")
    parser.add_argument("--data-type", default="history",
                        choices=["history", "info", "financials", "balance-sheet", "cashflow", "earnings", "holders", "actions"],
                        help="What kind of data you want")
    # History-specific options
    parser.add_argument("--period", default="1y",
                        help="History period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    parser.add_argument("--interval", default="1d",
                        help="Data interval: 1m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo")
    # Field filtering
    parser.add_argument("--fields",
                        help="Comma-separated fields (works for info & history columns). "
                             "Example for info: currentPrice,marketCap,dividendYield,forwardPE")
    # Output
    parser.add_argument("--output", "-o",
                        help="Output file path (e.g. stock_data.csv or data.json)")
    parser.add_argument("--format", default="csv", choices=["csv", "json"],
                        help="Output format when --output is used")

    args = parser.parse_args()

    print(f"🔄 Fetching {args.data_type} data for {args.tickers}...")

    data = fetch_data(args)

    if isinstance(data, pd.DataFrame) and data.empty:
        print("⚠️  No data returned. Check ticker symbols or dates.")
        return

    # === OUTPUT HANDLING ===
    if args.output:
        p = Path(args.output)
        p.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, pd.DataFrame):
            if args.format == "csv":
                data.to_csv(p, index=True)
            else:
                data.to_json(p, orient="records", date_format="iso")
        else:
            # dict of DataFrames / info
            serializable = make_serializable(data)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2, default=str)

        print(f"✅ Saved to → {p.resolve()}")
    else:
        # Console output
        if isinstance(data, pd.DataFrame):
            print(data)
        else:
            print(json.dumps(make_serializable(data), indent=2, default=str))

    print("\n🎉 Done! Run again with different --tickers / --data-type / --fields to crawl whatever you need.")


if __name__ == "__main__":
    main()