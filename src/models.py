""" In this module we define the different models"""

import pandas as pd
import numpy as np

class BaselineModel:
    """
    In this baseline model the prediction is defined as following:
    prediction = median(count) on the same weekday observed in training data.
    Remarque : no feature engineering for this pipeline
    """
    def __init__(self):
        self.predictor = None

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        """This fonction compute values for the predictor"""

        X_temp = X_train.copy()
        y_train = y_train.copy()
        X_temp["weekday"] = (X_temp["datetime"]).dt.weekday
        Xy = X_temp.join(y_train)
        self.predictor = Xy.groupby("weekday")["count"].median().reset_index() 


    def predict(self, X_test: pd.DataFrame) -> np.array:
        """This fonction predict using the predictor got
        by fitting """
        weekday = X_test["datetime"].dt.weekday

        return  self.predictor.loc[self.predictor["weekday"] == weekday]["count"].item()
    

