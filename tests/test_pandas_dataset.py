from glob import glob
from algotrader.dataset.pandas_dataset import PandasDataset
from algotrader.utils import print_data
from datetime import datetime


def _initialize_dataset():
    START_DATE = datetime(2021, 12, 1)
    END_DATE = datetime(2022, 3, 1)

    files = glob("./data/*.csv")

    dataset = PandasDataset(files, START_DATE, END_DATE)
    return dataset


def test_pandas_dataset_print():
    dataset = _initialize_dataset()
    print(dataset)


def test_pandas_dataset_next():
    dataset = _initialize_dataset()
    print(dataset)
    print_data(next(dataset))
    print(dataset)
    print_data(next(dataset))
    print(dataset)
    print_data(next(dataset))
    print(dataset)


def test_pandas_dataset_get_stocks():
    dataset = _initialize_dataset()
    print(dataset.get_items())