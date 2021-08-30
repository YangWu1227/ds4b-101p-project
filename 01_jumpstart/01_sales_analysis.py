# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# JUMPSTART (Module 1): First Sales Analysis with Python ----

# Important VSCode Set Up:
#   1. Select a Python Interpreter: ds4b_101p
#   2. Delete terminals to start a fresh Python Terminal session

# 1.0 Load Libraries ----

# %% Start Cell

# Core Python Data Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Plotting
# Only import functions we need
from plotnine import (
    ggplot,
    aes,
    geom_col,
    geom_line,
    geom_smooth,
    facet_wrap,
    scale_y_continuous,
    scale_x_datetime,
    labs,
    theme,
    theme_minimal,
    theme_matplotlib,
    expand_limits,
    element_text
)

# Miscellaneous
from mizani.breaks import date_breaks
from mizani.formatters import date_format, currency_format

# Only import the "pretty" module from the "rich" library
from rich import pretty
# The function installs automatic pretty printing in the Python read–eval–print loop
pretty.install()

# %% End cell


# 2.0 Importing Data Files ----

# Use help(pd.read_excel) to read documentations
# Use "q" to quit help window

# %% Start Cell

# Import bike data
# Use method chaining "."
# This equivalent to info(bikes_df)
bikes_df = pd.read_excel("00_data_raw/bikes.xlsx")
bikes_df.info()

# Import bike shops data
bikeshops_df = pd.read_excel("00_data_raw/bikeshops.xlsx")
bikeshops_df.info

# Import orderlines data
# Use the converters parameter to force import date as string
orderlines_df = pd.read_excel(
    io="00_data_raw/orderlines.xlsx",
    converters={'order.date': str}
)
orderlines_df.info()

# %% End Cell


# 3.0 Examining Data (EDA) ----

# %% Start Cell

# Examine the first 5 rows for each data frame
bikes_df.head(n=5)
bikeshops_df.head(n=5)
orderlines_df.head(n=5)

# The description column from the bikes table is a factor
# Extract the column as data structured called Pandas series
print(bikes_df["description"])
# Examine its type
print(type(bikes_df["description"]))
# Using the [[ operator returns a data frame
print(type(bikes_df[["description"]]))

# Count number of obs by group
# Return the most frequent five groups
print(
    bikes_df["description"]
    .value_counts(dropna=False)
    .nlargest(n=5)
)

# Bar plot (horizontal and descending order)
(
    bikes_df["description"]
    .value_counts(dropna=False)
    .nlargest(n=5)
    .plot(kind="barh")
    .invert_yaxis()
)

# %% End Cell

# 4.0 Joining Data ----


# 5.0 Wrangling Data ----

# * No copy


# * Copy


# * Handle Dates


# * Show Effect: Copy vs No Copy


# * Text Columns


# * Splitting Description into category_1, category_2, and frame_material


# * Splitting Location into City and State


# * Price Extended


# * Reorganizing


# * Renaming columns


# 6.0 Visualizing a Time Series ----


# 6.1 Total Sales by Month ----


# Quick Plot ----


# Report Plot ----


# 6.2 Sales by Year and Category 2 ----

# ** Step 1 - Manipulate ----


# Step 2 - Visualize ----


# Simple Plot


# Reporting Plot


# 7.0 Writing Files ----


# Pickle ----


# CSV ----


# Excel ----


# WHERE WE'RE GOING
# - Building a forecast system
# - Create a database to host our raw data
# - Develop Modular Functions to:
#   - Collect data
#   - Summarize data and prepare for forecast
#   - Run Automatic Forecasting for One or More Time Series
#   - Store Forecast in Database
#   - Retrieve Forecasts and Report using Templates
