# Standard Library
from pathlib import Path

# External Libraries
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
import plotly.express as px
from shiny import render, reactive
from shinywidgets import render_widget

# Local Imports
from books_get_basics import get_books_df
from util_logger import setup_logger

# Set up a global logger for this file
logger, logname = setup_logger(__name__)

# Declare our file path variables globally so they can be used in all the functions (like logger)
csv_books = Path(__file__).parent.joinpath("data").joinpath("book.csv")


def get_books_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    # First, declare shared reactive values (used between functions) up front
    # Initialize the values on startup
    # Previously, we had a single reactive dataframe to hold filtered results
    reactive_df = reactive.Value()
    # We also provided shared variables to hold the original dataframe and its count
    original_df = get_books_df()
    total_count = len(original_df)

    # Then, define our server functions

    @reactive.file_reader(str(csv_books))
    def get_book_df():
        logger.info(f"READING df from {csv_books}")
        df = pd.read_csv(csv_books)
        logger.info(f"READING df len {len(df)}")
        return df
    
    @reactive.Effect
    @reactive.event(input.BOOK_PRICE,input.AUTHOR)
    def _():
        input_range = input.BOOK_PRICE()
        input_min = input_range[0]
        input_max = input_range[1]
        author = input.AUTHOR()
        
        # init_mtcars_temps_csv()
        df = get_books_df()
        if author != "":
            filtered_df = df[(df["Price"] >= input_min) & (df["Price"] <= input_max) & (df["Author"] == author)]
        else:
            filtered_df = df[(df["Price"] >= input_min) & (df["Price"] <= input_max)]
        logger.info(f"init reactive_temp_df len: {len(df)}")
        reactive_df.set(filtered_df)
    
    @output
    @render.table
    def book_table():
        filtered_df = reactive_df.get()
        # Filter the data based on the selected location
        logger.info(f"Rendering TEMP table with {len(filtered_df)} rows")
        return filtered_df
    @output
    @render_widget
    def book_chart():
        logger.info(f"Starting mtstocks_output_widget1")
        filtered_df = reactive_df.get()
        logger.info(f"Rendering Price chart with {len(filtered_df)} points")
        plotly_express_plot = px.bar(filtered_df, x="Title",y="Price", color="Author")
        plotly_express_plot.update_layout(title="Books with Plotly Express")
        return plotly_express_plot

    @output
    @render.text
    def book_record_count_string():
        df = get_book_df()
        filtered_count = len(df)
        message = f"Showing {filtered_count} of {total_count} records"
        logger.debug(f"filter message: {message}")
        return message

    return [
        book_table,
        book_chart,
        book_record_count_string, 
    ]
