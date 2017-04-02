<!-- background: #fff -->
<!-- color: #000 -->
<!-- font: frutiger -->

# Business idea:
Tool for HR management

We've been provided with a dataset of customer service calls from Telenor with the task of predicting the number of calls for the upcoming eight weeks. The aim is to better prepare the customer department for distributing manpower.

We explored the possibilities of introducing external variables which are not commonly included in such analysis (i.e. weather data, the dates when AD campaigns are launched)

## Data cleaning
### Call Data
* Make the data even spaced, fill the time points where no calls are recorded with 0

* Set number of calls received from 20:30 to 7:45 to 0, when no calls are generally expected. The reason for doing so is that on special occasions (i.e. system outage), the customer service centre receives large number of calls and extra need of manpower should be expected. Thus when fitting the model, we removed these calls to avoid their effect on the prediction on regular days.

## Exploratory analysis

Plotting to look for potential pattern(i.e. periodicity, trend)

![alt text](https://github.com/Fransisnk/STK-INF-CC/blob/master/plots/totplot.png "Number of Calls of 4 Types")


## Outlier detection by Clustering

Classified days into 3 clusters. 

Introducing clusters beyond the 4th produces no meaningful cluster.

![alt text](https://github.com/Fransisnk/STK-INF-CC/blob/master/plots/clustertot.png "Calls in 3 Clusters")


# Modeling

* Linear regression

* Multi-layer Perceptron Analysis

## Preventing overfitting

Used early stopping to prevent overfitting