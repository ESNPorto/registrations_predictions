
import json
import requests
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent / 'data'
MODEL_PATH = Path(__file__).parent / 'model.pkl'
FEATURES_PATH = Path(__file__).parent / 'model_features.pkl'

# Headers from the user provided curl command
API_URL = os.getenv("API_URL")
if not API_URL:
    print("Warning: API_URL not found in environment variables.")

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,pt-PT;q=0.9,pt;q=0.8,en-US;q=0.7",
    "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-access-token": os.getenv("EVENTUPP_API_TOKEN"),
    "Referer": "https://eventupp.eu/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def fetch_data():
    now = datetime.now()
    start_date = int((now - timedelta(days=365*4)).timestamp() * 1000)
    end_date = int((now + timedelta(days=365)).timestamp() * 1000)
    
    url = f"{API_URL}?startDate={start_date}&endDate={end_date}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('students', [])
    except Exception as e:
        print(f"Error fetching API data: {e}. Falling back to local data.")
        with open(DATA_DIR / 'eventupp_students_private.json', 'r') as f:
            data = json.load(f)
            # Local file might be the raw list or dict, sample showed dict with 'students'
            if isinstance(data, dict) and 'students' in data:
                return data['students']
            return data

def process_data(students_data):
    df = pd.DataFrame(students_data)
    df['registerDate_dt'] = pd.to_datetime(df['registerDate'], unit='ms')
    df = df.sort_values('registerDate_dt')
    return df

def get_weekly_aggregations(df):
    df_ts = df.set_index('registerDate_dt').sort_index()
    weekly_registrations = df_ts.resample('W').size()
    weekly_df = pd.DataFrame({
        'week_ending': weekly_registrations.index,
        'registrations': weekly_registrations.values
    })
    return weekly_df

def create_features_for_df(df):
    """
    Replicates the training feature generation.
    """
    df = df.copy()
    df['month'] = df['week_ending'].dt.month
    df['year'] = df['week_ending'].dt.year
    df['week_of_year'] = df['week_ending'].dt.isocalendar().week.astype(int)
    df['day_of_month'] = df['week_ending'].dt.day
    df['week_of_month'] = ((df['day_of_month'] - 1) // 7)
    df['is_welcome_month'] = ((df['week_ending'].dt.month == 2) | (df['week_ending'].dt.month == 9)).astype(int)
    df['semester'] = ((df['week_ending'].dt.month >= 2) & (df['week_ending'].dt.month <= 7)).astype(int)

    def calculate_week_of_semester(row):
        year = row['year']
        month = row['month']
        week_ending = row['week_ending']
        if month >= 8:
            semester_start = pd.Timestamp(year=year, month=8, day=1)
        elif month <= 7 and month >= 2:
            semester_start = pd.Timestamp(year=year, month=2, day=1)
        else:
            semester_start = pd.Timestamp(year=year-1, month=8, day=1)
        weeks_diff = (week_ending - semester_start).days // 7
        return max(0, weeks_diff)

    df['week_of_semester'] = df.apply(calculate_week_of_semester, axis=1)
    df['week_sin'] = np.sin(2 * np.pi * df['week_of_year'] / 52)
    df['week_cos'] = np.cos(2 * np.pi * df['week_of_year'] / 52)
    
    # Lag features
    for lag in [1, 2, 52]: 
        df[f'lag_abs_{lag}'] = df['registrations'].shift(lag)

    df['roll_mean_4_abs'] = df['registrations'].shift(1).rolling(window=4).mean() 
    df['roll_std_4_abs']  = df['registrations'].shift(1).rolling(window=4).std()  
    
    return df

CACHE_FILE = DATA_DIR / 'prediction_cache.json'

def get_cached_prediction():
    print(f"Checking cache at: {CACHE_FILE.absolute()}")
    if not CACHE_FILE.exists():
        print(f"Cache miss: File not found at {CACHE_FILE.absolute()}")
        return None
    
    try:
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
            
        last_updated = datetime.fromisoformat(data['last_updated'])
        current_date = datetime.now()
        
        # Check if same ISO week
        if last_updated.isocalendar()[:2] == current_date.isocalendar()[:2]:
            print(f"Cache hit: Using cached prediction from {last_updated}")
            return data
        else:
            print(f"Cache miss: Week mismatch. Cache: {last_updated.isocalendar()[:2]}, Current: {current_date.isocalendar()[:2]}")
            
    except Exception as e:
        print(f"Error reading cache: {e}")
        return None

    return None

def save_cached_prediction(data):
    try:
        print(f"Saving cache to {CACHE_FILE.absolute()}...")
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print("Cache saved successfully.")
    except Exception as e:
        print(f"Error saving cache: {e}")

def predict_future(weeks_to_predict=8):
    # 0. Check Cache
    cached_data = get_cached_prediction()
    if cached_data:
        return cached_data

    # 1. Load Data
    raw_data = fetch_data()
    df = process_data(raw_data)
    weekly_df = get_weekly_aggregations(df)
    
    # 2. Append future weeks
    last_date = weekly_df['week_ending'].max()
    future_dates = [last_date + timedelta(weeks=i+1) for i in range(weeks_to_predict)]
    
    future_df = pd.DataFrame({
        'week_ending': future_dates,
        'registrations': [np.nan] * weeks_to_predict
    })
    
    # Combine history + future
    full_df = pd.concat([weekly_df, future_df], ignore_index=True)
    
    # 3. Load Model
    model = joblib.load(MODEL_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    
    # 4. Iterative Prediction (Walk-forward)
    # We need to predict one week at a time because lags depend on previous predictions
    # However, since we have 'registrations' as target, and we need lag_abs_1 (t-1), 
    # we need to fill the NaN in 'registrations' for the future week once we predict it.
    
    train_cutoff_index = len(weekly_df)
    
    predictions = []
    
    for i in range(weeks_to_predict):
        current_idx = train_cutoff_index + i
        
        # Re-calculate features for the whole dataframe (or just update, but full recalc is safer for lags)
        # Note: Optimization would be better but for <200 rows it's instant.
        
        df_features = create_features_for_df(full_df)
        
        # Get the row to predict
        row_to_predict = df_features.iloc[[current_idx]].copy()
        
        # Select features
        X_pred = row_to_predict[feature_names]
        
        # Predict
        y_pred = model.predict(X_pred)[0]
        y_pred = max(0, int(round(y_pred)))
        
        # Store prediction in dataframe so next iteration sees it as history
        full_df.at[current_idx, 'registrations'] = y_pred
        sigma = joblib.load(DATA_DIR / 'model_sigma.pkl')
        
        predictions.append({
            'week_ending': full_df.at[current_idx, 'week_ending'].isoformat(),
            'prediction': y_pred,
            'confidence_lower': max(0, int(y_pred - 1.96 * sigma)),
            'confidence_upper': int(y_pred + 1.96 * sigma)
        })
        
    result = {
        'last_updated': datetime.now().isoformat(),
        'history': weekly_df.tail(12).assign(week_ending=lambda x: x['week_ending'].apply(lambda d: d.isoformat())).to_dict(orient='records'),
        'forecast': predictions
    }
    
    # 5. Save Cache
    save_cached_prediction(result)
    
    return result

if __name__ == "__main__":
    # Test run
    print(json.dumps(predict_future(), indent=2))
