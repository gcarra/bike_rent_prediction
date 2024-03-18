""" This file create a simple EDA app"""
import streamlit as st
from src.path import DATA_DIR
import duckdb
from src.plots import *
import pandas as pd
from src.env import LINE_PLOT_VARS

from src.data_preprocessing import cleaning_data, feature_engineering

raw_data = pd.read_csv(DATA_DIR / "raw_data.csv")  

cleaned_data = cleaning_data(raw_data, split = False)
data = feature_engineering(cleaned_data, cyclical_values = False, drop_cols = False)
#data["datetime"] = data["datetime"].dt.tz_localize(None)

st.set_page_config(layout="wide")


# title
st.title(f'Bike sharing demand ')
st.header('An exploratory data analysis tool')

####

st.dataframe(filter_dataframe(data))

#####
sql_query = st.text_area(label = "Write a SQL query. The table name is: data")
tab1, tab2 = st.tabs(["'data' table", "queried table"])
with tab1 :
    st.dataframe(data,
                column_config={
    "Year": st.column_config.NumberColumn(
        help="Number of stars on GitHub",
        format="%d"),
    "holiday": st.column_config.CheckboxColumn(
        help="It indicates whether the day is a school holiday"),
    "season": st.column_config.NumberColumn(
        help="1 = Spring,  2 = Summer, 3 = Autumn, 4 = Winter"),
    "weather": st.column_config.NumberColumn(
        help= " 1 = Clear to cloudy, 2 = Foggy, 3 = Light rain or snow, 4 = Heavy showers or snow"
                   ),
    "temp": st.column_config.NumberColumn(
        help="Temperature in Celsius"),   
    "atemp": st.column_config.NumberColumn(
        help="Feeling temperature in Celsius"),
    "casual": st.column_config.NumberColumn(
        help="Count of casual users"),   
    "registered": st.column_config.NumberColumn(
        help="Count of registered users"),
    "count": st.column_config.NumberColumn(
        help="Hourly number of users"),
    "Weekday": st.column_config.NumberColumn(
        help="0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday, 5 = Saturday, 6 = Sunday")
                },
    hide_index=True
    )
with tab2:
    try:
        result = duckdb.query(sql_query).df()
        st.dataframe(result)
    except:
        st.write("The SQL query is empty or incorrect")

####
with st.sidebar:
    option = st.selectbox(
        "Variable would you lke to analyse ?",
        data.drop(columns = ["Hour", "count"], axis = 1).columns,
        index = None,
        placeholder="Select variable"
    )


st.divider()
st.markdown(f"### Fig 1. Hourly number of users") 
col1, col2 = st.columns(2)
selected_agg = col1.radio("Aggregation method", ["mean", "median"])
var = col2.selectbox(
        "Categorical variable to analyse ?",
        LINE_PLOT_VARS,
        index = 0,
        placeholder="Select variable")


with st.spinner(text="Plotting data"):   
    
    fig = plot_hour_vs_var(data, var, agg_method = selected_agg )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)
