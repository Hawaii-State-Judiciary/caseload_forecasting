import pandas as pd # For reading and handling the dataset
import statsmodels.api as sm # A tool for fitting the regression model
from statsmodels.tsa.arima.model import ARIMA # For creating the time series model 
import matplotlib.pyplot as plt
import os

# Data containing extracted statistics
file_path = '/Users/kanoa/Desktop/Judiciary senza time.xlsx' 
data = pd.read_excel(file_path)
response = data['Filed']
predictors = data[['Pending at Start', 'Total Caseload', 'Terminated', 
                   'Pending at End', 'General Fund Expenditure', 
                   'Special Fund Expenditure', 'General Fund Appropriations', 
                   'Special Fund Appropriations']]

# A constant to the predictors which adds a baseline value to the model, allowing predictions even when all other variables are zero
predictors = sm.add_constant(predictors)

# For fitting the multiple linear regression model
regression_model = sm.OLS(response, predictors).fit()

# For getting the beta weights from the regression model
beta_weights = regression_model.params
print("\n--- Beta Weights for Multiple Linear Regression ---\n")
print(beta_weights)

# Time series data for 'Filed'
filed_series = data['Filed']

# For fitting a basic ARIMA model
arima_model = ARIMA(filed_series, order=(1, 1, 1)).fit()

# ARIMA forecasting future values
forecast_steps = 5
forecast = arima_model.get_forecast(steps=forecast_steps)
forecast_mean = forecast.predicted_mean
confidence_intervals = forecast.conf_int()

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(filed_series.index, filed_series, label='Original Data', color='black')
plt.plot(range(len(filed_series), len(filed_series) + forecast_steps), forecast_mean, label='Forecast', color='blue')
plt.fill_between(range(len(filed_series), len(filed_series) + forecast_steps), 
                 confidence_intervals.iloc[:, 0], 
                 confidence_intervals.iloc[:, 1], 
                 color='blue', alpha=0.3)

# With Grid Lines^
plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
plt.minorticks_on()  # Enable minor ticks for finer grid
plt.title('Filed Forecast using ARIMA Model')
plt.xlabel('Year')
plt.ylabel('Filed')
plt.legend()
plt.show()

# For saving the regression and ARIMA results
output_file = 'model_summaries.txt'
try:
    with open(output_file, 'w') as f:
        f.write("--- Multiple Linear Regression Summary ---\n")
        f.write(str(regression_model.summary()) + "\n\n")
        f.write("--- ARIMA Model Summary ---\n")
        f.write(str(arima_model.summary()) + "\n")
    print(f"\nModel summaries saved successfully to '{output_file}'.")
except Exception as e:
    print(f"\nFailed to save model summaries. Error: {e}")

# For double checking that the file was created
if os.path.exists(output_file):
    print(f"\nThe summary file '{output_file}' exists.")
else:
    print(f"\nThe summary file '{output_file}' was not created.")
