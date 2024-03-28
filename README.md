# Documentation

## Introduction:

The purpose of this trading system is to algorithmically trade crypto currencies through alpaca. I have implemented machine learning to predict whether a currency will go up or down in the future, and buy or sell accordingly. 

## Market Data Retrieval:

To retrieve market data from Alpaca using the alpaca-py library, I have used the `get_crypto_bars`` API. In this implementation, we retrieve information such as the high, low, open and close of the crypto currency of choice over the last 100 minutes. Below is the code to get the market data:

```
# Set API information in separate env.py file
api_key = API_KEY
api_secret = API_SECRET
base_url = 'https://paper-api.alpaca.markets'  # Use paper trading base URL for testing


# Initialize Alpaca API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')


# Set following info for target asset, timeframe and budget
symbol = 'ETH/USD'  # Replace with your desired asset symbol
timeframe = '1Min'  # Desired timeframe
crypto_data = api.get_crypto_bars([symbol], timeframe).df
crypto_data = crypto_data.tail(100)
```

## Data Storage Strategy:

The data storage strategy I chose is a file system. Within my project3 directory (the directory in which main and env.py live), we automatically create a directory called `data` if it does not exist. This is the directory which holds all the data for all the crypto currencies. Within that directory, we will create a file called `[asset].csv` filled with all the data in our dataframe, including timestamps. Now we have saved a copy of all the data for all the different assets we choose to trade.

```
  # Save data in .csv file
  output_directory = 'project3/data'
  if not os.path.exists(output_directory):
      os.makedirs(output_directory)


  # Path to save the CSV file inside the project3 directory
  file_name = symbol.replace('/', '_') + '.csv'
  output_file_path = os.path.join(output_directory, file_name)


  # Save DataFrame to CSV file
  crypto_data.to_csv(output_file_path, index=True)
```

## Trading Strategy Development:.

I have opted to trade crypto currencies due to the fact that they may be traded 24/7 and there are no time constraints or market hours. This allows us to take the most recent 100 minutes worth of data and make trades at any given time. Using these 100 data points, I used the `sklearn.linear_model` Linear Regression function to predict the movement of the currency in the next minute using opening, closing, high and low values from the dataframe. Once the model is trained, we use the model to predict the movement of the currency in the next minute by feeding it the most recent data. If the model predicts an increase, we will buy as much as we can. Otherwise, we will make sure we have zero crypto in our portfolio. 

```
  X_train = train_data[['close', 'high', 'low', 'open']]
  y_train = train_data['next_output']


  # Create and fit a Linear Regression model
  model = LinearRegression()
  model.fit(X_train, y_train)

```


## Code Explanation:

This Python code employs Alpaca's API to create a trading bot that uses a linear regression model to predict cryptocurrency prices and execute trades accordingly. Below is a breakdown of the key sections and functionalities within the code:

### Importing Necessary Libraries:
- The code begins by importing required libraries such as `alpaca_trade_api`, `os`, `time`, `pandas`, and `sklearn.linear_model`.

### API Configuration and Initialization:
- It sets up the Alpaca API credentials (`API_KEY` and `API_SECRET`) stored in a separate `env.py` file and initializes the API connection using these keys.

### Define Target Asset and Parameters:
- Defines the target cryptocurrency symbol (`symbol`), timeframe for data (`timeframe`), and sets a budget (`budget`) for trading.

### Machine Learning Data Preparation:
- Initiates a loop (`while True`) to continuously fetch data and perform trading operations.
- Fetches historical cryptocurrency data (`crypto_data`) using the Alpaca API for the specified symbol and timeframe.
- Prepares a machine learning dataset (`ml_df`) by processing the fetched data, dropping unnecessary columns, and creating a column for the next price (`next_output`) to predict.

### Training the Machine Learning Model:
- Splits the data into training and testing sets (`train_data` and `test_data`) for model training.
- Defines features (`X_train`) and the target variable (`y_train`) for the linear regression model.
- Creates and fits a Linear Regression model using the training data.

### Model Prediction and Trading Decisions:
- Predicts the next price based on the model and the most recent cryptocurrency data.
- Determines whether to buy, sell, or hold based on predicted price changes compared to the current price.
- Executes buy or sell orders via the Alpaca API depending on predicted price trends and the current state of the portfolio.

### Saving Data:
- Saves the fetched cryptocurrency data to a .csv file within a specified directory (project3/data).

### Continual Execution and Delay:
- The code continuously loops and repeats the process of fetching data, training the model, making predictions, and executing trades.
- Includes a delay of 60 seconds (`time.sleep(60)`) between each iteration to prevent overwhelming API requests and allowing new market data to become available

## Testing and Optimization:

To test the strategy, I let the algorithm run with current market data, as well as feeding the API a timestamp of historical data. This helped me make sure that the algorithm was capable of actually making reasonable decisions, and this testing is what gave me the idea of using machine learning instead of my original algorithm. Another thing I realized I could optimize is that by getting only the last 100 minutes of data instead of the whole day, my machine learning algorithm was able to make predictions more accurately because the crypto market is constantly changing, and data from too long ago was not helpful for predicting future values. 

## Automation and Scheduling:

In the Python script, automation of the data retrieval process occurs through a continuous loop (`while True`) that fetches cryptocurrency market data using the Alpaca API. This script doesn't employ a specific scheduling mechanism but runs continuously, updating market data every minute (`time.sleep(60)`). The try-except block enables error handling, catching exceptions that might occur during data retrieval, model training, API interactions, or any other part of the code. If an exception occurs, it prints an error message containing the exception details (`print(f"An error occurred: {e}")`) and continues running. Regarding script version control, I have saved everything to a private git repository and consistently pushed code whenever I made a substantial change. 

## Paper Trading and Monitoring:

By using Alpaca’s paper trading feature, I was able to test the algorithm without risking any real money. I was able to let the algorithm run for long periods of time and manually see whether I was making or losing money, and in general I was able to make small amounts of money. The algorithm also prints the portfolio value to the terminal every iteration, so I can see how the value compares to the starting budget without navigating to the Alpaca website. 

## Results and Lessons Learned:

Throughout this project, I was able to develop a functional trading bot that used a Linear Regression model to predict cryptocurrency prices and execute trades accordingly. However, there were challenges encountered, notably in refining the trading strategy and ensuring consistent profitability. While this project was a good learning experience, it also made me realize that I have the skills to create interesting projects from scratch. Recognizing my own potential, I am motivated to explore and create more projects in the future. This project served as an excellent starting point, setting the stage for further exploration and development in the realm of software engineering.

## Compliance and Legal Considerations:

Algorithmic trading involves legal considerations to ensure compliance with financial regulations, particularly in preventing market manipulation and ensuring fair practices. My program aligns with these regulations by integrating risk management controls, transparency in decision-making, and adherence to both internal and external regulatory guidelines, maintaining market integrity and striving for compliance with evolving financial regulations.

## Conclusion:

In summary, this trading system harnesses algorithmic techniques and machine learning to facilitate automated cryptocurrency trading through the Alpaca platform. By employing a Linear Regression model, it predicts price movements and executes trades based on these predictions. The system retrieves market data, stores it in a file system, and continuously refines its strategy by analyzing the most recent 100 minutes of data, optimizing prediction accuracy. Testing revealed the system's capability to make reasonable decisions, leading to the adoption of machine learning over prior methods. Leveraging Alpaca's paper trading feature facilitated thorough testing without financial risk. Challenges were encountered in refining the strategy for consistent profitability. However, this project underscored the ability to create compelling projects from scratch, instilling motivation to delve deeper into software engineering. Ultimately, this project marks a significant stepping stone, providing insights and a foundation for further exploration in software engineering and algorithmic trading realms.


