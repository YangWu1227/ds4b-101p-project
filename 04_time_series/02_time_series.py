# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 4 (Time Series): Working with Time Series Data ----

# IMPORTS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from my_pandas_extensions.database import collect_data

# DATA

df = collect_data()

# 1.0 DATE BASICS



# Conversion


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




