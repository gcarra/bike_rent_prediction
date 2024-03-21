""" In this module we define the different ML models and pipelines """

import pandas as pd
import numpy as np
import lightgbm as lgb
import xgboost as xgb
from sklearn.pipeline import Pipeline, make_pipeline

from src.data_preprocessing import get_preprocessor_pipeline


class BaselineModel:
    """
    In this baseline model the prediction is defined as following:
    prediction = median(count) on the same weekday observed in training data.
    Remark: no feature engineering for this pipeline
    """

    def __init__(self):
        self.predictor = None

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        """This fonction compute values for the predictor"""

        # define weekday attribute
        X_train["weekday"] = (X_train["datetime"]).dt.weekday
        X_train["Hour"] = (X_train["datetime"]).dt.hour
        
        Xy = X_train.join(y_train)
        
        # compute the prediction and rename column
        self.predictor = Xy.groupby(["weekday","Hour" ])["count"].median().reset_index()
        self.predictor = self.predictor.rename(columns={"count": "pred_count"})

    def predict(self, X_test: pd.DataFrame) -> np.array:
        """This fonction predict using the predictor got
        by fitting"""
        X_test["weekday"] = X_test["datetime"].dt.weekday
        X_test["Hour"] = X_test["datetime"].dt.hour

        X_test = X_test.merge(self.predictor, how="left", on=["weekday", "Hour"])

        return X_test["pred_count"]


def get_xgb_pipeline(**hyperparams) -> Pipeline:
    """Getting the xgboost pipeline"""
    # preprocessor
    preprocessor = get_preprocessor_pipeline()

    # sklearn pipeline
    return make_pipeline(preprocessor, xgb.XGBRegressor(**hyperparams))


def get_LGBM_pipeline(**hyperparams) -> Pipeline:
    """Getting the xgboost pipeline"""
    # preprocessor
    preprocessor = get_preprocessor_pipeline()

    # sklearn pipeline
    return make_pipeline(preprocessor, lgb.LGBMRegressor(**hyperparams))
