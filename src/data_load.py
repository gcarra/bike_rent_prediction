""" This module contains functions to load data """

from pathlib import Path

import requests

from src.path import DATA_DIR


def download_dataset() -> Path:
    """Download the dataset and save it in the data folder as csv file"""
    URL = "https://www.kaggle.com/datasets/archit9406/bike-sharing/download?datasetVersionNumber=1"
    response = requests.get(URL, timeout=40)
    if response.status_code == 200:
        path = DATA_DIR / "raw_data.csv"
        with open(path, "wb") as file:
            file.write(response.content)
        return path
    raise Exception(f"{URL} is not available")
