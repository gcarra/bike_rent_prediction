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

    def __init__(self, DATA_DIR, LINE_PLOT_VARS, PLOT_LEGEND_DICT):

        self.path = DATA_DIR / "raw_data.csv"
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
        self.data: pd.Dataframe
            The dataframe containing the data loaded
        """
        raw_data = pd.read_csv(self.path)
        cleaned_data = cleaning_data(raw_data, split=False)
        self.data = feature_engineering(
            cleaned_data, cyclical_values=False, drop_cols=False
        )

    def widgets_hour_vs_var(self):
        """
        Widgets associated to the first figure
        """
        st.markdown(f"### Fig 1. Hourly number of users")
        col1, col2 = st.columns(2)
        self.agg_method = col1.radio("Aggregation method", ["mean", "median"])
        self.var = col2.selectbox(
            "Categorical variable to analyse ?",
            self.line_plot_vars,
            index=0,
            placeholder="Select variable",
        )

    def plot_hour_vs_var(self):
        """This function plot the hourly number of user as fonction
        of the hour, for different values of the var variable
        Parameters
        ----------
        self.data: pd.Dataframe
            Dataset containing data
        self.var: str
            String containing the variable the user chose to analyse
        self.agg_method: str
            String containing the method the user chose to aggregate data

        Returns
        -------
        self.fig: figure
        """
        grouped_data = (
            self.data.groupby(["Hour", self.var])
            .agg({"count": self.agg_method})
            .reset_index()
        )
        self.fig = px.line(
            grouped_data,
            x=grouped_data.Hour,
            y="count",
            color=self.var,
            markers=True,
            labels={"count": f"{self.agg_method} hourly number of users"},
        )
        if self.var in self.legend_to_modify:
            for i, new_name in enumerate(self.plot_legend_dict[self.var]):
                self.fig.data[i].name = new_name

    def widgets_var_vs_count(self):
        """Widgets associated to the second figure"""
        st.divider()
        st.markdown(f"### Fig. 2 Daily number of users")
        col2_1, col2_2 = st.columns(2)
        self.agg_method_2 = col2_1.radio(
            "Aggregation method", ["mean", "median"], key="fig2"
        )
        self.var_2 = col2_2.selectbox(
            "Categorical variable to analyse ?",
            self.line_plot_vars,
            index=0,
            placeholder="Select variable",
            key="Fig2",
        )

    def plot_var_vs_count(self):
        """This function shows the daily number of user as fonction
        the variable the user chose
        Parameters
        ----------
        self.data: pd.Dataframe
        Dataset containing data
        self.var: str
        String containing the variable the user chose to analyse
        self.agg_method: str
        String containing the method the user chose to aggregate data

        Returns
        -------
        self.fig: figure
        """
        data_temp = self.data.copy()
        data_temp["date"] = data_temp["datetime"].dt.date
        grouped_data = (
            data_temp.groupby(["date", self.var_2]).agg({"count": sum}).reset_index()
        )

        grouped_data = (
            grouped_data.groupby([self.var_2])
            .agg({"count": self.agg_method_2})
            .reset_index()
        )

        self.fig_2 = px.bar(grouped_data, x=self.var_2, y="count")
        self.fig_2.update_layout(
            yaxis_title=f"{self.agg_method_2} daily number of users",
            xaxis_title=self.var_2,
        )
        self.fig_2.update_yaxes(type="linear")
        self.fig_2.update_xaxes(type="category")
        self.fig_2.update_layout(height=600)

        if self.var_2 in self.legend_to_modify:
            for idx in range(len(self.fig_2.data)):
                self.fig.data[idx].x = self.plot_legend_dict[self.var_2]

    def widget_filter(self):
        with st.sidebar:
            st.markdown("""## FILTERS """)
            self.modify = st.checkbox("Add filters to the dataframe")

    def filter_dataframe(self):
        """
        Allowing users to filter columns

        Parameters:
            self.data: pd.DataFrame
                Original dataframe

        Returns:
            pd.DataFrame: Filtered dataframe
            bool : Is the filter radio bottom actif ?
        """

        with st.sidebar:
            if self.modify:
                to_filter_columns = st.multiselect(
                    "Filter data table on", self.data.columns
                )
                for column in to_filter_columns:
                    left, right = st.columns((1, 20))
                    left.write("↳")
                    # Treat columns with < 10 unique values as categorical
                    if self.data[column].nunique() < 13:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            self.data[column].unique(),
                            default=list(self.data[column].unique()),
                        )
                        self.filter_data = self.data[
                            self.data[column].isin(user_cat_input)
                        ]
                    elif is_numeric_dtype(self.data[column]):
                        _min = float(self.data[column].min())
                        _max = float(self.data[column].max())
                        step = (_max - _min) / 100
                        user_num_input = right.slider(
                            f"Values for {column}",
                            min_value=_min,
                            max_value=_max,
                            value=(_min, _max),
                            step=step,
                        )
                        self.filter_data = self.data[
                            self.data[column].between(*user_num_input)
                        ]
                    elif is_datetime64_any_dtype(self.data[column]):
                        user_date_input = right.date_input(
                            f"Values for {column}",
                            value=(
                                self.data[column].min(),
                                self.data[column].max(),
                            ),
                        )
                        if len(user_date_input) == 2:
                            user_date_input = tuple(
                                map(pd.to_datetime, user_date_input)
                            )
                            start_date, end_date = user_date_input
                            self.filter_data = self.data.loc[
                                self.data[column].between(start_date, end_date)
                            ]
                    else:
                        user_text_input = right.text_input(
                            f"Substring or value in {column}",
                        )
                        if user_text_input:
                            self.filter_data = self.data[
                                self.data[column]
                                .astype(str)
                                .str.contains(user_text_input)
                            ]
