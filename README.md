# Malaysia COVID-19 Cases and Vaccination

An in-depth extension of our previous [Assignment](https://github.com/BingQuanChua/COVID-19-Msia-Mining).



## 📚Datasets	

Data taken as of **`6-10-2021`** (cut off date)

1. COVID-19 Open Data from the Minister of Health (MoH)
   https://github.com/MoH-Malaysia/covid19-public

2. Vaccination Data from COVID-19 Immunisation Task Force (CITF)
   https://github.com/CITF-Malaysia/citf-public



## 📖Table of Contents

### **Exploratory Data Analysis**

* Analyse which group of population are more vulnerable to COVID cases in Malaysia.
* Analyse how COVID cases vary across time dimensions at different granularity.
* What is the stationarity of the time-series dataset?
* What are the vaccination and registration rates per state in Malaysia?
* What are the types and total number of side effects for each type of vaccine?
* Which type of vaccine is given to more people?
* Which states are recovering? Which of the states shows a decrease in the number of COVID-19 cases?
* When is the time of the day with most MySejahtera check-ins?
* What are the dates with the highest number of checkins? How does it correlate with the number of cases and deaths during the day?
* Rate of Serious Vaccine Side Effect VS COVID Death Rate without obtaining vaccine, which one is more dangerous?

### **Clustering Analysis**  

* How well does each state handle COVID-19 cases based on past COVID-19 cases and deaths records?

### **Regression and Classification** 

* By utilizing the previous COVID-19 records, is it possible to construct a model capable of predicting/classifying the number of cases for the upcoming day or week?

### **Time-series Regression**

* Is it possible for the government to predict the number of daily new cases accurately based on past data in order to deploy appropriate movement control measures?



## 🐱‍💻Deployment

Our results are deployed to Heroku using in the form of a Streamlit webapp.

Check out our page! https://covid-19-msia-cases-and-vax.herokuapp.com/


Screenshots:

<img src="images/page_navigation.gif">

<p align="center"> Fig.1 Navigation </p>

---

<img src="images/page_showcase.gif">

<p align="center"> Fig.2 Clustering Analysis </p>



## 📑References

1. [COVID-19: What Is Hidden Behind the Official Numbers?](https://towardsdatascience.com/which-countries-are-affected-the-most-by-covid-19-4d4570852e31)
2. [Data Visualization: Deploying an Interactive Map as a Web App with Heroku](https://medium.com/analytics-vidhya/data-visualization-deploying-an-interactive-map-as-a-web-app-with-heroku-51a323029e4)
3. [How to Develop LSTM Models for Time Series Forecasting](https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/)
4. [Time Series Prediction with LSTM Recurrent Neural Networks in Python with Keras](https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/)
5. [Evaluate the Performance Of Deep Learning Models in Keras](https://machinelearningmastery.com/evaluate-performance-deep-learning-models-keras/)
6. [Multivariate Time Series Forecasting with LSTMs in Keras](https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/)
