""" Here we define the different ML models pipelines """
from src.data_preprocessing import *
from src.models import *
from sklearn.pipeline import make_pipeline, Pipeline
import lightgbm as lgb


def get_xgb_pipeline(**hyperparams) -> Pipeline:
    """Getting the xgboost pipeline"""
    # preprocessor
    preprocessor = get_preprocessor_pipeline()
    

    # sklearn pipeline
    return make_pipeline(
        preprocessor,
        xgb.XGBRegressor(**hyperparams)
    )

def get_LGBM_pipeline(**hyperparams) -> Pipeline:
    """Getting the xgboost pipeline"""
    # preprocessor
    preprocessor = get_preprocessor_pipeline()
    

    # sklearn pipeline
    return make_pipeline(
        preprocessor,
        lgb.LGBMRegressor(**hyperparams)
    )