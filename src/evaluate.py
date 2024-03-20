""" In this model we create the function to evualuate the model"""

import pandas as pd
from sklearn.metrics import mean_absolute_error

from src.data_preprocessing import cleaning_data, feature_engineering, split_data
from src.models import *


def evaluate_Baseline(raw_data: pd.DataFrame):
    """
    The fonction evaluate the baseline model

        Returns
        -------
        test_mae: float
            Mean average error on test set
        mean_test_count: float
            Average number of users on test set
        train_mae: float
            Mean average error
        mean_train_count: float
            Average number of users on train set

    """
    features, target = cleaning_data(raw_data)

    (features_train, features_test, target_train, target_test) = split_data(
        features, target, 0.8
    )

    model = BaselineModel()
    model.fit(features_train, target_train)

    predictions = model.predict(features_test)
    predictions_train = model.predict(features_train)

    test_mae = mean_absolute_error(target_test, predictions)
    mean_test_count = target_test.mean()

    train_mae = mean_absolute_error(target_train, predictions_train)
    mean_train_count = target_train.mean()

    return test_mae, mean_test_count, train_mae, mean_train_count


def evaluate_xgb(raw_data: pd.DataFrame, **hyperparams):
    """
    The fonction evaluate the xgboost model

        Returns
        -------
        test_mae: float
            Mean average error on test set
        mean_test_count: float
            Average number of users on test set
        train_mae: float
            Mean average error
        mean_train_count: float
            Average number of users on train set

    """

    features, target = cleaning_data(raw_data)
    features_process = feature_engineering()
    features = features_process.define_exra_features(features)
    features = features_process.transform_cyclical_values(features)
    features = features_process.drop_cols(features)

    (features_train, features_test, target_train, target_test) = split_data(
        features, target, 0.8
    )

    xgb_pipeline = get_xgb_pipeline(**hyperparams)
    xgb_pipeline.fit(features_train, target_train)

    predictions = xgb_pipeline.predict(features_test)
    predictions_train = xgb_pipeline.predict(features_train)

    test_mae = mean_absolute_error(target_test, predictions)
    mean_test_count = target_test.mean()

    train_mae = mean_absolute_error(target_train, predictions_train)
    mean_train_count = target_train.mean()

    return test_mae, mean_test_count, train_mae, mean_train_count


def evaluate_LGBM(raw_data: pd.DataFrame, **hyperparams):
    """
    The fonction evaluate the LGBM model

        Returns
        -------
        test_mae: float
            Mean average error on test set
        mean_test_count: float
            Average number of users on test set
        train_mae: float
            Mean average error
        mean_train_count: float
            Average number of users on train set

    """

    features, target = cleaning_data(raw_data)
    features_process = feature_engineering()
    features = features_process.define_exra_features(features)
    features = features_process.transform_cyclical_values(features)
    features = features_process.drop_cols(features)

    (features_train, features_test, target_train, target_test) = split_data(
        features, target, 0.8
    )

    LGBM_pipeline = get_LGBM_pipeline(**hyperparams)
    LGBM_pipeline.fit(features_train, target_train)

    predictions = LGBM_pipeline.predict(features_test)
    predictions_train = LGBM_pipeline.predict(features_train)

    test_mae = mean_absolute_error(target_test, predictions)
    mean_test_count = target_test.mean()

    train_mae = mean_absolute_error(target_train, predictions_train)
    mean_train_count = target_train.mean()

    return test_mae, mean_test_count, train_mae, mean_train_count
