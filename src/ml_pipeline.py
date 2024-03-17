""" Here we define the different ML models pipelines """
import lightgbm as lgb
import xgboost as xgb
from sklearn.pipeline import Pipeline, make_pipeline

from src.data_preprocessing import get_preprocessor_pipeline


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
