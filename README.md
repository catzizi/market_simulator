# market_simulator
a market simulator that accepts trading orders and keeps track of a portfolio's value over time and then assesses the performance of that portfolio.
To execute, run python -m marketsim

Basic simulator
 implement a function, my market simulator, compute_portvals() that returns a dataframe with one column.
 
 The files containing orders are CSV files with the following columns:

Date (yyyy-mm-dd)
Symbol (e.g. AAPL, GOOG)
Order (BUY or SELL)
Shares (no. of shares to trade)
For example:

Date,Symbol,Order,Shares
2008-12-3,AAPL,BUY,130
2008-12-8,AAPL,SELL,130
2008-12-5,IBM,BUY,50

Total value of the portfolio for each day using adjusted closing prices. 
The value for each day is cash plus the current value of equities.
helper function to call compute_portvals()
have the factors as followed:

Plot the price history over the trading period.
Sharpe ratio (Always assume you have 252 trading days in an year. And risk free rate = 0) of the total portfolio
Cumulative return of the total portfolio
Standard deviation of daily returns of the total portfolio
Average daily return of the total portfolio
Ending value of the portfolio
