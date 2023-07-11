import os

from dataset import AnalisysThreads
from const import *
from ml import get_model_base


def main():
    api_key = os.getenv("API_KEY")
    model = get_model_base()
    AnalisysThreads(api_key, [NEGATIVE_VIDEO, NEUTRAL_VIDEO, POSITIVE_VIDEO], model).run()


if __name__ == "__main__":
    main()
