# STK-INF-CC

First thing: start mongoDB, since we store our read files there. After that, the flask web app is designed to read everything from the csv file (due to privacy restrictions not provided in the gitHub repository, will be given on request) and store it in the mongoDB.

1) start mongodb
2) run webapp.py [disclaimer: the 'kmeans' function doesn't work as of now and will maybe break the web app]

We put the linear regression prediction as well as the Multi Layer Perceptron prediction into linearRegression.py, but also use MLP training in predModels.py, since there the merging of MLP prediction and timeSeries prediction takes place.
The time series modeling happens in

