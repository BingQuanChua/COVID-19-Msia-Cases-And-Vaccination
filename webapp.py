import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import pickle
import plotly.express as px
from datetime import datetime, date
from PIL import Image

# read df from pickle files
cases_malaysia = pickle.load(open('pickle_files/cases_malaysia.pkl', 'rb'))

# read the Malaysia states geojson file
df_map = pd.read_csv('map/map.csv')

st.set_page_config(layout="wide")


def main():

    # Sidebar
    st.sidebar.title("Malaysia COVID-19 Cases and Vaccination")
    st.sidebar.write('''
        presented by:  
        Chua Bing Quan  
        Liew Kuan Yung  
        Soh Jing Guan  

        ---
    ''')
    st.sidebar.subheader("🧭Navigation")
    choice = st.sidebar.radio("go to", ('Exploratory Data Analaysis', 'Clustering Analysis',
                              'Regression', 'Classification', 'Time-Series Regression'), index=0)

    if choice == 'Exploratory Data Analaysis':
        page_eda()
    elif choice == 'Clustering Analysis':
        page_clustering()
    elif choice == 'Regression':
        page_regression()
    elif choice == 'Classification':
        page_classification()
    elif choice == 'Time-Series Regression':
        page_time_series_regression()


def page_dashboard():

    st.title("Malaysia COVID-19 Cases and Vaccination")
    st.write("## **Daily Recorded Cases in Malaysia**")
    fig = px.line(cases_malaysia, x='date', y=['cases_new', 'cases_recovered'],
                  title='Daily report COVID cases and cases recovered in Malaysia')
    st.plotly_chart(fig, use_container_width=True)

    st.write('')
    st.write('---')

    st.write('## **Select a Data Range**')
    st.write('The recorded data starts from `2020-01-25` to `2021-10-05`. Any dates selected out of this range will not be shown.')
    cases_malaysia['date'] = cases_malaysia['date'].astype('datetime64[ns]')
    date_range = st.date_input(
        "Pick a date", (cases_malaysia.date.min(), cases_malaysia.date.max()))

    if len(date_range) == 2:  # when 2 dates are selected
        first_date = datetime.combine(date_range[0], datetime.min.time())
        second_date = datetime.combine(date_range[1], datetime.min.time())

        filtered_cases_malaysia = cases_malaysia[(
            cases_malaysia['date'] >= first_date) & (cases_malaysia['date'] <= second_date)]

        if len(filtered_cases_malaysia) == 0:
            st.error('No available data! Please select another set of date range.')
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.write('## **Data Frame**')
                st.write(filtered_cases_malaysia)

            with col2:
                st.write('## **Same Bar Plot**')
                fig = px.line(filtered_cases_malaysia, x='date', y=['cases_new', 'cases_recovered'],
                              title='Daily report COVID cases and cases recovered in Malaysia')
                st.plotly_chart(fig, use_container_width=True)


def page_eda():
    st.title('🔎Exploratory Data Analaysis')

    st.subheader('EDA 1: Analyse which group of population are more vulnerable to covid cases in Malaysia.')
    
    st.subheader('EDA 2: Analyse how covid cases vary across time dimensions at different granularity.')

    st.subheader('EDA 3: What is the stationarity of the time-series dataset?')

    st.subheader('EDA 4: What are the vaccination and registration rates per state in Malaysia?')

    st.subheader('EDA 5: What are the types and total number of side effects for each type of vaccine?')

    st.subheader('EDA 6: Which type of vaccine is given to more people?')

    with st.expander('EDA 7 - Which states are recovering? Which of the states shows a decrease in the number of COVID-19 cases?'):
        st.subheader('Which states are recovering? Which of the states shows a decrease in the number of COVID-19 cases?')
        st.markdown('''
            Since the number of vaccinated entities are increasing, there is a significant decrease in the number of COVID-19 cases in each state. By plotting the moving average of daily confirmed cases and the cumulative number of vaccinated persons against the dates, we can observe that there is a downward trend after the vaccination has reached a certain level in each of the states. The moving average of daily cases is obtained by averaging the number of daily cases in the past 7 days. 

            To calculate the daily cumulative number of vaccinated persons, we start by calculating the number of people who completed their vaccination dose. This includes adding the 

            * daily number of adults who has completed their 2nd dose of vaccine (either Pfizer, Sinovac or Astra)
            * daily number of adults who has taken Cansino (since Cansino only requires 1 dose)
            * daily number of children who complete their 2nd dose of Pfizer

            These numbers are accumulated to obtain the daily cumulative number of vaccinated persons.    
        ''')

        for i in range(16):
            im = Image.open('images/EDA07_{:02d}.png'.format(i+1))
            st.image(im)

        st.write('It is observed that the number of vaccinated people in some states has exceeded their state population. The two states that have this phenomena are Kuala Lumpur and Putrajaya. This might be due to foreigners receiving their vaccination shot in our country.')


    with st.expander('EDA 8 - When is the time of the day with most MySejahtera check-ins?'):
        st.subheader('When is the time of the day with most MySejahtera check-ins?')
        st.markdown('''
            checkin_malaysia_time.csv records the time distribution of daily check-ins on MySejahtera at the country level. The data records the number of check-ins nationwide in every 30 minutes interval.

            By summing up each column in the dataset, we can obtain the total number of check-ins at each 30 minutes between 2020-12-01 to 2021-10-05, spanning over 309 days.
        ''')
        im = Image.open('images/EDA08_1.png')
        st.image(im, caption='Total number of check-ins from MySejahtera data')
        st.write('From the plot above, we can roughly observe 3 peaks, which are around 8am, 12pm, and 6pm respectively. Presumably these are the preferred hours for Malaysians to buy their meals.')


    with st.expander('EDA 9 - What are the dates with the highest number of checkins? How does it correlate with the number of cases and deaths during the day?'):
        st.subheader('What are the dates with the highest number of checkins? How does it correlate with the number of cases and deaths during the day?')
        im = Image.open('images/EDA09_1.png')
        st.image(im, caption='Daily number of confirmed cases, deaths, and check-ins')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('''
                The date with the highest number of checkins between 2020-12-01 and 2021-10-02 is 2021-04-03 (the 3rd of April 2021). On that day, the number of cases and deaths are considerably low. 
                
                In order to visualize the correlation between the daily number of cases and deaths with the daily number of check-ins, we have plotted a heatmap among these 3 attributes. 
                
                The heatmap shows that there is almost no correlation between them.
            ''')
        with col2:
            im = Image.open('images/EDA09_2.png')
            st.image(im, caption='Correlation heatmap')


    with st.expander('EDA 10 - Rate of Serious Vaccine Side Effect  VS Covid Death Rate without obtaining vaccine, which one is more dangerous?'):
        st.subheader('Rate of Serious Vaccine Side Effect  VS Covid Death Rate without obtaining vaccine, which one is more dangerous?')
        st.markdown('''
            Some people refuse to obtain vaccines because they think vaccines are dangerous and high risk. In this question, we will measure the rate of serious side effects of vaccination and covid death rate if without obtaining a vaccine to evaluate whether reducing it is a good choice or not. 
            
            We divide the total number of covid deaths without obtaining a vaccine and divide with the total number of people without obtaining a vaccine then multiply with 100 to obtain the rate of covid death without obtaining the vaccine. Besides, we sum out the number of serious side effect cases and divide the total number of people obtaining the vaccine then multiply it to 100 to obtain the rate of the serious side effect. We use both rates to multiply 1000 to obtain the number of death or serious side effects cases for every 1000 people. The figure above shows the results of the measures. As we can see, for every 1000 people, about 200 people without obtaining a vaccine will die because of covid. But only about 2 people may get a serious vaccine side effect for every 1000 people. 
        ''')
        col1, col2 = st.columns(2)
        with col1:
            im = Image.open('images/EDA10_1.png')
            st.image(im, caption='Number of cases and serious side effect of vaccine amoung 1000 people')
        with col2:
            im = Image.open('images/EDA10_2.png')
            st.image(im, caption='Raio of serious side effect in ratio of number of people not obtain vaccine and dead because of COVID (among 1000 people)')


        st.markdown('''
            The result at the left is evidence to show it is more dangerous if you do not obtain any vaccine. The figure  at the right shows the ratio of serious vaccine side effect cases in the number of covid deaths without obtaining any vaccine for every 1000 people. We can find a ratio of serious vaccine side effects not greater than 1%. So that, in a nutshell, obtaining a vaccine is a safer and smart decision to protect your life. 
        ''')


def page_clustering():

    st.title('🧩Clustering Analysis')
    st.write('## **How well does each state handle COVID-19 cases based on past COVID-19 cases and deaths records?**')
    st.markdown('''
        To evaluate how well each state handles COVID-19 cases, we would like to perform time-series clustering to divide each state into different clusters based on their daily cases and deaths to analyze or discover the pattern or characteristics of each state. Time series k mean from `tslearn` library will be used to perform time-series clustering. 
        
        Before we start clustering the states, the number of daily cases and deaths of each state have been normalized by their state’s population and 3 clusters have been chosen (refer to our code for more) for the time series k means.

        Select a parameter for clustering:
    ''')

    df_map.cluster_cases = df_map.cluster_cases.astype('string')
    df_map.cluster_deaths = df_map.cluster_deaths.astype('string')
    
    cluster = st.selectbox('Clustering based on:', ['Daily COVID-19 Cases', 'Daily Number of Deaths'])

    if cluster == 'Daily COVID-19 Cases':
        cluster_attr = 'cluster_cases'
    else:
        cluster_attr='cluster_deaths'
    
    fig = px.scatter_mapbox(df_map, lat="lat", lon="lon", hover_name='state', 
        hover_data=["population"], color=cluster_attr,
        center={
            'lat': 4.0,
            'lon': 108.25
        }, 
        zoom=4.8, height=600,
        mapbox_style="carto-darkmatter",
        title=f"Clustering Malaysia states based on {cluster}",
        category_orders={cluster_attr: ['0', '1', '2']}
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        
        if cluster == 'Daily COVID-19 Cases':
            st.subheader('Clustering each states into 3 clusters according to daily cases')
            im = Image.open('images/CTR_1.png')
            st.image(im,width=600, caption='Dividing each states into different clusters according to cases')
        else:
            st.subheader('Clustering each states into 3 clusters according to daily deaths')
            im = Image.open('images/CTR_2.png')
            st.image(im,width=600, caption='Dividing each states into different clusters according to deaths')

    with col2:
        st.subheader('States and their clusters')
        st.write(df_map[['state', cluster_attr]])

    st.write('') 
    st.write('')
    st.write('')
    
    if cluster == 'Daily COVID-19 Cases':
        st.markdown('''
            The figure above shows the results of clustering according to the daily_cases. There is 1 state cluster as red clusters. Which is Labuan. The trends of daily cases slightly increase between 2020 October to 2021 March and significantly increase when 2021 June. In 2021 July, the cases start decreasing.  

            Next, there are 4 states as green clusters. Which are Kuala Lumpur, Melaka, Selangor and Negeri Sembilan. The cases of these states are quite stable until 2021 Jun, the cases start increasing until 2021 July, then cases decrease. 

            Lastly, 11 states are red clusters. The trends of cases for these states are also similar to states as green clusters, but the number of cases increases a little bit higher than states in green clusters.

            According to the result of clustering, except Labuan, before June 2021, each of the state's daily cases could be considered stable, most of the states were able to control the daily cases well. But in  June 2021, the cases for each state kept increasing, especially Labuan, whose cases have significantly increased if compared with other states. We can consider that during that period, Labuan was out of control in daily cases. But fortunately, after only about 1 month, Labuan cases have been under control, the cases start decreasing and during that period, other states' daily cases still keep increasing until September then start decreasing. In conclusion, some investigation on Labuan in handling covid cases should be considered especially in Jun 2021 since that time performs a very significant increase of cases which can’t be observed in other states. Besides, states in green clusters and states in red clusters have similar patterns but states in green clusters cases are less than the states in red clusters, which may handle the daily cases better if compared with those states in red or red clusters.
        ''')
    else:
        st.markdown('''
            The figure above shows the states clustering based on daily deaths cases. As we can see there is one state as a red cluster. The deaths slightly increase from September 2020 to March 2021 and a significant increase in deaths cases in June 2021. Besides, there are four states as green clusters, which are Kuala Lumpur, Melaka, Selangor, and Negeri Sembilan again. The death cases in green clusters keep increasing more rapidly if compared with states in blue clusters from June to September 2021. Furthermore, states in blue clusters perform more stable trends of death cases if compared with another two clusters. 

            According to this figure, we can conclude that Labuan is not doing well in handling covid cases. In both figures, it performed a very significant increase in June 2021, and from November to March 2021, it also slightly increased its death cases but other states didn’t have the same problems. For states in the blue cluster, although their daily cases are slightly higher than states in the green cluster, their death cases are much more stable if compared with states in the green cluster. So, states in the blue cluster perform better in handling covid cases and problems.       
        ''')

    st.write('') 
    st.write('')
    st.write('')

    with st.beta_expander('Tips'):
        st.write('Select clustering based on a differnt parameter above to get more results.')

        
def page_regression():

    st.title('📈Regression Models')
    st.write('''In short, this section explains how we use historical cases data (data from past 7 days) to predict cases 
    moving average for tomorrow or next week using [supervised learning for time series forecasting](https://machinelearningmastery.com/time-series-forecasting-supervised-learning/).''')
    st.write('## Data Preprocessing')
    st.write(''' Firstly, The data is first being preprocessed and merged data from cases, tests, deaths, and vaccination. The date stamps are 
    2020-01-31 to 2021-10-02, 611 rows in total. The NaN is filled with 0 because deaths and vaccination only started at 
    some point and hence they are not an error or outlier. Then we calculate the next day’s moving average “ma7_next_day" 
    attribute using a sliding window calculation and [sample-bin them using the median](https://towardsdatascience.com/data-preprocessing-with-python-pandas-part-5-binning-c5bd5fd1b950) 
    for classification later.''')

    X_train = pickle.load(open('pickle_files/classification_X_train.pkl', 'rb'))
    y_train = pickle.load(open('pickle_files/classification_y_train.pkl', 'rb'))
    
    st.write('### X train, dimensions')
    st.write(X_train.head())
    st.write('### y train, to be predicticted')
    st.write('Binned moving average of next day')
    st.write(y_train.head())
    st.write('Another worth mentioning part is the y train is being binned using median sample bin. This')
    
    col1, col2 = st.columns((5,5))
    im1 = Image.open('images/DM_class_reg_data_median_bin.png')
    col1.image(im1,width=400, caption='5 equally distributed median')
    im2 = Image.open('images/DM_class_reg_data_median_bin2.png')
    col2.image(im2,width=400, caption='Sample bin median')

    st.write('### Feature Importance')
    col1, col2, col3 = st.columns(3)
    im = Image.open('images/DM_class_reg_heatmap.png')
    col1.image(im,width=500, caption='Heatmap for All Features')
    im = Image.open('images/DM_class_reg_SHAP1.png')
    col2.image(im,width=500, caption='Heatmap for All Features')
    im = Image.open('images/DM_class_reg_SHAP2.png')
    col3.image(im,width=500, caption='Heatmap for All Features')

    st.markdown('''
    #### Regression Models

    Regression models that will be used:\n
    1. Linear Regression
    2. Decision Tree Regressor
    3. Random Forest Regressor
    4. Support Vector Regressor

    Evaluation matrics that will be used:\n
    1. R Square
    2. Mean Absolute Error(MAE)
    3. Root Mean Square Error(RMSE)
    ''')

    st.write('''
    EXample for Support Vector Regressor\n
    ```
    reg_sv = SVR(kernel='linear')\n
    reg_sv = reg_sv.fit(X_train, np.ravel(y_train))\n
    y_pred = reg_sv.predict(X_test)
    ```
    ''')

    st.markdown('''
    #### Results
    |                               | Linear Regression | Decision Tree | Random Forest | SVR       |
    | ----------------------------- | ----------------- | ------------- | ------------- | --------- |
    | R Square                      | 0.89642           | 0.98097       | 0.93570       | 0.88917   |
    | Mean Absolute Error (MAE)     | 0.40572           | 0.04065       | 0.03211       | 0.39836   |
    | Root Mean Square Error (RMSE) | 0.47043           | 0.20162       | 0.14114       | 0.48661   |
    ''')

    st.write('''
    .\n\n
    #### Conclusion
    An interesting observation is that Random Forest and Decision Tree both perform better than SVR and Linear Regressor.
    We decude the reason behind is because both RF and DT supports non linearity better and the nature of the dataset is 
    non linear as well.
    ''')
    
def page_classification():

    st.title('📊Classification')
    st.write('''
    This is the continuation of Regression usign similar [dataset](#data-preprocessing). A gentle reminder, do visit 
    regression page before diving into this classification section.
    ''')

    st.write('''
    ### Classification Models

    Classification models that will be used:\n
    1. K-Nearest Neighbors Classifier
    2. Naive Bayes Classifier
    3. Decision Tree Classifier
    4. Random Forest Classifier

    Performance evaluation metrics that will be used:\n
    1. Confusion Matrix
    2. Precision, Recall, F1-score
    3. ROC Curve
    ''')

    st.write('### Model Accuracy')
    st.write('''
    |                        | KNN       | GaussianNB  | Decision Tree | Random Forest | SVC      |
    | ---------------------- | ----------| ------------| ------------- | ------------- | -------- |
    | Test Set Accuracy      | 0.94309   | 0.95122     | 0.95935       | 0.95935       | 0.78049  |
    ''')

    st.write('### Confusion Matrix')
    im = Image.open('images/DM_class_reg_confusionMatrix.png')
    st.image(im,width=800, caption='Confusion Matrix')
    im = Image.open('images/DM_class_reg_confusionMatrix2.png')
    st.image(im,width=800, caption='Confusion Matrix')

    st.write('### Precision & Recall')
    im = Image.open('images/DM_class_reg_ROC1.png')
    st.image(im,width=800, caption='F1-Score')
    im = Image.open('images/DM_class_reg_ROC2.png')
    st.image(im,width=800, caption='F1-Score')


def page_time_series_regression():

    st.title('⏳Time-Series Regression')
    st.write('## **Is it possible for the government to predict the number of daily new cases accurately based on past data in order to deploy appropriate movement control measures?**')
    st.markdown('''
        With an accurate forecast of the daily new cases, the government would be able to control the vaccination rate to tackle the pandemic effectively. We have implemented a time-series regression to forecast the number of COVID-19 cases in Malaysia. Two LSTM-based RNN is built to aid us in this problem.
    ''')
    
    ### model 1
    st.subheader('LSTM-based RNN')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            The first time-series regression model is a single variate LSTM-based RNN model. The number of daily cases is separated into a train and test set on 2021-07-01. The training set has a total of 523 days and the test set has a total of 97 days.

            A 5 layer LSTM-based RNN with a total of 71,051 trainable parameters has been implemented. Each layer apart from the dense layer has 50 units and a dropout rate of 0.2. After training the model, we used it to predict the test set. The model failed to predict the trend of the daily cases as shown below. The results have a root mean square error of 7740.403.

            | Evaluation                    | LSTM-Based RNN |
            | ----------------------------- | -------------- |
            | Root Mean Square Error (RMSE) | 7740.403       |
        ''')
    with col2:
        im = Image.open('images/LSTM_1.png')
        st.image(im,width=500, caption='Actual and Predicted results for COVID-19 Cases')

    ### model 2
    st.subheader('Multivariate LSTM-based RNN')
    st.markdown('''
        Our second time-series regression model is a multivariate LSTM-based regression. We have plenty of datasets that might have an impact on the number of daily COVID-19 cases. These datasets are cases_malaysia, test_malaysia, deaths_malaysia, checkin_malaysia, vax_malaysia, and vaxreg_malaysia which records the cases, tests, deaths, check-ins, vaccination and registration data in Malaysia.

        A simple feature selection was used to retrieve the attributes with higher correlation to the number of daily cases. We have generated heatmaps to visualize the correlationship of each attribute with `cases_new` (daily COVID cases). Before that, we will be merging a few datasets together. Since tests_malaysia, deaths_malaysia, and checkin_malaysia have a similar time range, we will merge them together along with cases_malaysia. On the other hand, vax_malaysia and vaxreg_malaysia have a relatively shorter time range. Hence, we will merge them with the `cases_new` column separately in another DataFrame.

        After observing the correlationship between `cases_new` and other attributes from various datasets (cases_malaysia, tests_malaysia, deaths_malaysia, checkin_malaysia, vax_malaysia and vaxreg_malaysia). We found that the features with higher correlation (>= 0.9 positively or negatively) are:
    ''')

    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown('''
            `cases_recovered`,  
            `cases_active`,  
            `cases_pvax`,  
            `cases_child`,  
            `cases_adolescent`,  
            `cases_adult`,  
            `cases_elderly`,  
            `deaths_new`,  
            `deaths_new_dod`, and  
            `deaths_bid_dod`.
        ''')
    with col2:
        im = Image.open('images/LSTM_2.png')
        st.image(im,width=500, caption='Using Heatmap for Feature Selection')


    st.markdown('''
        The resulting dataset has 568 days of data. Similar to the above, we implemented a 5 layer LSTM-based RNN with a total of 73,051 trainable parameters. A lookback of 30 days is used to create our dataset, resulting in 538 days of data. We then get the last 50 days for prediction and the rest of the days for training and validation. The model came to an early stopping at 16 epoch after training and validation data were fed to it.

        After the training, we test our model by predicting the test data. The results show that the model is able to capture the overall downward trend of the number of daily cases in Malaysia but failed to capture the ups and downs in the details. The model has a root mean square error of 1640.952, which is an improvement from the previous model.

        | Evaluation                    | Multivariate LSTM-Based RNN |
        | ----------------------------- | --------------------------- |
        | Root Mean Square Error (RMSE) | 1640.952                    |


    ''')
    st.write('') 
    st.write('')
    st.write('')
    
    im = Image.open('images/LSTM_3.png')
    st.image(im,width=900, caption='Actual and Predicted results for COVID-19 Cases using Multivariate LSTMnet')
    
    st.write('---')
    st.subheader('Stationary Time-Series and Non-stationary Time-Series')
    st.markdown('''
        We learnt that time-series data can be categorized into stationary and non-stationary. Stationary time-series data tends to be more predictable as the mean and variance normally remains constant and does not possess any trends or seasonality. On the other hand, non-stationary data are considered harder to predict as it is the opposite of stationary data. Other time series regression models such as the ARIMA model perform better forecasts with stationary time-series data. 

        The daily number of COVID-19 cases in Malaysia is a non-stationary time-series data, hence the prediction results are not accurate.    
    ''')

    im = Image.open('images/LSTM_5.png')
    st.image(im,width=1000, caption='Stationary Time-Series and Non-stationary Time-Series')

    st.markdown('''
        References:

        1. [Stationarity in Time Series Analysis Explained using Python](https://blog.quantinsti.com/stationarity/)
        2. [Time Series Analysis using ARIMA and LSTM(in Python and Keras)](https://medium.com/analytics-vidhya/time-series-analysis-using-arima-and-lstm-in-python-and-keras-part1-f987e11f9f8c)    
    ''')


if __name__ == "__main__":
    main()
