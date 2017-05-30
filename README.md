# STK-INF-CC

Fransis Kolstø      (Bachelor)
Wei Liu             (Master)
Felix Schweinfest   (Bachelor)
Harjeet Harpal      (Master)

The two jupyter notebooks used in the presentation are the (only) two in this repository: presentation29.05.17.ipynb and Timeseries.ipynb.

Running the files [csv file needed, not part of repository]: start mongoDB, since we store our read files there. After that, the flask web app is designed to read everything from the csv file (due to privacy restrictions not provided in the gitHub repository, will be given on request) and store it in the mongoDB.

1) start mongodb
2) run webapp.py [disclaimer: the 'kmeans' function doesn't work as of now and will maybe break the web app]

We put the linear regression prediction as well as the Multi Layer Perceptron prediction into linearRegression.py, but also use MLP training in predModels.py, since there the merging of MLP prediction and timeSeries prediction takes place.
Findinga suitable time series parameters happens in timeseries.py; Tspredict.py then uses the found parameters to predict what  is then fed to the MLP.

The .pkl files are trained MLP models. If they are deleted before run, the MLP model will re-train and re-create those files. Otherwise the prediction uses those pre-trained models. We used that for the sake of speed in the prediction and it only needs to be changed if parameters of training or the training data changes.

Scraping youtube videos to get information about advertisement campaigns was dropped, since it didn't improve the predictions by a meaningful level.
