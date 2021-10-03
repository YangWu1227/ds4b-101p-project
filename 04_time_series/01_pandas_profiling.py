# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 4 (Time Series): Profiling Data ----


# Imports
import pandas as pd
import os as os
import numpy as np
from pandas_profiling import profile_report, ProfileReport
from pandas_extensions.database import collect_data

# Pandas Profiling
df = pd.DataFrame(collect_data())

# Get a Profile
# This method generate a profile report from a dataset stored as a pandas `DataFrame`
# This object is of class ProfileReport
profile = ProfileReport(
    df=df
)

# Sampling - Big Datasets
# This is in a sense similar to the augment() function from the R broom package
df.profile_report()

# If the Data frame is large, we can take a random sample
df.sample(frac=0.5).profile_report()

# Pandas Helper
# ?pd.DataFrame.profile_report

# Saving Output
df.profile_report().to_file("./04_time_series/profile_report.html")

# VSCode Extension - Browser Preview
