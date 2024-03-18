""" This file create a simple EDA app"""
# Absolute import
import duckdb
from src.path import DATA_DIR
from streamlit.plots import Displayer

import streamlit as st


### App
class EdaApp(Displayer):
    """
    This class creates a Streamlit app that displays the allow to explore a bike sharing dataset.

    Parameters
    ----------
    None

    Returns
    -------
    A Streamlit app
    """

    def __init__(self, DATA_DIR, LINE_PLOT_VARS, PLOT_LEGEND_DICT, VAR_DOC):
        """
        Initialize the app.
        """

        self.path = DATA_DIR / "raw_data.csv"
        self.line_plot_vars = LINE_PLOT_VARS
        self.plot_legend_dict = PLOT_LEGEND_DICT
        self.legend_to_modify = LEGEND_TO_MODIFY
        self.var_doc = VAR_DOC

        st.set_page_config(layout="wide")

        # load data
        self.load_data()

        # display App title and description
        self.title_and_description()

        # display filter widget
        self.widget_filter()

        # display the filter fonctionnality in the side in the side bar
        self.filter_dataframe()

        # config dataframe display
        self.display_df_config()

        # display dataset and sql query entry
        self.display_dataset_section()

        # display widgets of figure 1
        self.widgets_hour_vs_var()

        # plot fig 1
        self.plot_hour_vs_var()
        st.plotly_chart(
            self.fig, theme="streamlit", use_container_width=True, width=1000
        )

        # display widdget fig 2
        self.widgets_var_vs_count()

        # display plot fig 2
        self.plot_var_vs_count()
        st.plotly_chart(
            self.fig_2, theme="streamlit", use_container_width=True, width=1000
        )

    def title_and_description(self):
        """Display title and App description
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        st.title("Bike sharing dataset ")
        st.header("An exploratory data analysis tool")
        st.markdown(
            """ This app is a simple tool allowing
                    analysts to make a first exploratory data analysis
                    of the bike sharing dataset.
                """
        )

    def display_dataset_section(self):
        """Display the dataset and the related fonctionnalities
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        with st.container(border=True):
            st.markdown("### The dataset")
            text_query = st.text_area(
                label="You can write a SQL query below. The table name is: data"
            )

            if self.modify:
                tab0, tab1, tab2 = st.tabs(
                    ["filtered 'data' table", "'data' table", "queried table"]
                )
                with tab0:
                    try:
                        st.dataframe(
                            self.filter_data,
                            column_config=self.df_config,
                            hide_index=True,
                        )
                    except:
                        st.dataframe(
                            self.data, column_config=self.df_config, hide_index=True
                        )
            else:
                tab1, tab2 = st.tabs(["'data' table", "queried table"])
            with tab1:
                st.dataframe(self.data, column_config=self.df_config, hide_index=True)
            with tab2:
                try:
                    data = self.data.copy()

                    self.result = duckdb.query(text_query).df()

                    st.dataframe(self.result, column_config=self.df_config)
                except:
                    st.write("The SQL query is empty or incorrect")

    def display_df_config(self):
        """
        Define the config to display the dataframe
        Parameters
        ----------
        None

        Returns
        -------
        self.df_config: pandas dictionnary
            Dictionnary allowing to configure st.dataframe
        """
        self.df_config = {
            "Year": st.column_config.NumberColumn(
                help="Number of stars on GitHub", format="%d"
            ),
            "holiday": st.column_config.CheckboxColumn(
                help="It indicates whether the day is a school holiday"
            ),
            "season": st.column_config.NumberColumn(help=str(self.var_doc["season"])),
            "weather": st.column_config.NumberColumn(help=str(self.var_doc["weather"])),
            "temp": st.column_config.NumberColumn(help="Temperature in Celsius"),
            "atemp": st.column_config.NumberColumn(
                help="Feeling temperature in Celsius"
            ),
            "casual": st.column_config.NumberColumn(help="Count of casual users"),
            "registered": st.column_config.NumberColumn(
                help="Count of registered users"
            ),
            "count": st.column_config.NumberColumn(help="Hourly number of users"),
            "Weekday": st.column_config.NumberColumn(help=str(self.var_doc["Weekday"])),
        }


if __name__ == "__main__":
    EdaApp(DATA_DIR, LINE_PLOT_VARS, PLOT_LEGEND_DICT, VAR_DOC)
