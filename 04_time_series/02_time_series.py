# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 4 (Time Series): Working with Time Series Data ----

# Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_extensions.database import collect_data

# Data
df = pd.DataFrame(collect_data())

# 1.0 DATE BASICS

# Check timestamp
df["order_date"]

# Conversion from string to timestamp object
pd.to_datetime("2021-10-3")
# Conversion from timestamp object to period object
pd.to_datetime("2021-10-3").to_period(freq="W")
# Conversion from period object back to timestamp object
pd.to_datetime("2021-10-3").to_period(freq="W").to_timestamp()

# Accessing elements

# Months


# Days


# DATE MATH


# DATE SEQUENCES


# PERIODS
# - Periods represent timestamps that fall within an interval using a frequency.
# - IMPORTANT: {sktime} requires periods to model univariate time series


# Convert to Time Stamp

# Get the Frequency


# TIME-BASED GROUPING (RESAMPLING)
# - The beginning of our Summarize by Time Function

# Using kind = "timestamp"


# Using kind = "period"


# MEASURING CHANGE

# Difference from Previous Timestamp

#  - Single (No Groups)


#  - Multiple Groups: Key is to use wide format with apply


#  - Difference from First Timestamp


# CUMULATIVE CALCULATIONS


# ROLLING CALCULATIONS

# Single

# Groups - Can't use assign(), we'll use merging
