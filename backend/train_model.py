
import json
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
import joblib

warnings.filterwarnings('ignore')

DATA_DIR = Path(__file__).parent / 'data'
MODEL_PATH = Path(__file__).parent / 'model.pkl'

def create_features(df):
    df = df.copy()

    df['month'] = df['week_ending'].dt.month
    df['year'] = df['week_ending'].dt.year
    df['week_of_year'] = df['week_ending'].dt.isocalendar().week.astype(int)

    # Calculate week of month (0-5)
    df['day_of_month'] = df['week_ending'].dt.day
    df['week_of_month'] = ((df['day_of_month'] - 1) // 7)

    # Is welcome month (February=2 or September=9)
    df['is_welcome_month'] = ((df['week_ending'].dt.month == 2) | (df['week_ending'].dt.month == 9)).astype(int)

    # Semester: 0 for fall (Aug-Jan), 1 for spring (Feb-Jul)
    df['semester'] = ((df['week_ending'].dt.month >= 2) & (df['week_ending'].dt.month <= 7)).astype(int)

    # Week of semester calculation
    def calculate_week_of_semester(row):
        year = row['year']
        month = row['month']
        week_ending = row['week_ending']

        if month >= 8:  # Fall semester (Aug-Dec)
            semester_start = pd.Timestamp(year=year, month=8, day=1)
        elif month <= 7 and month >= 2:  # Spring semester (Feb-Jul)
            semester_start = pd.Timestamp(year=year, month=2, day=1)
        else:  # January (still fall semester of previous academic year)
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

def load_data():
    with open(DATA_DIR / 'eventupp_students_private.json', 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)

    df['registerDate'] = pd.to_datetime(df['registerDate'], unit='ms')
    df_ts = df.set_index('registerDate').sort_index()

    weekly_registrations = df_ts.resample('W').size()

    weekly_df = pd.DataFrame({
        'week_ending': weekly_registrations.index,
        'registrations': weekly_registrations.values
    })
    return weekly_df

def train():
    print("Loading data...")
    df = load_data()
    
    print("Creating features...")
    df_features = create_features(df)
    
    df_model = df_features.dropna()
    
    target = 'registrations'
    features = [c for c in df_model.columns if c not in ['registrations', 'week_ending', 'day_of_month', 'is_welcome_month', 'week_of_month']]
    
    X = df_model.drop(columns=['registrations', 'week_ending'])
    y = df_model['registrations']
    
    print(f"Training on {len(X)} samples with {X.shape[1]} features...")
    
    model = XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        objective='reg:absoluteerror',
        n_jobs=-1,
        random_state=42
    )
    
    model.fit(X, y)

    predictions = model.predict(X)
    residuals = y - predictions
    sigma = np.std(residuals)
    
    joblib.dump(sigma, MODEL_PATH.parent / 'model_sigma.pkl')
    
    print("Saving model to", MODEL_PATH)
    joblib.dump(model, MODEL_PATH)
    
    joblib.dump(X.columns.tolist(), MODEL_PATH.parent / 'model_features.pkl')
    print("Done.")

if __name__ == "__main__":
    train()
