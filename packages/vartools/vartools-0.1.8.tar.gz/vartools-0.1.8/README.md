# VaR Calculation Library

## Overview
This Python library provides functions to calculate the **Value at Risk (VaR)** and **Conditional Value at Risk (cVaR)** for financial portfolios, including stock and forex portfolios. These risk measures help in understanding potential losses under given confidence levels. It also allows you to conveniently download price data from Yahoo Finance and perform portfolio optimization using multiple strategies.

## Features
- Download stock price data.
- Calculate **VaR** and **cVaR** for a **stock portfolio**.
- Calculate **VaR** and **cVaR** for a **forex portfolio**.
- Supports both **long** and **short** positions.
- Outputs results in both **percentage** and **cash value**.
- Rebalance a **stock portfolio**.
- Portfolio optimization for multiple strategies.

## Installation
Ensure you have the required dependencies installed:

```bash
pip install scipy
pip install numpy 
pip install pandas
pip install yfinance
pip install matplotlib
```

Then

```bash
pip install vartools
```
Also run

```bash
pip install --upgrade vartools
```

To get the latest version.

## Functions

### `get_data(stocks, start_date, end_date, type)`

#### Parameters
- **stocks** (*list*): List of stock tickers to download.
- **start_date** (*str*): Start date in the format `YYYY-MM-DD`.
- **end_date** (*str*): End date in the format `YYYY-MM-DD`.
- **type** (*str*): Type of price to retrieve (e.g., `"Adj Close"`, `"Close"`).

#### Returns
- **pd.DataFrame**: A DataFrame containing the selected price type for the specified stocks.

**Note:** If you prefer to directly download the data from yfinance it is encouraged a format like this:

```python
stocks = ["AAPL", "TSLA", "AMD", "LMT", "JPM"]
data=yf.download(stocks, start="2020-01-01", end="2023-01-01")['Close'][stocks]
```

Also if you get the data from an excel or csv file create the list `stocks` or `currencies`with the name of the columns in your file for correct functioning. Also make sure to establish yor `Date`column as index.

### `var_stocks(data, n_stocks, conf, long, stocks)`
Calculates the **VaR** and **cVaR** for a stock portfolio.

#### Parameters:
- `data` (*pd.DataFrame*): DataFrame containing stock prices.
- `stocks` (*list*): List of stock tickers.
- `n_stocks` (*list*): Number of stocks per ticker.
- `conf` (*float*): Confidence level (e.g., 95 for 95%).
- `long` (*bool*): `True` for long position, `False` for short position.

#### Returns:
A DataFrame with the following columns:
- **Métrica**: "VaR" and "cVaR".
- **Porcentaje**: The percentage value of risk.
- **Cash**: The risk in monetary terms.

**Note:** Utilize this function when you have the number of shares of each stock instead of the weights.


### `var_forex(data, positions, conf, long, currencies)`
Calculates the **VaR** and **cVaR** for a forex portfolio.

#### Parameters:
- `data` (*pd.DataFrame*): DataFrame containing forex currency pair prices.
- `currencies` (*list*): List of currency pairs.
- `positions` (*list*): Number of units per currency pair.
- `conf` (*float*): Confidence level (e.g., 95 for 95%).
- `long` (*bool*): `True` for long position, `False` for short position.

#### Returns:
A DataFrame with the following columns:
- **Métrica**: "VaR" and "cVaR".
- **Porcentual**: The percentage value of risk.
- **Cash**: The risk in monetary terms.


### `rebalance_stocks(w_original, target_weights, data, stocks, portfolio_value)`
Calculates the number of shres to buy/sell to rebalance a **stock portfolio**..

#### Parameters:
- **w_original**: `list` of floats representing the original weights of each asset in the portfolio.
- **target_weights**: `list` of floats representing the target weights of each asset in the portfolio.
- **data**: `pd.DataFrame` with historical stock prices, where columns represent different stocks.
- **stocks**: `list` of stock tickers (column names in the `data` DataFrame).
- **portfolio_value**: `float` representing the total value of the portfolio.

#### Returns:
- A `pd.DataFrame` showing the original weights, target weights, and the number of shares to buy or sell for each asset to rebalance the portfolio.


### `var_weights(data, weights, conf)`

#### Parameters
- **data** (*pd.DataFrame*): DataFrame containing historical stock prices.
- **weights** (*list or np.array*): Portfolio weights corresponding to each stock.
- **conf** (*float*): Confidence level (e.g., 95 for 95%).

#### Returns
- **var** (*float*): The Value at Risk (VaR) at the given confidence level.

**Note:** It only works for long positions, and the weights must add up to 1.


### `cvar_weights(data, weights, conf)`

#### Parameters
- **data** (*pd.DataFrame*): DataFrame containing historical stock prices.
- **weights** (*list or np.array*): Portfolio weights corresponding to each stock.
- **conf** (*float*): Confidence level (e.g., 95 for 95%).

#### Returns
- **cvar_pct** (*float*): The Conditional Value at Risk (CVaR), representing the expected loss beyond VaR.

**Note:** It only works for long positions, and the weights must add up to 1.



### `opt_sharpe(returns, rf)`

#### Parameters
- **returns** (*pd.DataFrame*): DataFrame containing the daily returns of the stock prices.
- **rf**: One-year risk-free rate

#### Returns
It returns a vector with the optimal weight for each stock.


### `min_variance(returns, rf)`

#### Parameters
- **returns** (*pd.DataFrame*): DataFrame containing the daily returns of the stock prices.

#### Returns
It returns a vector with the optimal weight for each stock.


### `min_cvar(returns, alpha)`

#### Parameters:
- returns (*pd.DataFrame*): DataFrame containing historical asset returns.
- alpha (float): Significance level for CVaR (example: 0.05 for 95% confidence level).

#### Returns:
It returns a vector with the optimal weight for each stock.

**Note:** It is required to write alpha in decimal notation, also this portfolio strategy only works for long positions.


### `mcc_portfolio(returns, alpha)`

#### Parameters:
- returns (*pd.DataFrame*): DataFrame containing historical asset returns.
- alpha (float): Significance level for CVaR (example: 0.05 for 95% confidence level).

#### Returns:
It returns a vector with the optimal weight for each stock.

**Note:** It is required to write alpha in decimal notation, also this portfolio strategy only works for long positions.


### `def cvar_contributions(weights, returns, alpha)`

#### Parameters:
- weights: An array with the weights for each asset in the portfolio.
- returns (*pd.DataFrame*): DataFrame containing historical asset returns.
- alpha (float): Significance level for CVaR (example: 0.05 for 95% confidence level).

#### Returns:
It returns an array with the individual contribution of each asset to the cvar of the portfolio.

**Note:** It is required to write alpha in decimal notation, also this portfolio strategy only works for long positions, so the weights must add up to 1.



### `plot_weights(df)`

#### Parameters
- df (*pd.DataFrame*): DataFrame with the weights for each stock.

#### Returns
It creates a pie chart with the weights of the portfolio.

**Note:** It works with the DataFrames generated by the optimization modules of the package.

### `BlackScholes`

#### Parameters:

- S: Current stock price
- k: Strike price
- r: Risk-free rate
- sigma: Volatility of the asset
- T: Time to expiration (in years)

#### Returns
The value of the delta of a call or put option.

**Note:** It also has function to determine how much of the underlying asset (in monetary unit) should be bought to delta hedge.

## Usage Example
```python
import numpy as np
import pandas as pd
import yfinance as yf
import vartools as vt
import matplotlib.pyplot as plt
from scipy.optimize import minimize
```

## get_data
```python
stocks = ["AAPL", "TSLA", "AMD", "LMT", "JPM"]
start_date = "2020-01-01"
end_date = "2023-01-01"
type = 'Close' # 'Close', select the type of price you want to download

data = vt.get_data(stocks, start_date, end_date, type)
```

## var_stocks
```python
stocks = ["AAPL", "TSLA", "AMD", "LMT", "JPM"]
start_date = "2020-01-01"
end_date = "2023-01-01"
type = 'Close' # 'Close', select the type of price you want to download

data = vt.get_data(stocks, start_date, end_date, type)
n_stocks =[2193, 1211, 3221, 761, 1231]
conf = 95
long = True

var_df = vt.var_stocks(data, n_stocks, conf, long, stocks)
```

## var_forex
```python
currencies = ['CHFMXN=X', 'MXN=X']
start_date = "2020-01-01"
end_date = "2024-12-02"
type = 'Close'

data = vt.get_data(currencies, start_date, end_date, type)
positions = [7100000, 5300000] # How much you have in each currency. Must match the order in currencies.
conf = 99 # Nivel de confianza
long = True

var_forex_df = vt.var_forex(data, positions, conf, long, currencies)
```

## rebalance_stocks
```python
stocks = ["AAPL", "TSLA", "AMD", "LMT", "JPM"]
start_date = "2020-01-01"
end_date = "2023-01-01"
type = 'Close' # 'Close', select the type of price you want to download

data = vt.get_data(stocks, start_date, end_date, type)

rt = data.pct_change().dropna()
stock_value = n_stocks * data.iloc[-1]
portfolio_value = stock_value.sum()
w_original = stock_value / portfolio_value
w_opt = [0.33, 0.15, 0.06, 0.46, 0.00]

rebalance_df = vt.rebalance_stocks(w_original, w_opt, data, stocks, portfolio_value)
```

## var_weights
```python
stocks = ["AAPL", "TSLA", "AMD", "LMT", "JPM"]
start_date = "2020-01-01"
end_date = "2023-01-01"
type = 'Close' # 'Close', select the type of price you want to download

data = vt.get_data(stocks, start_date, end_date, type)

weights = [0.2457, 0.1301, 0.1820, 0.3064, 0.1358]
conf = 95
var_pct = vt.var_weights(data, weights, conf)
```

## cvar_weights
```python
stocks = ["AAPL", "TSLA", "AMD", "LMT", "JPM"]
start_date = "2020-01-01"
end_date = "2023-01-01"
type = 'Close' # 'Close', select the type of price you want to download

data = vt.get_data(stocks, start_date, end_date, type)

weights = [0.2457, 0.1301, 0.1820, 0.3064, 0.1358]
conf = 95
cvar_pct = vt.cvar_weights(data, weights, conf)
```

## opt_sharpe
```python
stocks=['WMT','AAPL','GOOGL','PG','XOM','KO','CMG','F']
start_date='2020-01-01'
end_date='2024-11-24'
type='Close'

data = vt.get_data(stocks, start_date, end_date, type)
returns = data.pct_change().dropna()
rf = 0.04413

opt_sharpe_weights = vt.opt_sharpe(returns, rf)
```

## min_variance
```python
stocks=['WMT','AAPL','GOOGL','PG','XOM','KO','CMG','F']
start_date='2020-01-01'
end_date='2024-11-24'
type='Close'

data = vt.get_data(stocks, start_date, end_date, type)
returns = data.pct_change().dropna()

min_var_weights = vt.min_variance(returns)
```


## min_cvar
```python
# bonds, commodities, equities and real estate
stocks = ['VBTLX', 'GSG', 'VTI', 'VNQ']
start_date = '2019-01-01'
end_date = '2024-01-01'
type = 'Close'

data = vt.get_data(stocks, start_date, end_date, type)
returns = data.pct_change().dropna()
alpha = 0.05

min_cvar = vt.min_cvar(returns, alpha)
```


## mcc_portfolio
```python
# bonds, commodities, equities and real estate
stocks = ['VBTLX', 'GSG', 'VTI', 'VNQ']
start_date = '2019-01-01'
end_date = '2024-01-01'
type = 'Close'

data = vt.get_data(stocks, start_date, end_date, type)
returns = data.pct_change().dropna()
alpha = 0.05

mcc_weights = vt.mcc_portfolio(returns, alpha)
```

## cvar_contributions
```python
# bonds, commodities, equities and real estate
stocks = ['VBTLX', 'GSG', 'VTI', 'VNQ']
start_date = '2019-01-01'
end_date = '2024-01-01'
type = 'Close'

data = vt.get_data(stocks, start_date, end_date, type)
returns = data.pct_change().dropna()
alpha = 0.05

mcc_weights = vt.mcc_portfolio(returns, alpha)

cvar_contributions = vt.cvar_contributions(mcc_weights, returns, alpha)
```


## plot_weights
```python
stocks=['WMT','AAPL','GOOGL','PG','XOM','KO','CMG','F']
start_date='2020-01-01'
end_date='2024-11-24'
type='Close'

data = vt.get_data(stocks, start_date, end_date, type)
returns = data.pct_change().dropna()
rf = 0.04413

opt_sharpe = vt.opt_sharpe(returns, rf)

vt.plot_weights(stocks, opt_sharpe)
```


## call_delta and put_delta
```python
S_call = 20.3
K_call = 20.43
r_call = 0.0425
sigma_call = 0.102
T_call = 1/12

S_put = 20.3
K_put = 20.2
r_put = 0.0425
sigma_put = 0.156
T_put = 1/12

delta_call = vt.BlackScholes().call_delta(S_call, K_call, r_call, sigma_call, T_call)
delta_put = vt.BlackScholes().put_delta(S_put, K_put, r_put, sigma_put, T_put)

delta_call, delta_put
```

```python
# Write in order S, K, r, sigma, T

call = [20.3, 20.43, 0.0425, 0.102, 1/12]
put = [20.3, 20.2, 0.0425, 0.156, 1/12]

delta_call = vt.BlackScholes().call_delta(*call)
delta_put = vt.BlackScholes().put_delta(*put)

delta_call, delta_put
```


## delta_hedge
```python
# Write in order S, K, r, sigma, T, N (money invested in each option)

info_call = [[20.3, 20.43, 0.0425, 0.102, 1/12, 23],
            [20.3, 20.52, 0.0425, 0.111, 1/12, 25],
            [20.3, 20.43, 0.0421, 0.297, 6/12, 17],
            [20.3, 20.52, 0.0421, 0.289, 6/12, 32]]

info_put = [[20.3, 20.2, 0.0425, 0.156, 1/12, 12],
            [20.3, 20, 0.0425, 0.153, 1/12, 16],
            [20.3, 20.2, 0.0421, 0.348, 6/12, 11],
            [20.3, 20, 0.0421, 0.378, 6/12, 17]]

# If N is in millions of dollar, then
hedge = vt.BlackScholes().delta_hedge(info_call, info_put)
print(f'Buy {hedge} millions of dollars of the underlying asset')
```


## License
This project is licensed under the GPL-3.0 license.

## Author
Luis Fernando Márquez Bañuelos
