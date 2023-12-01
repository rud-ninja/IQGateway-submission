import pandas as pd
from types import GeneratorType


class NestedCV:
    def __init__(self, k):
        self.k = k

    def split(self, data, date_column):
        unique_dates = sorted(data[date_column].unique())

        if (len(unique_dates)-1)/self.k < 1:
            error_message = "n_splits > number of month ends.. reduce number of splits"
            raise ValueError(error_message)
        
        train_size = (len(unique_dates)-1)//self.k

        for i in range(self.k):
            train_end_date = unique_dates[(i+1) * train_size]
            test_end_date = unique_dates[((i+1) * train_size) + 1]

            train = data[data[date_column] <= train_end_date]
            validate = data[(data[date_column] > train_end_date) & (data[date_column] <= test_end_date)]

            yield train, validate



if __name__ == "__main__":

    # data = pd.read_csv(r"/content/train.csv")
    # # data = data.copy()
    # # data["date"] = pd.to_datetime(data["date"])

    # k = 3
    cv = NestedCV(k)
    splits = cv.split(data, "date")

    assert isinstance(splits, GeneratorType)

    count = 0
    for train, validate in splits:

        assert isinstance(train, pd.DataFrame)
        assert isinstance(validate, pd.DataFrame)

        assert train.shape[1] == validate.shape[1]

        assert train["date"].max() <= validate["date"].unique()

        count += 1

    assert count == k