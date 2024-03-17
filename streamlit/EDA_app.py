""" This file create a simple EDA app"""
import streamlit as st
from src.path import DATA_DIR
import duckdb
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
        "Which variable would you like to analyse ?",
        ("Weekday", "holiday", "year"),
        index = None,
        placeholder="Select variable"
    )


with st.spinner(text="Plotting data"):
   
   


    

    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)
        
    progress_bar.progress(6/N_STEPS)
