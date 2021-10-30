# Malaysia COVID-19 Cases and Vaccination

An in-depth extension of our previous [Assignment](https://github.com/BingQuanChua/COVID-19-Msia-Mining).

Our work must consist of 
- ~~1️⃣ association rule mining algorithm,~~ => change to :one: of the below
- at least 2️⃣ classification models, 
- at least 2️⃣ regression models, and 
- 1️⃣ clustering technique.

We must provide visualization to your findings and analyze them accordingly.

## 📚Datasets	

Data taken as of **`6-10-2021`**

Covid-19 Open Data:
https://github.com/MoH-Malaysia/covid19-public

Vaccination Data:
https://github.com/CITF-Malaysia/citf-public

❌ datasets that are not in use: `clusters.csv`, `hospital.csv`, `icu.csv`, `pkrc.csv`

## 📋To-Do List

Exploratory Data Analysis

- [ ] A little bit more

Data Mining Questions

- [ ] Clustering Analysis 
- [ ] Time Series Regression
- [ ] Time Series Regression 2
- [ ] Classification

Deployment

- [ ] Streamlit webapp

Project report

- [ ] Report typed in LaTeX

## ❓Questions

**Clustering**
* Access how well does each state handle covid cases based on pass covid records (cases, population, test)
Suggested methods: time-series clustering.
PIC: Ryan

**Regression**
* In order to deploy appropriate movement control measures, how can the government accurately predict of weely new cases based on past data?
* Predict the vaccination rate based on past data?
Suggested methods: LSTMNet, ARIMA
PIC: Bing

**Classification**
* By using previous 3, 5, 7 days covid records, come out with a model that can classify next day / week’s cases.
Suggested methods: dunno
PIC: KY

## 📑References

1. [COVID-19: What Is Hidden Behind the Official Numbers?](https://towardsdatascience.com/which-countries-are-affected-the-most-by-covid-19-4d4570852e31)
2. [Data Visualization: Deploying an Interactive Map as a Web App with Heroku](https://medium.com/analytics-vidhya/data-visualization-deploying-an-interactive-map-as-a-web-app-with-heroku-51a323029e4)
3. [How to Develop LSTM Models for Time Series Forecasting](https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/)
4. [Time Series Prediction with LSTM Recurrent Neural Networks in Python with Keras](https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/)
5. [Evaluate the Performance Of Deep Learning Models in Keras](https://machinelearningmastery.com/evaluate-performance-deep-learning-models-keras/)
6. [Multivariate Time Series Forecasting with LSTMs in Keras](https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/)
