import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from streamlit_folium import folium_static
import folium
import pickle
import plotly.express as px
from datetime import datetime, date

# read df from pickle files
cases_malaysia = pickle.load(open('pickle_files/cases_malaysia.pkl', 'rb'))

# read the Malaysia states geojson file
df_map = pd.read_csv('map/map.csv')

st.set_page_config(layout="wide")

def main():

    # Sidebar
    st.sidebar.header("🧭Navigation")
    choice = st.sidebar.radio("go to", ('Dashboard', 'Clustering Analysis', 'Regression', 'Classification'), index=0)

    if choice == 'Dashboard':
        page_dashboard()
    elif choice == 'Clustering Analysis':
        page_clustering()
    elif choice == 'Regression':
        page_regression()
    elif choice == 'Classification':
        page_classification()



def page_dashboard():

    st.title("Malaysia COVID-19 Cases and Vaccination")
    st.write("## **Daily Recorded Cases in Malaysia**")
    fig = px.line(cases_malaysia, x='date', y=['cases_new', 'cases_recovered'],
            title='Daily report COVID cases and cases recovered in Malaysia')
    st.plotly_chart(fig, use_container_width=True)

    st.write('Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna.')
    st.write('---')

    st.write('## **Select a Data Range**')
    st.write('The recorded data starts from `2020-01-25` to `2021-10-05`. Any dates selected out of this range will not be shown.')
    cases_malaysia['date'] = cases_malaysia['date'].astype('datetime64[ns]')
    date_range = st.date_input("Pick a date", (cases_malaysia.date.min(), cases_malaysia.date.max()))

    if len(date_range) == 2: # when 2 dates are selected
        first_date = datetime.combine(date_range[0], datetime.min.time())
        second_date = datetime.combine(date_range[1], datetime.min.time())

        filtered_cases_malaysia = cases_malaysia[(cases_malaysia['date'] >= first_date) & (cases_malaysia['date'] <= second_date)]

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
    
    cluster = st.selectbox("Clustering based on:", ['Daily COVID-19 Cases', 'Daily Number of Deaths'])

    if cluster == 'Daily COVID-19 Cases':
        cluster_attr='cluster_cases'
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
                        title=f"Clustering Malaysia states based on {cluster}")

    st.plotly_chart(fig, use_container_width=True)
    st.write(df_map)


def page_regression():

    st.title('📈Regression Model')
    st.video('https://youtu.be/o-YBDTqX_ZU') 

def page_classification():

    st.title('📊Classification Model')
    st.write('Hello')


if __name__ == "__main__":
    main()