""" This file create a simple EDA app"""
import streamlit as st
from src.path import DATA_DIR
import duckdb
from src.plots import *
import pandas as pd
from src.data_preprocessing import cleaning_data, feature_engineering

raw_data = pd.read_csv(DATA_DIR / "raw_data.csv")  

cleaned_data = cleaning_data(raw_data, split = False)
data = feature_engineering(cleaned_data, cyclical_values = False, drop_cols = False)
print(data['Year'])

st.set_page_config(layout="wide")

# title
st.title(f'Bike sharing demand ')
st.header('An exploratory data analysis tool')

#####
sql_query = st.text_area(label = "Write a SQL query. The table name is: data")
tab1, tab2 = st.tabs(["'data' table", "queried table"])
with tab1 :
        st.write(data)
with tab2:
    try:
        result = duckdb.query(sql_query).df()
        st.write(result)
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

col1, col2 = st.columns(2)
selected_agg = col1.radio("Aggregation method", ["mean", "median"])
var = col2.selectbox(
        "Variable to analyse ?",
        data.drop(columns = ["Hour", "count", "datetime"], axis = 1).columns,
        index = 0,
        placeholder="Select variable")



with st.spinner(text="Plotting data"):
    fig = plot_hour_vs_var(data, var, agg_method = selected_agg )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)
