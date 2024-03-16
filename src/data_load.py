""" This module contains functions to load data """
from pathlib import Path
from src.path import DATA_DIR
import requests


def download_dataset() -> Path:
    URL = "https://www.kaggle.com/datasets/archit9406/bike-sharing/download?datasetVersionNumber=1"
    response = requests.get(URL)
    if response.status_code == 200:
        path = DATA_DIR / "raw_data.csv"
        open(path, "wb").write(response.content)
        return path
    else:
        raise Exception(f"{URL} is not available")
