# STK-INF-CC

- *Fransis Kolstø*       (Bachelor)
- *Wei Liu*              (Master)
- *Felix Schweinfest*    (Bachelor)
- *Harjeet Harpal*       (Master)


The two Jupyter Notebooks used in the presentation are found in the `presentation notebooks` folder.

To run the files [`.csv` file needed, not part of repository]: start MongoDB, since we stored our read files there. After that, the Flask web app is designed to read everything from the `.csv` file (due to privacy restrictions not provided in the GitHub repository, will be given on request) and store it in the MongoDB.

1) start `mongodb`
2) run `webapp.py` [disclaimer: the `kmeans` function doesn't work as of now and will maybe break the web app]

We put the linear regression prediction as well as the Multi Layer Perceptron prediction into `linearRegression.py`, but also use MLP training in `predModels.py`, since there the merging of MLP and time series prediction takes place.
`timeSeries.py` contains some explorative analysis and the research of a suitable subset of hyperparameters that would define the best time series model (seasonal ARIMA) using the functions stored in `gridsearch.py`; the code in `timeSeries.py` has to be run only once.
`Tspredict.py` contains a function that returns the fitted values and the predictions for the model we specify, with the purpose to feed them to the MLP.

Scraping YouTube videos to get information about advertisement campaigns was dropped, since it didn't improve the predictions by a meaningful level.
