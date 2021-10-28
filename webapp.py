import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from streamlit_folium import folium_static
import folium
import geopandas as gp
import pickle
import plotly.express as px
from datetime import datetime, date

# read df from pickle files
cases_malaysia = pickle.load(open('pickle_files/cases_malaysia.pkl', 'rb'))

# read the Malaysia states geojson file
df_map = gp.read_file('msia-states.json')

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
            st.write('No available data')
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
                
    m = folium.Map([4.602973124617278, 108.64564992244625], zoom_start=6)

    # covid-19 cases for each state in Malaysia (dummy number)
    # cases in this order: Johor, Kedah, Kelantan, Kuala Lumpur, Labuan, Melaka, Negeri Sembilan, Pahang, Perak, Perlis, Pulau Pinang, Putrajaya, Sabah, Sarawak, Selangor, Trengganu
    df_map['Cases'] = [1322,3456,2332,3432,2321,2223,6567,6762,5569,3870,9807,3498,5489,9870,10709,7790]
    bins = list(df_map['Cases'].quantile([0, 0.5, 0.75, 0.95, 1]))

    # choropleth of states in Malaysia
    states = folium.Choropleth(
        geo_data=df_map,
        data=df_map,
        key_on='feature.properties.name_1',
        columns=['name_1','Cases'],
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name='Cases',
        bin=bins,
        reset=True,
    ).add_to(m)

    # adding tooltips
    states.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=['name_1', 'Cases'],
                                    aliases=['State: ', 'Cases:'])
    )

    option = st.checkbox('📌Display map (this might take a while)')

    if option:
        # adding map layers
        folium.TileLayer('Stamen Terrain').add_to(m)
        folium.TileLayer('Stamen Toner').add_to(m)
        folium.TileLayer('Stamen Water Color').add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.LayerControl().add_to(m)

        folium_static(m)

        expander = st.beta_expander('💡Tips')
        expander.write('Hover over the states to check out the number of cases!')

    make_map_responsive="""
        <style>
            [title~="st.iframe"] {width: 100%}
        </style>
    """
    st.markdown(make_map_responsive, unsafe_allow_html=True)


def page_clustering():

    st.title('📉 Clustering Analysis')
    st.write('Hi')

def page_regression():

    st.title('📈 Regression Model')
    st.video('https://youtu.be/o-YBDTqX_ZU') 

def page_classification():

    st.title('📊 Classification Model')
    st.write('Hello')


if __name__ == "__main__":
    main()