import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

#  FUNCTION 1: Load CSV data
def load_data(filepath):
    #Loads sales time series data from a CSV file.
    df = pd.read_csv(filepath, parse_dates=['ds']) #parse_dates tells pandas to automatically convert the 'ds' column into datetime objects
    df = df.sort_values('ds') #sort the dataframe by the 'dates' column
    return df

# FUNCTION 2: Fit a Prophet model & forecast future
def forecast_sales(df, periods=30):
    model = Prophet()
    model.fit(df) #fit the model to the data
    future = model.make_future_dataframe(periods=periods) #create a dataframe with future dates
    forecast = model.predict(future) #predict future values
    return model, forecast #returns the fitted model and the forecasted values

# FUNCTION 3: Plot forecast result
def plot_forecast(model, forecast):
    model.plot(forecast) #plot the forecasted values
    plt.title("Sales Forecast") #add title
    plt.xlabel("Date") #add x-axis label
    plt.ylabel("Sales") #add y-axis label
    plt.show() #display the plot


# Main function to run the steps
if __name__ == "__main__":
    # Path to your sample sales data
    filepath = "data/sample_sales.csv"
    
    # Step 1: Load the data from CSV
    df = load_data(filepath)
    print(df.head())  # Print the first few rows for sanity check
    
    # Step 2: Forecast future sales using Prophet
    model, forecast = forecast_sales(df, 30)
    
    # Step 3: Plot the forecasted results
    plot_forecast(model, forecast)