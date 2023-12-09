import alpaca_trade_api as tradeapi
import os
from env import API_KEY, API_SECRET
import time
from sklearn.linear_model import LinearRegression
import pandas as pd

# Set API information in separate env.py file
api_key = API_KEY
api_secret = API_SECRET
base_url = 'https://paper-api.alpaca.markets'  # Use paper trading base URL for testing

# Initialize Alpaca API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Set following info for target asset, timeframe and budget
symbol = 'ETH/USD'  # Replace with your desired asset symbol
timeframe = '1Min'  # Desired timeframe
budget = 1000.00 # Set your budget

# Initialize global variables
portfolio_val = budget
i = 1
quantity_in_portfolio = 0

while True:
  try:
    print(f'iteration {i}')

    # Initialize Machine learning dataframe
    crypto_data = api.get_crypto_bars([symbol], timeframe).df
    crypto_data = crypto_data.tail(100)
    ml_df = crypto_data.copy()

    ml_df.drop(['volume', 'vwap', 'symbol'], axis=1, inplace=True)

    ml_df['next_output'] = ml_df['close'].shift(-1)
    ml_df.dropna(inplace=True)

    # print(ml_df)

    # Initialize ML model
    train_size = 0.8  # 80% of the data for training, 20% for testing
    split_index = int(len(ml_df) * train_size)

    train_data = ml_df.iloc[:split_index]
    test_data = ml_df.iloc[split_index:]

    # Define your features (X) and target variable (y) for training and testing
    X_train = train_data[['close', 'high', 'low', 'open']]
    y_train = train_data['next_output']

    # Create and fit a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train) 

    coefficient = model.coef_  # This gives you the slope (m)
    intercept = model.intercept_  # This gives you the intercept (b)
    # Create a string representation of the linear regression equation
    regression_equation = f'y = {coefficient[0]:.4f} * close + {coefficient[1]:.4f} * high + {coefficient[2]:.4f} * low + {coefficient[3]:.4f} * open + {intercept:.4f}'

    print("Linear Regression Equation:")
    print(regression_equation)

    # Save data in .csv file
    output_directory = 'project3/data'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Path to save the CSV file inside the project3 directory
    file_name = symbol.replace('/', '_') + '.csv'
    output_file_path = os.path.join(output_directory, file_name)

    # Save DataFrame to CSV file
    crypto_data.to_csv(output_file_path, index=True)

    close = crypto_data.iloc[-1]['close']
    high = crypto_data.iloc[-1]['high']
    low = crypto_data.iloc[-1]['low']
    open = crypto_data.iloc[-1]['open']
    
    price = close
    if quantity_in_portfolio != 0:
      portfolio_val = price * quantity_in_portfolio

    input_features = pd.DataFrame({
      'close': [close],
      'high': [high],
      'low': [low],
      'open': [open]
    })

    # Predict next price using the model and the DataFrame with feature names
    predicted_next_price = model.predict(input_features)[0]
    print(f'current price: {price}')
    print(f'next price: {predicted_next_price}')

    # Purchase if empty portfolio and price predicted to increase
    if quantity_in_portfolio == 0 and predicted_next_price > price:
      print('purchase')
      api.submit_order(
        symbol=symbol,
        qty=portfolio_val/price,
        side='buy',
        type='limit',
        time_in_force='gtc',
        limit_price=price,
      )
      quantity_in_portfolio = portfolio_val/price
    # Sell if portfolio not empty and price predicted to decrease
    elif quantity_in_portfolio != 0 and predicted_next_price < price:
      print('sell')
      api.submit_order(
        symbol=symbol,
        qty=quantity_in_portfolio,
        side='sell',
        type='limit',
        time_in_force='gtc',
        limit_price=price,
      )
      quantity_in_portfolio = 0
    else:
      print('no change to portfolio')
    print(f'Portfolio worth {round(portfolio_val,2)}')

    # print(crypto_data)
    i += 1

    time.sleep(60)
  except Exception as e:
    print(f"An error occurred: {e}")

