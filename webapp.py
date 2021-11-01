import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
# from streamlit_folium import folium_static
# import folium
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
    st.sidebar.header("🧭Navigation")
    choice = st.sidebar.radio("go to", ('Dashboard', 'Clustering Analysis',
                              'Regression', 'Classification', 'Time-Series Regression'), index=0)

    if choice == 'Dashboard':
        page_dashboard()
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

    st.write('''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. 
    Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, 
    pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, 
    vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede 
    mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. 
    Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, 
    feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies 
    nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget 
    condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, 
    luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero 
    venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris 
    sit amet nibh. Donec sodales sagittis magna.''')
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
            col1, col2 = st.beta_columns(2)

            with col1:
                st.write('## **Data Frame**')
                st.write(filtered_cases_malaysia)

            with col2:
                st.write('## **Same Bar Plot**')
                fig = px.line(filtered_cases_malaysia, x='date', y=['cases_new', 'cases_recovered'],
                              title='Daily report COVID cases and cases recovered in Malaysia')
                st.plotly_chart(fig, use_container_width=True)


def page_clustering():

    st.title('🧩Clustering Analysis')
    st.write('## **How well does each state handle COVID-19 cases based on past COVID-19 cases and deaths records?**')

    df_map.cluster_cases = df_map.cluster_cases.astype('string')
    df_map.cluster_deaths = df_map.cluster_deaths.astype('string')

    cluster = st.selectbox("Clustering based on:", [
                           'Daily COVID-19 Cases', 'Daily Number of Deaths'])

    if cluster == 'Daily COVID-19 Cases':
        cluster_attr = 'cluster_cases'
    else:
        cluster_attr = 'cluster_deaths'

    fig = px.scatter_mapbox(df_map, lat="lat", lon="lon", hover_name='state',
                            hover_data=["population"], color=cluster_attr,
                            center={
                                'lat': 4.0,
                                'lon': 108.25
                            },
                            zoom=4.8, height=600,
                            mapbox_style="carto-darkmatter",
                            title=f"Clustering Malaysia states based on {cluster}")

    st.plotly_chart(fig, use_container_width=True)
    st.write(df_map)


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
    #### Conclution
    An interesting observation is that Random Forest and Decision Tree both perform better than SVR and Linear Regressor.
    We decude the reason behind is because both RF and DT supports non linearity better and the nature of the dataset is 
    non linear as well.
    ''')
    
def page_classification():

    st.title('📊Classification Models')
    st.write('Hello')


def page_time_series_regression():

    st.title('⏳Time-Series Regression')
    st.write('## **Is it possible for the government to predict the number of daily new cases accurately based on past data in order to deploy appropriate movement control measures?**')
    st.markdown('''
    
    With an accurate forecast of the daily new cases, the government would be able to control the vaccination rate to tackle the pandemic effectively. We have implemented a time-series regression to forecast the number of COVID-19 cases in Malaysia. Two LSTM-based RNN is built to aid us in this problem.

    ''')
    st.subheader('LSTM-based RNN ')


if __name__ == "__main__":
    main()
