import streamlit as st
import pandas as pd
from modules.transport.data_fetch import ensure_transport_data

@st.cache_data
def load_and_clean_transport_data():
    """Load, clean, and perform feature engineering on the NYC taxi dataset."""
    data_path = ensure_transport_data()
    if data_path is None:
        return pd.DataFrame()

    df = pd.read_csv(data_path)

    # Basic cleaning
    df.rename(columns={
        'lpep_pickup_datetime': 'pickup_datetime',
        'lpep_dropoff_datetime': 'dropoff_datetime',
        'PULocationID': 'pickup_location_id',
        'DOLocationID': 'dropoff_location_id',
        'passenger_count': 'passengers',
    }, inplace=True)

    # Convert to datetime and feature engineering
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    df['trip_duration_mins'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_weekday'] = df['pickup_datetime'].dt.day_name()
    df['pickup_date'] = df['pickup_datetime'].dt.date
    df['route'] = df['pickup_location_id'].astype(str) + ' -> ' + df['dropoff_location_id'].astype(str)

    # Map payment type to readable names
    payment_type_map = {
        1: 'Credit card',
        2: 'Cash',
        3: 'No charge',
        4: 'Dispute',
        5: 'Unknown',
        6: 'Voided trip'
    }
    df['payment_type_name'] = df['payment_type'].map(payment_type_map).fillna('Unknown')

    # Filter out unreasonable trips
    df = df[(df['trip_duration_mins'] > 0) & (df['trip_duration_mins'] < 120)]
    df = df[df['passengers'] > 0]
            
    return df
