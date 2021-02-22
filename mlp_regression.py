# import the necessary packages
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import datasets
import models
import numpy as np
import matplotlib.pyplot as plt

path = "/Users/ming/PycharmProjects/MachineLearning/cve_vectors.csv"

print("[INFO] loading metric_probability_vectors")
df = datasets.load_metric_vectors(path)
# construct a training and testing split with 75% of the data used for training and the remaining 25% for evaluation
print("[INFO] constructing training/testing split...")
(train, test) = train_test_split(df, test_size=0.15, random_state=42)

# find the largest condition probability in the training set and use it to
# scale our condition probabilities to the range [0, 1] (this will lead to better training and convergence)
maxProb = train["CP"].max()
trainY = train["CP"]
testY = test["CP"]

# process the metric probability data by performing min-max scaling on continuous features
print("[INFO] processing data...")
(trainX, testX) = datasets.process_metric_vectors(df, train, test)

# create our MLP and then compile the model using mean absolute
# percentage error as our loss, implying that we seek to minimize
# the absolute percentage difference between our probability predictions and the *actual prices*
model = models.create_mlp(4, regress=True) # 4 is the number of inputs
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)
# train the model
print("[INFO] training model...")
model.fit(x=trainX, y=trainY,
    validation_data=(testX, testY),
    epochs=30, batch_size=8)
# model.summary()
# make predictions on the testing data
print("[INFO] predicting conditional probabilities...")
preds = model.predict(testX)

# compute the difference between the *predicted* conditional probabilities and the
# actual conditional probabilities, then compute the percentage difference and
# the absolute percentage difference
diff = preds.flatten() - testY
percentDiff = (diff / testY) * 100
absPercentDiff = np.abs(percentDiff)
# compute the mean and standard deviation of the absolute percentage difference
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)

# show statistics on the model
print("[INFO] avg. difference of conditional probability: {}, std conditional probability: {}".format(mean,std))
print("Total values： {}, Input values: {} ， Predicted values: {}".format(len(train) + len(test), len(train), len(test)))
# print(preds)
# print(testY)
# plt.scatter(test['AC'], test['CP'], color='black')
# plt.show()