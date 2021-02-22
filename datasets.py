# import the necessary packages
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def load_metric_vectors(path):
    # initialize the list of column names in the CSV file and then
    # load it using Pandas
    cols = ["AV", "AC", "PR", "UI", "CP"]
    df = pd.read_csv(path, sep=",", header=None, names=cols)
    return df


def process_metric_vectors(df, train, test):
    # initialize the column names of the continuous data
    continuous = ["AV", "AC", "PR", "UI"]
    # performing min-max scaling each continuous feature column to the range [0, 1]
    mm_scaler = MinMaxScaler()
    trainContinuous = mm_scaler.fit_transform(train[continuous])
    testContinuous = mm_scaler.transform(test[continuous])
    trainX = [trainContinuous]
    testX = [testContinuous]
    return (trainX, testX)

