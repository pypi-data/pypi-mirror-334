import pandas as pd
import numpy as np
import yfinance as yf


def trueRange(row):
    '''
    row: High Low, previousClose
    '''
    return max(abs(row[0]-row[2]),abs(row[1]-row[2]),row[0]-row[1])



def calculate_true_range(df, lookback_period=14):
    """
    Calculate True Range (TR) and Average True Range (ATR) for a given DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing ["High", "Low", "Close"] columns.
    lookback_period (int): Period for calculating ATR (default is 14).

    Returns:
    pd.DataFrame: DataFrame with added columns "True Range" and "ATR".
    """
    # Ensure the required columns are present
    required_columns = ["High", "Low", "Close"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Shift Close to get Previous Close
    df["Previous Close"] = df["Close"].shift(1)

    # Calculate True Range (TR)
    df["True Range"] = df.apply(
        lambda row: max(
            abs(row["High"] - row["Low"]),  # High - Low
            abs(row["High"] - row["Previous Close"]),  # High - Previous Close
            abs(row["Low"] - row["Previous Close"]),  # Low - Previous Close
        ),
        axis=1
    )

    # Calculate Average True Range (ATR) using Exponential Moving Average
    df["ATR"] = df["True Range"].ewm(span=lookback_period, adjust=False).mean()

    return df