# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 4 (Time Series): Working with Time Series Data ----

# Imports ------------------------------------
from numpy.core.shape_base import stack
import pandas as pd
import numpy as np
import inspect as insp
import datetime as dt
import matplotlib.pyplot as plt
from pandas_extensions.database import collect_data

# Data ------------------------------------
df = pd.DataFrame(collect_data())


# Check timestamp ------------------------------------
df["order_date"]

# Conversion from string to timestamp object
pd.to_datetime("2021-10-3")
# Conversion from timestamp object to period object
pd.to_datetime("2021-10-3").to_period(freq="W")
# Conversion from period object back to timestamp object
pd.to_datetime("2021-10-3").to_period(freq="W").to_timestamp()

# Accessing elements using the datetime accessor ------------------------------------

# Months ------------------------------------
df.order_date.dt.month
df.order_date.dt.month_name()

# Days ------------------------------------
df.order_date.dt.day
df.order_date.dt.day_name()

# Years ------------------------------------
df.order_date.dt.year

# DATE MATH  ------------------------------------

# Get today's date
# Using the classmethod from the "date" module
dt.date.today()
# Timedelta is the pandas equivalent of datetime.timedelta
# This represents a duration
# String
pd.Timedelta('2 days 2 hours 15 minutes 30 seconds')
# Integer
pd.Timedelta(6, unit='h')
# Date offsets
# Weeks, days, hours, minutes, seconds
# Milliseconds, microseconds, nanoseconds
pd.Timedelta(microseconds=4000000000000)
# Arithmetic
pd.to_datetime(dt.date.today() - pd.Timedelta('2 days'))
# Suppose we would like to shift the date feature one year
df.order_date + pd.Timedelta("1Y")

# Duration ------------------------------------
# There is on average 4.345 weeks in a month
((dt.date.today() + pd.Timedelta("1Y")) - dt.date.today()) / pd.Timedelta("4.345W")

# DATE SEQUENCES ------------------------------------
# Frequency defaults to daily
pd.date_range(
    start=pd.to_datetime("2011-01"),
    # Number of periods
    periods=10,
    # Frequency
    freq="2D"
)
# Alternatively, we can supply an end date
pd.date_range(
    start=pd.to_datetime("2011-01"),
    end=pd.to_datetime("2021-01"),
    freq="2Y"
)


# PERIODS ------------------------------------
# - Periods represent timestamps that fall within an interval using a frequency.
# - IMPORTANT: {sktime} requires periods to model univariate time series


# Convert to Time Stamp ------------------------------------
# The order_date column has data type datetime64[ns]
df.order_date
# Convert to periods collapse observations based on period widths
df.order_date.dt.to_period(freq="s")
df.order_date.dt.to_period(freq="h")
df.order_date.dt.to_period(freq="D")
df.order_date.dt.to_period(freq="W")
df.order_date.dt.to_period(freq="M")
df.order_date.dt.to_period(freq="Q")
df.order_date.dt.to_period(freq="Y")
df.order_date.dt.to_period(freq="2Y")

# Get the Frequency ------------------------------------
df.order_date.dt.to_period(freq="W").dt.freq
df.order_date.dt.to_period(freq="M").dt.freq
df.order_date.dt.to_period(freq="2Y").dt.freq

# Use pd.to_datetime() to convert text to timestamp
# Use pd.to_period() to convert timestamp to period
# Use pd.to_timestamp() to convert period to timestamp
# Notice that the dates have changed based on the frequency
# Compare this to the original pandas series
df.order_date.dt.to_period(freq="W").dt.to_timestamp()
df.order_date.dt.to_period(freq="M").dt.to_timestamp()


# TIME-BASED GROUPING (RESAMPLING) ------------------------------------
# - The beginning of our Summarize by Time Function

# Single timeseries ------------------------------------
# Using kind = "timestamp"
# Pass ‘timestamp’ to convert the resulting index to a DateTimeIndex
bike_sales_m_df = pd.DataFrame(
    df[["order_date", "total_revenue"]]
    .set_index(
        "order_date"
    )
    .resample(
        rule="M",
        kind="timestamp"
    )
    .aggregate(
        func=np.sum
    )
    .reset_index()
)

# Grouped timeseries ------------------------------------
# Using kind = "period"
# Pass ‘period’ to convert resulting index to a PeriodIndex
bike_sales_cat2_m_wide_df = pd.DataFrame(
    df[["category_2", "order_date", "total_revenue"]]
    .set_index(
        ["order_date"]
    )
    # Groupby prevents us to use kind = "period"
    # The grouped indices have overlaps and pandas cannot handle it
    # For instance, "Elite" and "Fat" bikes may have overlapping order_dates
    .groupby(
        by="category_2"
    )
    # We have to manually convert to monthly periodicity later
    .resample(
        # Offset alias
        rule="M",
        kind="period"
    )
    .aggregate(
        func=np.sum
    )
    .reset_index()
    # Convert order_date from period to timestamp manually
    .assign(
        # The x is the df object so we subset for order_date
        order_date=lambda x: x.order_date.dt.to_period(freq="M")
    )
    # Pivot wider
    .pivot(
        index="order_date",
        columns="category_2",
        values="total_revenue"
    )
)

# MEASURING CHANGE ------------------------------------

# Difference from Previous Timestamp ------------------------------------

#  - Single (No Groups)
# First way ------------------------------------
(
    bike_sales_m_df.assign(
        # Here x is the df so we need to get the series
        # We use the shift() method of pandas series
        total_revenue_lagged=lambda x: x.total_revenue.shift(periods=1)
    )
    .assign(
        diff=lambda x: x.total_revenue - x.total_revenue_lagged
    )
    .plot(y="diff")
)

# Second way ------------------------------------
(
    bike_sales_m_df.set_index(
        # Set order_date as index
        # The date column cannot be used to compute percentage change
        ["order_date"]
    )
    .apply(
        # Here x is the entire data frame
        func=lambda x: (x - x.shift(periods=1)) / (x.shift(periods=1))
    )
    # Remove first row due to NaN
    .iloc[1:, :]
    .style.format(
        {"total_revenue": lambda x: f'{round(x, 4)}%'}
    )
)

# Multiple Groups: Key is to use wide format with apply ------------------------------------
(
    bike_sales_cat2_m_wide_df.apply(
        # Here x is the entire data frame
        func=lambda x: x - x.shift(periods=1)
    )
)

# Another option is to apply lambda function to grouped data frames
# The downside is we lose the category variable
(
    bike_sales_cat2_m_wide_df.reset_index()
    # Convert back to long format
    # We need to use the "order_date" field and so reset_index()
    .melt(
        id_vars="order_date",
        value_vars=[
            'Cross Country Race', 'Cyclocross',
            'Elite Road', 'Endurance Road',
            'Fat Bike', 'Over Mountain',
            'Sport', 'Trail', 'Triathalon'
        ],
        var_name="category_2",
        value_name="total_revenue"
    )
    .set_index(
        ["order_date"]
    )
    .groupby(
        by=["category_2"]
    )
    # We lose the category grouping variable
    # Could also use .apply()
    .transform(
        # Each x is a grouped data frame
        func=lambda x: x - x.shift(periods=1)
    )
    .reset_index()
)


# Difference from First Timestamp ------------------------------------
# Relative difference w.r.t the first obs
(
    bike_sales_m_df.set_index(
        ["order_date"]
    )
    .apply(
        # Here x is the entire data frame
        func=lambda x: (x - x[0]) / x[0]
    )
    .plot()
)

# Wide data ------------------------------------
(
    bike_sales_cat2_m_wide_df.apply(
        # Here x is the entire data frame
        func=lambda x: (x - x[0]) / x[0]
    )
    .plot()
)

# Another solution ------------------------------------
(
    bike_sales_cat2_m_wide_df.stack(
        "category_2"
    )
    .groupby(
        by="category_2"
    )
    .transform(
        func=lambda x: x - x[0]
    )
)

# CUMULATIVE CALCULATIONS ------------------------------------

# Single time series ------------------------------------

# Method 1 ------------------------------------
(
    bike_sales_m_df.set_index(
        ["order_date"]
    )
    .resample(
        # Year start
        rule="YS"
    )
    .aggregate(
        func=np.sum
    )
    # Cumulative sum function
    .cumsum()
    # Reset order_date as a column
    .reset_index()
    # Convert from timestamp to period
    .assign(
        order_date=lambda x: x.order_date.dt.to_period(freq="Y")
    )
    # Set the index again
    .set_index(
        ["order_date"]
    )
    # Now the x axis will be year
    .plot(kind="bar")
)

# Method 2 ------------------------------------
(
    bike_sales_m_df.set_index(
        ["order_date"]
    )
    .resample(
        # Year start
        rule="YS"
    )
    .aggregate(
        func=np.sum
    )
    # Use the pd.Dataframe.expanding() function
    # This returns an expanding object
    # It allows summary functions to be applied cumulatively
    .expanding()
    # Summary function
    .aggregate(
        func=np.sum
    )
    # Reset order_date as a column
    .reset_index()
    # Convert from timestamp to period
    .assign(
        order_date=lambda x: x.order_date.dt.to_period(freq="Y")
    )
    # Set the index again
    .set_index(
        ["order_date"]
    )
    # Now the x axis will be year
    .plot(kind="bar")
)

# Multiple time series ------------------------------------
(
    bike_sales_cat2_m_wide_df.resample(
        # Year end frequency
        rule="Y"
    )
    .aggregate(
        func=np.sum
    )
    .cumsum()
    .plot(kind="bar", stacked=True)
)

# ROLLING CALCULATIONS ------------------------------------

# Single timeseires ------------------------------------
# Simple line chart ------------------------------------
(
    bike_sales_m_df.plot(y="total_revenue")
)

# Rolling mean ------------------------------------
(
    bike_sales_m_df.set_index(
        ["order_date"]
    )
    .assign(
        # Return a rolling object
        # Allow summary functions to be applied to windows of length n
        rolling_mean=lambda x: x["total_revenue"].rolling(
            # 12 months
            window=12,
            # Center align the rolling mean series
            center=True,
            # Allow edge cases to use partial windows < 12 months
            # Allow for as small as 1 month window for first and last obs
            min_periods=1
        )
        .aggregate(
            func=np.mean
        )
    )
    .plot()
)

# Multiple timeseires ------------------------------------
(
    bike_sales_cat2_m_wide_df.apply(
        func=lambda x: x.rolling(
            window=24,
            center=True,
            min_periods=1
        )
        .aggregate(
            func=np.mean
        )
    )
    .plot()
    .get_legend()
    .set_visible(False)
)

# We do not need to use the apply() function
(
    bike_sales_cat2_m_wide_df.rolling(
        window=24,
        center=True,
        min_periods=1
    )
    .aggregate(
        func=np.mean
    )
    # Rename the columns before merging with original data frame
    .rename(
        mapper=lambda x: x + "_rolling_values",
        axis=1
    )
    # Left join
    .merge(
        right=bike_sales_cat2_m_wide_df,
        how="left",
        left_index=True,
        right_index=True
    )
    .plot()
    .get_legend()
    .set_visible(False)
)
