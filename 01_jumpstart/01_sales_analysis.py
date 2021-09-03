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

# %% Start Cell

# Check pandas df object type
print(type(orderlines_df))
# Convert to pandas data frame object
orderlines_df = pd.DataFrame(orderlines_df)
print(type(orderlines_df))

# Drop primary key column
# The axis argument indicates whether to drop labels from the index or columns
bikes_orderlines_df = (orderlines_df
                       .drop(
                           columns="Unnamed: 0",
                           axis="column"
                       )
                       # Left join bikes data onto orderlines data
                       .merge(
                           right=bikes_df, how="left",
                           left_on="product.id", right_on="bike.id"
                       )
                       # Left join bikeship data on two the resultant data
                       .merge(
                           right=bikeshops_df, how="left",
                           left_on="customer.id", right_on="bikeshop.id"))

# %% End Cell


# 5.0 Wrangling Data ----

# %% Start Cell

# * No copy
df = bikes_orderlines_df
df
# * Copy
# Make a copy of this object's indices and data
# Deafult is deep = TRUE
# Modifcations to the copy will not be reflected in the original
df2 = bikes_orderlines_df.copy(deep=True)
df2

# * Handle Dates
print(type(df["order.date"]))
# Subset and assignment
df["order.date"] = pd.to_datetime(df["order.date"])
# Check type and see if that column is a data time object
df.info()

# * Show Effect: Copy vs No Copy
# See that the object "bikes_orderlines_df" is also modified
# Without copy, Python implements modify-in-place
# See that the data column is now a datetime object
# When we use the "=" operator, we create a new binding
# This binding still references the original object
# This may be memory efficient but is less safe
bikes_orderlines_df.info()

# With df.copy(), a new memory allocation is created
# Python implements copy-on-modify now
# This doubles the memory usage but preserves the original object
df2.info()

# * Text Columns
# To see columns more clearly, we may transpose the df
df.T

# * Splitting Description into category_1, category_2, and frame_material
# Use the split() function to plot text variable into separate ones
# This gives us a series lists with three elements
print(df["description"].str.split(pat=" - "))
# The "expand" argument indicates whether to expand the split strings into separate columns
print(df["description"].str.split(pat=" - ", expand=True))
# Now subset multiple elements and assign
df[["category_1",
    "category_2",
    "frame_material"]] = (df["description"]
                          .str.split(
        pat=" - ",
        expand=True
    ))
df

# * Splitting Location into City and State
df[["city", "state"]] = (df["location"]
                         .str.split(
    pat=", ",
    expand=True
))
df

# * Price Extended
df["total_revenue"] = df.quantity * df.price

# Order rows by values of revenue (high to low)
df.sort_values(by="total_revenue", ascending=False)

# * Reorganizing

# Get attributes (colnames) from df object class
# This returns all the column names
df.columns
# This function is used to access the attribute of object
print(getattr(df, "total_revenue"))
# Keep only a subset of variable
# Subset by character index (a list)
# Use [[ operator for multiple subsetting
# This creates a copy
# A new binding is created from the name df to the copied object
df = df[[
    'order.id',
    'order.line',
    'order.date',
    # 'customer.id',
    # 'product.id',
    'quantity',
    # 'bike.id',
    'model',
    'price',
    'total_revenue',
    # 'description',
    # 'bikeshop.id',
    'bikeshop.name',
    # 'location',
    'category_1',
    'category_2',
    'frame_material',
    'city',
    'state'
]]


# * Renaming columns
# Replace all "." with "_"
df.columns = df.columns.str.replace(
    pat=".",
    repl="_",
)

# Create a new binding from new name to same object
bikes_orderlines_wrangled = df

# %% End Cell


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
