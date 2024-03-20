""" This function return the evaluation"""
from src.evaluate import *
from src.path import DATA_DIR


def display_results(test_mae, mean_test_count, train_mae, mean_train_count):
    """
    Function displaying results
    """
    print(f"The mean absolute error of the test set is {test_mae:.2f}")
    print(f"The average hourly number of users of the test set is {mean_test_count:.2f}\n")

    print(f"The mean absolute error of the train set is {train_mae:.2f}")
    print(f"The average hourly number of users of the train set is {mean_train_count:.2f}\n")

if __name__ == "__main__":

    raw_data = pd.read_csv(DATA_DIR / "raw_data.csv") 

    test_mae, mean_test_count, train_mae, mean_train_count = evaluate_Baseline(raw_data)
    print('\n Baseline model')
    display_results(test_mae, mean_test_count, train_mae, mean_train_count)
    print("\n")

    test_mae, mean_test_count, train_mae, mean_train_count = evaluate_xgb(raw_data)
    print('\n XGBoost model')
    display_results(test_mae, mean_test_count, train_mae, mean_train_count)

    test_mae, mean_test_count, train_mae, mean_train_count = evaluate_LGBM(raw_data, force_col_wise = True)
    print('\n LightGBM model')
    display_results(test_mae, mean_test_count, train_mae, mean_train_count)