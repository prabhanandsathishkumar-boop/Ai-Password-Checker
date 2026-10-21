"""Entry point: build the labelled training dataset."""

from utils.console import enable_utf8
from utils.data_preprocessing import generate_labeled_csv

if __name__ == "__main__":
    enable_utf8()
    generate_labeled_csv()
