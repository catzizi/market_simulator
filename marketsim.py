"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import os

from util import get_data, plot_data
from portfolio.analysis import get_portfolio_value, get_portfolio_stats, plot_normalized_data

def compute_portvals(start_date, end_date, orders_file, start_val):
    """Compute daily portfolio value given a sequence of orders in a CSV file.

    Parameters
    ----------
        start_date: first date to track
        end_date: last date to track
        orders_file: CSV file to read orders from
        start_val: total starting cash available

    Returns
    -------
        portvals: portfolio value for each trading day from start_date to end_date (inclusive)
    """
    # TODO: Your code here
    orders = pd.read_csv(orders_file, parse_dates=True, sep=',', dayfirst=True) #initiate orders data frame
    symbol_list = orders['Symbol'].tolist() #creates list of symbols
    symbols = list(set(symbol_list)) #gets rid of duplicates in list


    orders['SharesChange'] = orders.Shares * orders.Order.apply(lambda o: 1 if o == 'BUY' else -1) #lambda if/else changing share values positive or negative according to buy or sell respectively
    orders = orders.groupby(['Date', 'Symbol']).agg({'SharesChange' : np.sum}).unstack().fillna(0.00) #restack data according to symbols to match up with prices data frame
    orders['Date']=orders.index


    dates_list = orders['Date'].tolist() #creates list of order dates
    dates_orders = list(set(dates_list)) #gets rid of duplicates in list


    dates = pd.date_range(start_date, end_date) #establish dates from start_date and end_date
    prices_all = get_data(symbols, dates)
    prices = prices_all[symbols] #generate data frame for prices for each symbol

    prices['Cash'] = 1.00 #adds columns for later calculation



    trade = pd.DataFrame(0.00, index = prices.index, columns = symbols) #establish trade data frame filled with zeroes
    trade['Cash'] = 0.00 #add column Cash

    days=len(dates)

    num_orders=len(dates_list)


    prices.index =prices.index.map(lambda t: t.strftime('%Y-%m-%d')) #correct datetime data into correct format for comparison with datetime date from orders data frame

    for i in range(0, len(prices.index)):
          
        for j in range(0, num_orders):
            if prices.index[i] == orders.index[j]:
                for p in range(0, len(symbols)): #step through orders data frame to update trade data frame unders symbols
                    trade[symbols[p]][i] = orders['SharesChange', symbols[p]][j]
                for h in range(0, len(symbols)): #update Cash column to be the sum of cash spent for trades bought on that day
                    trade['Cash'][i] = trade['Cash'][i] - prices[symbols[h]][i] * trade[symbols[h]][i]


    holdings = pd.DataFrame(0.00, index = prices.index, columns = symbols) #establish holdings data frame
    holdings['Cash'] = 0.00
    holdings['Cash'][0] = start_val + trade['Cash'][0]


    for r in range(0, len(prices.index)): #value of next day is value of previous day plus value from row in trade data frame
        for k in range(0, len(symbols)):
            holdings[symbols[k]][r] = holdings[symbols[k]][r-1] + trade[symbols[k]][r]
    for y in range(1, len(prices.index)):
        holdings['Cash'][y] = holdings['Cash'][y-1] + trade['Cash'][y]
           
    value = prices * holdings #establishing the value data frame, which is the product of the prices and holdings data frames

    portvals = value.sum(axis=1) #calculating the portfolio value, which is the some of each row of the value data frame
    print portvals

    return portvals


def test_run():
    """Driver function."""
    # Define input parameters
    start_date = '2011-01-05'
    end_date = '2011-01-20'
    orders_file = os.path.join("orders", "orders-short.csv")
    start_val = 1000000

    # Process orders
    portvals = compute_portvals(start_date, end_date, orders_file, start_val)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # if a DataFrame is returned select the first column to get a Series
    
    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)

    # Simulate a $SPX-only reference portfolio to get stats
    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['$SPX']]  # remove SPY
    portvals_SPX = get_portfolio_value(prices_SPX, [1.0])
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = get_portfolio_stats(portvals_SPX)

    # Compare portfolio against $SPX
    print "Data Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX: {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX: {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    # Plot computed daily portfolio value
    df_temp = pd.concat([portvals, prices_SPX['$SPX']], keys=['Portfolio', '$SPX'], axis=1)
    plot_normalized_data(df_temp, title="Daily portfolio value and $SPX")


if __name__ == "__main__":
    test_run()