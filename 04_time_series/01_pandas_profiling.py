# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 4 (Time Series): Profiling Data ----


# IMPORTS
import pandas as pd
import numpy as np
from pandas_profiling import profile_report, ProfileReport
from pandas_extensions.database import collect_data

# PANDAS PROFILING
df = pd.DataFrame(collect_data())

# Get a Profile
# This method generate a profile report from a Dataset stored as a pandas `DataFrame`
# This object is of class ProfileReport
profile = ProfileReport(
    df=df
)

# Sampling - Big Datasets


# Pandas Helper
# ?pd.DataFrame.profile_report


# Saving Output


# VSCode Extension - Browser Preview
