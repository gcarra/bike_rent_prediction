"""Module allowing the data preprocessing process"""

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.compose import (
    ColumnTransformer,
    make_column_selector,
    make_column_transformer,
)
from sklearn.preprocessing import OneHotEncoder, RobustScaler


def cleaning_data(raw_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """This function is responsible for dataset cleaning"""

    # drop_duplicates
    cleaned_data = raw_data.drop_duplicates().copy()

    # convert datetime feature in datetime type
    cleaned_data["datetime"] = pd.to_datetime(raw_data["datetime"])
    # convert to categorical data
    cleaned_data["holiday"] = cleaned_data["holiday"].astype("bool")
    cleaned_data["workingday"] = cleaned_data["workingday"].astype("bool")
    cleaned_data["weather"] = cleaned_data["weather"].astype("category")

    target = cleaned_data["count"]
    features = cleaned_data.drop(["count"], axis=1).copy()

    return features, target


def feature_engineering(features: pd.DataFrame) -> pd.DataFrame:
    """function in charge of the feature engineering"""
    # Feature engineering 1: from the feature "datetime"
    # we create four other features: year, month, day, hour
    features["Year"] = pd.to_datetime(features["datetime"]).dt.year
    features["Month"] = pd.to_datetime(features["datetime"]).dt.month
    features["Day"] = pd.to_datetime(features["datetime"]).dt.weekday
    features["Hour"] = pd.to_datetime(features["datetime"]).dt.hour

    # Feature engineering 2: from the features month, day, hours we create cyclical features
    features["hour_sin"] = np.sin(features.Hour * (2.0 * np.pi / 24))
    features["hour_cos"] = np.cos(features.Hour * (2.0 * np.pi / 24))
    features["month_sin"] = np.sin((features.Month - 1) * (2.0 * np.pi / 12))
    features["month_cos"] = np.cos((features.Month - 1) * (2.0 * np.pi / 12))
    features["day_sin"] = np.sin((features.Day) * (2.0 * np.pi / 7))
    features["day_cos"] = np.cos((features.Day) * (2.0 * np.pi / 7))

    columns_to_drop = [
        "datetime",
        "casual",
        "atemp",
        "windspeed",
        "registered",
        "Hour",
        "season",
        "Month",
        "Day",
    ]
    features = features.drop(columns_to_drop, axis=1)
    return features


def get_preprocessor_pipeline() -> ColumnTransformer:
    """The function create the Column transformer of the
    preprocessing process"""

    preprocessor = make_column_transformer(
        (RobustScaler(), make_column_selector(dtype_include=np.number)),
        (OneHotEncoder(), make_column_selector(dtype_exclude=np.number)),
    )

    return preprocessor
