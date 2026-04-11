import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

def clean_traffic_data(file_path):
    # 1. Load the raw data
    df = pd.read_csv(file_path)
    
    # 2. Convert timestamp strings to actual datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 3. Sort by location then time
    df = df.sort_values(by=['location', 'timestamp'])
    
    # 4. Handle the "3-hour gap"
    # We create a column to mark if a row is the start of a "new session" 
    # if the time jump from the previous row is > 20 minutes.
    df['time_diff'] = df.groupby('location')['timestamp'].diff().dt.total_seconds() / 60
    df['new_session'] = df['time_diff'] > 20 # True if there was a gap
    
    # 5. Scaling (Normalization)
    # We scale 'congestion_level' because it's our primary target for prediction
    scaler = MinMaxScaler()
    df['scaled_congestion'] = scaler.fit_transform(df[['congestion_level']])
    
    # Save the cleaned data to a new file
    output_path = 'data/cleaned_traffic_history.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Cleaning Complete! Saved to {output_path}")
    print(f"Total Rows: {len(df)}")
    return df

if __name__ == "__main__":
    if os.path.exists('data/traffic_history.csv'):
        clean_traffic_data('data/traffic_history.csv')
    else:
        print("Error: traffic_history.csv not found in 'data/' folder.")