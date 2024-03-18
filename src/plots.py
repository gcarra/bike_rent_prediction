""" """

import plotly.express as px
import pandas as pd
from typing import Tuple
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
import streamlit as st
import plotly.graph_objects as go
from src.env import LEGEND_TO_MODIFY, PLOT_LEGEND_DICT
var = "Day"
# ## Feature "Hour" for each day
# # For each day of the week plot average count as function of the hour
# def plot_hour_vs_var(var: str) :
#     f, ax = plt.subplots(figsize=(12, 8))
#     df_plot = pd.DataFrame(data.groupby(['Hour',var],sort=True)['count'].mean()).reset_index()
#     sns.pointplot(x=data['Hour'], y=data['count'],hue = data[var], data=data, join=True, legend_out = True)
#     ax.set(xlabel='Hour', ylabel='Number of users')
#     leg_handles = ax.get_legend_handles_labels()[0]
#     ax.legend(leg_handles,  ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'])
#     return f



def plot_hour_vs_var(data, var, agg_method = "median"):

   #     self = _self

    print("Creating plot 1...") # modify with spinner
    grouped_data = data.groupby(["Hour", var]).agg({
        "count": agg_method
    }).reset_index()   
    fig = px.line(grouped_data, x=grouped_data.Hour, y='count', color=var, 
                markers=True, labels={'count':f'{agg_method} hourly number of users'})
    if var in LEGEND_TO_MODIFY:
        for i, new_name in enumerate(PLOT_LEGEND_DICT[var]):
            fig.data[i].name = new_name

    return fig


def plot_var_vs_count(data, var, agg_method = "median"):

    data_temp = data.copy()
    data_temp['date'] = data_temp['datetime'].dt.date
    grouped_data = data_temp.groupby(["date", var]).agg({
        "count": sum
    }).reset_index() 

    grouped_data = grouped_data.groupby([var]).agg({
        "count": agg_method
    }).reset_index()   

    fig = px.bar(grouped_data, x=var, y='count')
    fig.update_layout(yaxis_title=f'{agg_method} daily number of users', xaxis_title= var)
    fig.update_yaxes(type='linear')
    fig.update_xaxes(type='category')
    fig.update_layout(height=600)
          
        
    if var in LEGEND_TO_MODIFY:
        for idx in range(len(fig.data)):
            fig.data[idx].x = PLOT_LEGEND_DICT[var]

    return fig


def filter_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, bool]:
    """
    Allowing users to filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
   

    
    df = df.copy()


    with st.sidebar :
        st.markdown("""## FILTERS """ )
        modify = st.checkbox("Add filters to the dataframe")
        if not modify:
            return df, modify
        to_filter_columns = st.multiselect("Filter data table on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if df[column].nunique() < 13:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]) :
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or value in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df, modify