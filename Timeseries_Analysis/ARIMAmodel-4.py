import pandas as pd  # For handling and manipulate contnets of a CSV files or like
import itertools  # The generator for combinations of parameters for ARIMA model tuning
import statsmodels.api as sm  # For statistical modeling, including ARIMA
import warnings  # TO override and suppress warning messages that may clutter output
import matplotlib.pyplot as plt  # Visualize the data and results

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Dataset containing monthly court case filings from 1998 to 2024
file_path = '/Users/kanoa/Downloads/monthly_case_filings_1998-2024.csv'
data = pd.read_csv(file_path)  # Reads the CSV file into a DataFrame

# FOR EXAMPLE
# 1C and case type ('Civil_Action')
# This^^ helps isolate data relevant to a specific category rather than analyzing everything at once.
filtered_data = data[(data['COURT'] == '1C') & (data['CASE_TYPE_NAME'] == 'Civil_Action')]

# For converting the 'YEAR' and 'MONTH' columns into a datetime format with the first day of each month
# This creates a time index which is critcial for time series analysis
filtered_data['DATE'] = pd.to_datetime(filtered_data[['YEAR', 'MONTH']].assign(DAY=1))

# Set the data in chronological order for modeling
filtered_data = filtered_data.sort_values('DATE')

# Set 'DATE' as the index of the DataFrame and extract only the case count column for analysis
time_series = filtered_data.set_index('DATE')['CASE_COUNT']

# RECAP of variables signficance:
# p: Number of lag observations included in the model (autoregession)
# d: Number of times the data needs to be differenced to make it stationary
# q: Size of the moving average window
p = range(0, 5)  # Testing AR terms from 0 to 4
d = range(0, 2)  # Testing differencing terms from 0 to 1
q = range(0, 5)  # Testing MA terms from 0 to 4

# Generate all possible combinations of (p, d, q) for the ARIMA model
pdq_combinations = list(itertools.product(p, d, q))

best_aic = float("inf")  # AIC (Akaike Information Criterion) - lower is better for model selection
best_order = None  # To keep track of the best combination of (p, d, q)
best_model = None  # To store the best ARIMA model

print("Starting ARIMA grid search...")

# For iterating through each combination of (p, d, q) values and evaluate the ARIMA model
for param in pdq_combinations:
    try:
        # Fit an ARIMA model with the current (p, d, q) values
        model = sm.tsa.ARIMA(time_series, order=param)
        result = model.fit()
        
        # Print the model parameters and the corresponding AIC value
        print(f'Tested ARIMA{param} - AIC: {result.aic:.2f}')
        
        # Check if the current model has a lower AIC than the best model found so far
        if result.aic < best_aic:
            best_aic = result.aic  # Update best AIC score
            best_order = param  # Update the best model order (p, d, q)
            best_model = result  # Store the best model
    except Exception as e:
        # Handle cases where model fitting fails due to invalid parameter combinations
        print(f"Error with parameters {param}: {e}")
        continue

# Display the best model order and its AIC score after testing all combinations
print("\nOptimal ARIMA order:", best_order)
print("Optimal AIC:", best_aic)

# Plot actual data versus the best fitted ARIMA model values
plt.figure(figsize=(12, 6))
plt.plot(time_series, label='Actual', color='blue')  
plt.plot(time_series.index, best_model.fittedvalues, label='Fitted', color='red', linestyle='--')  
plt.title(f'Best ARIMA{best_order} Model Fit')  # Title with best model order
plt.xlabel('Date')  
plt.ylabel('Case Count')  
plt.legend()  
plt.grid(True, linestyle='--', alpha=0.6)  
plt.show()

# Forecasting the next 12 months using the best ARIMA model
forecast_steps = 12  
forecast = best_model.get_forecast(steps=forecast_steps)  # Generate forecast

# Create a date index for the forecasted period
forecast_index = pd.date_range(time_series.index[-1], periods=forecast_steps + 1, freq='M')[1:]

# Extract the forecasted values and confidence intervals
forecast_values = forecast.predicted_mean  
forecast_conf_int = forecast.conf_int()  # Confidence intervals (upper and lower bounds)

# Plot the actual data along with the forecasted values
plt.figure(figsize=(12, 6))
plt.plot(time_series, label='Actual', color='blue')  # Plot the historical data
plt.plot(forecast_index, forecast_values, label='Forecast', color='green')  # Plot forecasted values
plt.fill_between(forecast_index, forecast_conf_int.iloc[:, 0], forecast_conf_int.iloc[:, 1], color='lightgreen', alpha=0.3)
plt.title(f'Forecast using ARIMA{best_order}')  
plt.xlabel('Date')  
plt.ylabel('Case Count')  
plt.legend()  
plt.grid(True, linestyle='--', alpha=0.6)  
plt.show()
print("\nForecasted values for the next 12 months:")
print(forecast_values)
