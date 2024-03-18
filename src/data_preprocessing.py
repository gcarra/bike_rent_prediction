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


def cleaning_data(
    raw_data: pd.DataFrame, split: bool = True
) -> Tuple[pd.DataFrame, pd.Series]:
    """This function is responsible for dataset cleaning"""

    # drop_duplicates
    cleaned_data = raw_data.drop_duplicates().copy()

    # convert datetime feature in datetime type
    cleaned_data["datetime"] = pd.to_datetime(raw_data["datetime"])
    # convert to categorical data
    cleaned_data["holiday"] = cleaned_data["holiday"].astype("bool")
    cleaned_data["workingday"] = cleaned_data["workingday"].astype("bool")
    cleaned_data["weather"] = cleaned_data["weather"].astype("category")

    # sort values by datetime
    cleaned_data = cleaned_data.sort_values(by="datetime")

    if split:
        # define target and feature dataframe
        target = cleaned_data["count"]
        features = cleaned_data.drop(["count"], axis=1).copy()

        return features, target
    return cleaned_data


def split_data(features: pd.DataFrame, target: pd.Series, ratio: float):
    """This fonction split data in train and test set
    ratio : ratio of data in train set"""
    features_train, features_test = np.split(features, [int(ratio * len(features))])
    target_train, target_test = np.split(target, [int(ratio * len(target))])
    return features_train, features_test, target_train, target_test


class feature_engineering:
    """Class in charge of the feature engineering.
    We define 3 methods
        Parameters
        ----------
        self.features: pd.Dataframe

        Returns
        -------
        None

    """

    def define_exra_features(self, features: pd.DataFrame):
        """
        Feature engineering 1: from the feature "datetime"
        we create four other features: year, month, day, hour
        """
        features["Month"] = (features["datetime"]).dt.month
        features["Year"] = (features["datetime"]).dt.year
        features["Weekday"] = (features["datetime"]).dt.weekday
        features["Hour"] = (features["datetime"]).dt.hour

        return features

    def transform_cyclical_values(self, features: pd.DataFrame):
        """Feature engineering 2: from the features month, day, hours
        we create cyclical features"""
        features["hour_cos"] = np.cos(features.Hour * (2.0 * np.pi / 24))
        features["month_sin"] = np.sin((features.Month - 1) * (2.0 * np.pi / 12))
        features["month_cos"] = np.cos((features.Month - 1) * (2.0 * np.pi / 12))
        features["day_cos"] = np.cos((features.Weekday) * (2.0 * np.pi / 7))
        features["hour_sin"] = np.sin(features.Hour * (2.0 * np.pi / 24))
        features["day_sin"] = np.sin((features.Weekday) * (2.0 * np.pi / 7))

        return features

    def drop_cols(self, features: pd.DataFrame):
        columns_to_drop = [
            "datetime",
            "casual",
            "atemp",
            "windspeed",
            "registered",
            "Hour",
            "season",
            "Month",
            "Weekday",
        ]
        return features.drop(columns_to_drop, axis=1).copy()


def get_preprocessor_pipeline() -> ColumnTransformer:
    """The function create the Column transformer of the
    preprocessing process"""

    preprocessor = make_column_transformer(
        (RobustScaler(), make_column_selector(dtype_include=np.number)),
        (OneHotEncoder(), make_column_selector(dtype_exclude=np.number)),
    )

    return preprocessor
