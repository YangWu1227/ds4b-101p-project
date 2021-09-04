# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# JUMPSTART (Module 1): First Sales Analysis with Python ----

# Important VSCode Set Up:
#   1. Select a Python Interpreter: ds4b_101p
#   2. Delete terminals to start a fresh Python Terminal session

# 1.0 Load Libraries ----

# %% Start Cell

# Core Python Data Analysis
import os
from textwrap import fill
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core import groupby

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
    element_rect,
    element_blank,
    element_text,
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
from plotnine.themes.elements import element_blank, element_rect
from plotnine.themes.themeable import panel_background

# Only import the "pretty" module from the "rich" library
from rich import pretty
from rich.console import group
# The function installs automatic pretty printing in the Python read–eval–print loop
pretty.install()

# Import OS library to interact with operating system

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
# A new binding is created from the name "df" to the copied object with reordered columns
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

# Create a new binding from new name to the same object
bikes_orderlines_wrangled = df

# %% End Cell

# Store data as file so we do not need to run the above cells each time

# %% Start Cell

# Check current working directory
os.getcwd()
# Create a new sub-directory in this working directory using a relative path
# os.mkdir(path="00_data_wrangled")
# Serialize pandas data frame to folder using pickle
# Python serialization is the act of converting a Python object into a byte stream
# bikes_orderlines_wrangled.to_pickle(path="00_data_wrangled/bikes_wrangled.pk1")

# %% End Cell


# 6.0 Visualizing a Time Series ----

# %% Start Cell

# Unpickle byte stream to get python object back
df = pd.read_pickle(
    "00_data_wrangled/bikes_wrangled.pk1"
)
df = pd.DataFrame(df)

# 6.1 Total Sales by Month ----

# Examine datetime object (datetime64[ns])
print(df["order_date"])
# Extract year, month, day
print(df["order_date"].dt.year)
print(df["order_date"].dt.month)
print(df["order_date"].dt.day)

# Subset
sales_by_month = (df[["order_date", "total_revenue"]]
                  # Set date column as index (row labels)
                  # Similar to xts objects in R
                  # The argument "inplace" indicates whether to modify in place
                  .set_index(
    keys="order_date",
    inplace=False
)
    # Frequency conversion and resampling of time series
    # The rule argument is the offset alias
    # Data will be grouped by the frequency "rule"
    # We convert from daily to monthly frequency
    # "MS" is the alias for month start frequency
    .resample(
        rule="MS"
)
    # Sum total revenue by month
    .aggregate(
        func=np.sum
)
    .reset_index()
)
# Examine last 10 rows
sales_by_month.tail(n=5)
# Number of monthly observations (n = 60)
len(sales_by_month)

# Quick Plot ----

sales_by_month.plot(
    x="order_date",
    y="total_revenue"
)

# Report Plot ----

# Use a function factory that creates a function that formats numeric values
usd_fn = currency_format(prefix="$", digits=0, big_mark=",")
# See it in action
usd_fn([100000])

# Note some arguments use "." in R but "_" in Python
(ggplot(data=sales_by_month,
        mapping=aes(x="order_date", y="total_revenue")) +
 geom_line(color="black") +
 geom_smooth(
    method="loess",
    color="orange",
    se=False,
    # This argument controls the amount of smoothing
    # Smaller numbers produce wigglier lines, larger numbers produce smoother lines.
    span=0.4
) +
    labs(
    x="",
    y="Revenues (USD)",
    title="Total Monthy Revenues"
) +
    scale_y_continuous(
    labels=usd_fn
) +
    # Ensure that the y-axis begins with 0
    expand_limits(
    y=0
) +
    theme(
    panel_background=element_rect(fill="white"),
    panel_grid=element_blank()
))


# 6.2 Sales by Year and Category 2 ----

# ** Step 1 - Manipulate ----
# Subset
sales_by_week = (df[["order_date", "total_revenue", "category_2"]]
                 .set_index(
    keys="order_date"
)
    # This returns a DataFrameGroupBy object
    # THe split-apply-combine approach
    .groupby(
    by="category_2"
)
    # This returns DatetimeIndexResamplerGroupby object
    .resample(
        rule="W"
)
    # Sum total revenue by Week
    # Pass a dictionary of dictionaries to .agg
    # Apply np.sum to the "total_revenue" column
    .aggregate(
        func={"total_revenue": np.sum}
)
    # Remove multiindex
    # Remve this last line to see what multiindex means
    .reset_index()
)

sales_by_week = pd.DataFrame(sales_by_week)

# Step 2 - Visualize ----

sales_by_week

# Convert data from long to wide
sales_by_week_wide = (sales_by_week
                      .pivot(
                          index="order_date",
                          columns="category_2",
                          values="total_revenue"
                      )
                      # Fill NaN as 0
                      .fillna(
                          value=0,
                          inplace=False
                      )
                      )

# Simple Plot
# This defaults to using row indices as x and columns as y
sales_by_week_wide.plot(
    kind="line",
    subplots=True,
    layout=(5, 2)
)


# Reporting Plot
(ggplot(data=sales_by_week,
        mapping=aes(
            x="order_date",
            y="total_revenue"
        )) +
 geom_smooth(
    mapping=aes(color="category_2"),
    method="loess",
    se=False,
    span=0.2
) +
    facet_wrap(
    facets="category_2",
    # Ensure each category has its own y-axis
    scales="free_y"
) +
    scale_y_continuous(
    labels=usd_fn
) +
    scale_x_datetime(
    breaks=date_breaks("2 years"),
    labels=date_format(fmt="%Y %m")
) +
    labs(
    x="",
    y="Total Revenue",
    title="Total Revenue by Weeky",
    # Change legend title
    color="Category"
) +
    theme(
    subplots_adjust={"wspace": 0.5},
    # Change y axis text size
    axis_text_y=element_text(size=6),
    # Change x axis text size
    axis_text_x=element_text(size=6),
    panel_background=element_rect(fill="white"),
    panel_grid=element_blank()
)
)


# 7.0 Writing Files ----

# CSV ----
df.to_csv("00_data_wrangled/bikes_wrangled.csv",
          # Do not include primary key
          # Or use index_lable to specify column name
          index=False)

# Excel ----
df.to_excel("00_data_wrangled/bikes_wrangled.xlsx",
            # Do not include primary key
            # Or use index_lable to specify column name
            index=False)

# %% End cell

# WHERE WE'RE GOING
# - Building a forecast system
# - Create a database to host our raw data
# - Develop Modular Functions to:
#   - Collect data
#   - Summarize data and prepare for forecast
#   - Run Automatic Forecasting for One or More Time Series
#   - Store Forecast in Database
#   - Retrieve Forecasts and Report using Templates
