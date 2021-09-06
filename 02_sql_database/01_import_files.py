# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 2 (Pandas Import): Importing Files ----

# IMPORTS ----

# %% Start Cell

import pandas as pd

# 1.0 FILES ----

# - Pickle ----

# Pickle object reads faster and is read exactly as how it was saved
df_pickle = pd.read_pickle("00_data_wrangled/bikes_wrangled.pk1")

# - CSV ----

# CSV files my import the wrong data structure for certain variables
# Use parse_date to convert data column from text to datetime object
df_csv = pd.read_csv("00_data_wrangled/bikes_wrangled.csv",
                     # This argument only works with index column
                     # Need to specify a list to specify columns
                     parse_dates=["order_date"])
# Check name
# The "order_date" column is now a datetime object
df_csv.info()

# - Excel ----

# Excel file
# The function did parse the "order_date" column as datetime object
df_excel = pd.read_excel("00_data_wrangled/bikes_wrangled.xlsx")

# %% End cell
