# yahoo_finance_crawl

525102290496 - Nguyen Cong Thanh
# Get Help
python yahoo_crawler.py --help

# Example 1: Get stock price history (last 1 year)
python yahoo_crawler.py --tickers AAPL,MSFT,GOOGL,VNM.VN --period 1y

# Example 2: Save data to CSV file
python yahoo_crawler.py --tickers VCB.VN,HPG.VN,AAPL --period 6mo --output stock_prices.csv

# Example 3: Get current company information
python yahoo_crawler.py --tickers AAPL,TSLA,VNM.VN --data-type info --fields currentPrice,marketCap,forwardPE,dividendYield --output info.json --format json

Purpose,Command
Daily prices for last 1 year,"python yahoo_crawler.py --tickers AAPL,MSFT,VNM.VN --period 1y"
Daily prices for last 6 months,"python yahoo_crawler.py --tickers VCB.VN,HPG.VN --period 6mo"
Daily prices for last 3 months,python yahoo_crawler.py --tickers AAPL --period 3mo
Custom date range,python yahoo_crawler.py --tickers VNM.VN --start 2025-01-01 --end 2026-04-19
Only specific columns (Close & Volume),"python yahoo_crawler.py --tickers AAPL --fields Close,Volume"
Get current price & key info,"python yahoo_crawler.py --tickers AAPL,TSLA --data-type info"
Get selected fields only,"python yahoo_crawler.py --tickers VCB.VN --data-type info --fields currentPrice,marketCap,forwardPE,dividendYield"
Save output as CSV,... --output stock_data.csv
Save output as JSON,... --output data.json --format json
