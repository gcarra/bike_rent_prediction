""" This file create the class Displayer 
used by the main file of the streamlit App """

from typing import Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from src.data_preprocessing import cleaning_data, feature_engineering
from src.env import LEGEND_TO_MODIFY, LINE_PLOT_VARS, PLOT_LEGEND_DICT, VAR_DOC
from src.path import DATA_DIR

import streamlit as st


class Displayer:
    """This class allow to define methods to produce plots and filter UI"""

    def __init__(self, path, LINE_PLOT_VARS, PLOT_LEGEND_DICT):

        self.path = path
        self.line_plot_vars = LINE_PLOT_VARS
        self.plot_legend_dict = PLOT_LEGEND_DICT
        self.legend_to_modify = LEGEND_TO_MODIFY

    def load_data(self):
        """
        Load and process data of the Bike Sharing dataset.

        Parameters
        ----------
        None

        Returns
        -------
        data: pd.Dataframe
            The dataframe containing the data loaded
        """
        raw_data = pd.read_csv(self.path)
        cleaned_data = cleaning_data(raw_data, split=False)
        process = feature_engineering()
        data = process.define_exra_features(cleaned_data)
        return data

    def widgets_hour_vs_var(self):
        """
        Widgets associated to the first figure
        Parameters
        ----------
        None

        Returns
        -------
        agg_method: str
            The aggregation methode chose by the user
        var: str
            The variable the user wants to analyse    
        """
        st.markdown(f"### Fig 1. Hourly number of users")
        col1, col2 = st.columns(2)
        agg_method = col1.radio("Aggregation method", ["mean", "median"])
        var = col2.selectbox(
            "Categorical variable to analyse ?",
            self.line_plot_vars,
            index=0,
            placeholder="Select variable",
        )
        return agg_method, var

    def plot_hour_vs_var(self, data, var, agg_method):
        """This function plot the hourly number of user as fonction
        of the hour, for different values of the var variable
        Parameters
        ----------
        data: pd.Dataframe
            Dataset containing data
        var: str
            String containing the variable the user chose to analyse
        agg_method: str
            String containing the method the user chose to aggregate data

        Returns
        -------
        self.fig: figure
        """
        grouped_data = (
            data.groupby(["Hour", var])
            .agg({"count": agg_method})
            .reset_index()
        )
        self.fig = px.line(
            grouped_data,
            x=grouped_data.Hour,
            y="count",
            color= var,
            markers=True,
            labels={"count": f"{agg_method} hourly number of users"},
        )
        if var in self.legend_to_modify:
            for i, new_name in enumerate(self.plot_legend_dict[var]):
                self.fig.data[i].name = new_name
        

    def widgets_var_vs_count(self):
        """Widgets associated to the second figure
        Parameters
        ----------
        None

        Returns
        -------
        agg_method: str
            The aggregation methode chose by the user
        var: str
            The variable the user wants to analyse    
        """
        st.divider()
        st.markdown(f"### Fig. 2 Daily number of users")
        col2_1, col2_2 = st.columns(2)
        agg_method_2 = col2_1.radio(
            "Aggregation method", ["mean", "median"], key="fig2"
        )
        var_2 = col2_2.selectbox(
            "Categorical variable to analyse ?",
            self.line_plot_vars,
            index=0,
            placeholder="Select variable",
            key="Fig2",
        )
        return  var_2, agg_method_2

    def plot_var_vs_count(self, data, var_2, agg_method_2):
        """
        This function shows the daily number of user as fonction
        the variable the user chose
        Parameters
        ----------
        data: pd.Dataframe
        Dataset containing data
        var_2: str
        String containing the variable the user chose to analyse
        agg_method_2: str
        String containing the method the user chose to aggregate data

        Returns
        -------
        self.fig_2: figure
        """
        data_temp = data.copy()
        data_temp["date"] = data_temp["datetime"].dt.date
        grouped_data = (
            data_temp.groupby(["date", var_2]).agg({"count": sum}).reset_index()
        )

        grouped_data = (
            grouped_data.groupby([var_2])
            .agg({"count": agg_method_2})
            .reset_index()
        )

        self.fig_2 = px.bar(grouped_data, x=var_2, y="count")
        self.fig_2.update_layout(
            yaxis_title=f"{agg_method_2} daily number of users",
            xaxis_title=var_2,
        )
        self.fig_2.update_yaxes(type="linear")
        self.fig_2.update_xaxes(type="category")
        self.fig_2.update_layout(height=600)

        if var_2 in self.legend_to_modify:
            for idx in range(len(self.fig_2.data)):
                self.fig_2.data[idx].x = self.plot_legend_dict[var_2]
   

    def widget_filter(self):
        """
        This checkbox allow to select the filter option
        Parameters
        ----------
        None

        Returns
        ----------
        modify: bool
            It says if the filter option has been selected
        """
        with st.sidebar:
            st.markdown("""## FILTERS """)
            modify = st.checkbox("Add filters to the dataframe")
        return modify

    def filter_dataframe(self, data, modify):
        """
        Allowing users to filter columns

        Parameters:
            data: pd.DataFrame
                Original dataframe
            modify: bool
                It says if the filter option has been selected

        Returns:
            pd.DataFrame: Filtered dataframe
        """

        with st.sidebar:
            if modify:
                
                to_filter_columns = st.multiselect(
                    "Filter data table on", data.columns
                )
                for column in to_filter_columns:
                    left, right = st.columns((1, 20))
                    left.write("↳")
                    # Treat columns with < 10 unique values as categorical
                    if data[column].nunique() < 13:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            data[column].unique(),
                            default=list(data[column].unique()),
                        )
                        self.filter_data = data[
                            data[column].isin(user_cat_input)
                        ]
                    elif is_numeric_dtype(data[column]):
                        _min = float(data[column].min())
                        _max = float(data[column].max())
                        step = (_max - _min) / 100
                        user_num_input = right.slider(
                            f"Values for {column}",
                            min_value=_min,
                            max_value=_max,
                            value=(_min, _max),
                            step=step,
                        )
                        self.filter_data = data[
                            data[column].between(*user_num_input)
                        ]
                    elif is_datetime64_any_dtype(data[column]):
                        user_date_input = right.date_input(
                            f"Values for {column}",
                            value=(
                                data[column].min(),
                                data[column].max(),
                            ),
                        )
                        if len(user_date_input) == 2:
                            user_date_input = tuple(
                                map(pd.to_datetime, user_date_input)
                            )
                            start_date, end_date = user_date_input
                            self.filter_data = data.loc[
                                data[column].between(start_date, end_date)
                            ]
                    else:
                        user_text_input = right.text_input(
                            f"Substring or value in {column}",
                        )
                        if user_text_input:
                            self.filter_data = data[
                                data[column]
                                .astype(str)
                                .str.contains(user_text_input)
                            ]
