import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def clean_cycles(df):
    #### clean cycles data
    cycles_cleaned = df.dropna()
    # convert date columns to datetime
    cycles_cleaned['Cycle start time'] = pd.to_datetime(cycles_cleaned['Cycle start time'], dayfirst=True)
    cycles_cleaned['Cycle end time'] = pd.to_datetime(cycles_cleaned['Cycle end time'], dayfirst=True)
    # create new date columns
    cycles_cleaned['start date'] = cycles_cleaned['Cycle start time'].dt.date
    cycles_cleaned['end date'] = cycles_cleaned['Cycle end time'].dt.date
    # create new cycle length column
    cycles_cleaned['Cycle length'] = cycles_cleaned['Cycle end time'] - cycles_cleaned['Cycle start time']
    # remove any cycles with length less than 20 or greater than 30 hours
    cycles_cleaned = cycles_cleaned[(cycles_cleaned['Cycle length'].dt.total_seconds() / 3600 >= 20) &(cycles_cleaned['Cycle length'].dt.total_seconds() / 3600 <= 30)]

    return cycles_cleaned

def clean_sleep_length(df):
    # Convert the date columns to datetime objects if they are not already
    df['Sleep onset'] = pd.to_datetime(df['Sleep onset'])
    df['Wake onset'] = pd.to_datetime(df['Wake onset'])
    # Calculate the sleep length in hours
    df['Sleep Length'] = (df['Wake onset'] - df['Sleep onset']).dt.total_seconds() / 3600  # Convert to hours
    # Filter rows with sleep length >= 4 hours as anything under 4 hours is more likely a nap
    df = df[df['Sleep Length'] >= 4]
    columns_to_drop = ['Cycle timezone']
    df = df.drop(columns=columns_to_drop)

    return df

def add_journal_data(df, journals):
    ### bring in journals data
    columns_to_drop = ['Cycle timezone', 'Notes']
    journals = journals.drop(columns=columns_to_drop)
    # Pivot the DataFrame to get the desired format
    journals = journals.pivot(index=['Cycle start time', 'Cycle end time'], columns='Question text', values='Answered yes').reset_index()
    # convert date columns to datetime
    journals['Cycle start time'] = pd.to_datetime(journals['Cycle start time'], dayfirst=True)
    journals['Cycle end time'] = pd.to_datetime(journals['Cycle end time'], dayfirst=True)
    # merge
    merged_df = df.merge(journals, on=['Cycle start time', 'Cycle end time'], how='inner')

    return merged_df

def create_features(df):
    df['Cycle start time'] = pd.to_datetime(df['Cycle start time'])
    df['Cycle end time'] = pd.to_datetime(df['Cycle end time'])
    df['start date'] = pd.to_datetime(df['start date'])
    df['end date'] = pd.to_datetime(df['end date'])
    # perform feature engineering
    # Calculate the percentage of time spent in deep sleep
    df['Percentage Deep Sleep'] = (df['Deep (SWS) duration (min)'] / df['Asleep duration (min)']) * 100
    df['Percentage REM Sleep'] = (df['REM duration (min)'] / df['Asleep duration (min)']) * 100
    # calculate moving average of recover over past week
    df = df.sort_values(by='start date')
    df['Recovery 7-Day Moving Average'] = df['Recovery score %'].rolling(window=7, min_periods=1).mean()
    # Calculate metrics like weekly or monthly total exercise time or intensity level.
    # calculate moving average of strain over past week
    df['Starin 7-Day Moving Average'] = df['Day Strain'].rolling(window=7, min_periods=1).mean()

    return df

def external_data(df, weather_data):
    weather_data['date'] = pd.to_datetime(weather_data['date'], dayfirst=True)
    weather_data = weather_data[['date', 'rain', 'sun', 'maxtp', 'mintp']]
    # Filter the DataFrame based on the date range
    start_date = '2022-12-30'
    end_date = '2023-05-19'
    weather_data = weather_data[(weather_data['date'] >= start_date) & (weather_data['date'] <= end_date)]
    merged_df = df.merge(weather_data, left_on='end date', right_on='date', how='inner')

    return merged_df

