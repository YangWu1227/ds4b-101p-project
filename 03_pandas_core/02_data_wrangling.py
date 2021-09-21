# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Week 2 (Data Wrangling): Data Wrangling ----

# IMPORTS -------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.series import Series
from plotnine.themes.elements import element_blank
from pandas_extensions.database import collect_data
from mizani.formatters import dollar_format
from plotnine import (
    ggplot, geom_col,
    aes, facet_wrap, labels,
    theme, labs,
    element_blank, element_rect,
    coord_flip, guide_legend
)

# DATA -------------------------------------------

df = pd.DataFrame(collect_data())

# 1.0 SELECTING COLUMNS -------------------------------------------

# Select by name -------------------------------------------

# Pass a list of strings to [] operator
# Select column in the order specified by the list
# This returns a pandas.core.frame.DataFrame
df[["order_date", "order_id", "order_line"]]

# Using [] returns a pandas.core.series.Series
df["order_date"]

# Select by position -------------------------------------------

# Purely integer-location based indexing for selection by position
# All rows and the first three columns
df.iloc[:, 0:3]

# All columns and last two rows
# Start indexing from the last row and stop at the third last row
df.iloc[:-3:-1, :]

# Another way is to use the head and tail methods
df.tail(n=3)
df.head(n=5)

# Select by text matching -------------------------------------------

# Use the filter method
# Select columns whose name matches regular expression regex
# This returns a data frame
df.filter(regex="order_date")

# Regex expression
# Select columns whose names "start" with "order"
df.filter(regex="(^order)", axis=1)

# Select columns whose names "contain" "cat"
# Sort of like wildcard
df.filter(regex="cat", axis=1)

# Select columns whose names end with "price"
df.filter(regex="(price$)", axis=1)

# Rearranging columns -------------------------------------------

# - Single column

# This is a pandas.core.indexes.base.Index object
type(df.columns)
df.columns
# Convert this index object to list
list_of_names = df.columns.tolist()
print(list_of_names)
# Now remove the column we wish to rearrange
list_of_names.remove("model")
# Now create a new list with "model" as the first element
# Use * to unpack so that we don't have a nested list inside the list
list_of_names = ["model", *list_of_names]
# Now subset
# The columns are now ordered as desired
df[list_of_names]

# - Multiple column

# Suppose we would like to rearrange multiple columns
# First we get the index object and convert to list
list_of_names = df.columns.tolist()
print(list_of_names)
# We rearrange as desired
list_of_names = ['frame_material', 'order_id',
                 'order_date', 'state',
                 'quantity', 'price',
                 'total_revenue',
                 'model', 'category_1',
                 'category_2', 'order_line',
                 'bikeshop_name', 'city']
# Now subset with this index list
# The columns will now be in the right order
df[list_of_names]

# - Multiple columns using set operations

# Suppose we would like to move three columns up front
# First, create a set of column names to be moved
set_of_moves = set(["bikeshop_name", "city", "state"])
type(set_of_moves)
# Create a set of all columns
set_of_names = set(df.columns.tolist())
# Keep columns in set_of_names that are not in set_of_moves
set_of_stay = set_of_names - set_of_moves
print(set_of_stay)
# Or equivalently using set method
set_of_stay_method = set_of_names.difference(set_of_moves)
print(set_of_stay_method)
# The above two are the same
print(set_of_stay == set_of_stay_method)
# Now index using the new sets with the set of moves up front
# Be sure convert sets to lists and to unpack the two lists
df[[*list(set_of_moves), *list(set_of_stay)]]


# - Multiple columns using list comprehension
# The basic syntax
[name for name in list_of_names]
# This essentially just prints the list itself
[name for name in list_of_names] == list_of_names
# Keep only those columns not in the move list
list_of_stay = [
    name for name in list_of_names if name not in list(set_of_moves)]
print(list_of_stay)
# Now subset the three columns up front and the rest behind
df[[*list(set_of_moves), *list_of_stay]]


# Select by data types -------------------------------------------

# Examine data types
df.info()
# Select method to include all text columns
df.select_dtypes(include="object")
# Select method to exclude all text columns
df.select_dtypes(exclude="object")

# Dropping Columns (De-selecting) -------------------------------------------

# Drop columns by name
df.drop(["model", "order_line", "city"], axis=1)

# Suppose we wish to move the above three columns to the back
# Create an intermediate df to store columns without those three
df_keep_front = df.drop(["model", "order_line", "city"], axis=1)
print(df_keep_front)
# Create another intermediate df to store columns to be moved
df_move_back = df[["model", "order_line", "city"]]
print(df_move_back)
# Now column bind the two data frames using the concat method
# Now three columns are moved to the back
pd.concat(
    [df_keep_front,
     df_move_back],
    axis=1
)

# 2.0 ARRANGING ROWS -------------------------------------------

# Sort by a single column, ascending by default
df.sort_values(
    by=["total_revenue"],
    ascending=False,
    inplace=False,
    na_position="last"
)

# Sort by multiple columns
# First by total revenue and then by quantity
# This means that whenever there's a tie in total revenue
# Quantity will be used to sort the ties in total revenue
df.sort_values(
    by=["total_revenue", "quantity"],
    ascending=False,
    inplace=False,
    na_position="last"
)

# 3.0 FILTERING  -------------------------------------------

# Simpler Filters -------------------------------------------

# Suppose we wish to filter all rows with order date > 2015
# Create an boolean index series
df.order_date >= pd.to_datetime("2015-01-01")
type(df.order_date >= pd.to_datetime("2015-01-01"))
# Now select rows based on TRUE's in the boolean index series
df[df.order_date >= pd.to_datetime("2015-01-01")]

# Suppose we wish to filter rows by category
# Select all road bikes
df[df.category_1 == "Road"]

# Pandas series also has string accessors
# Such as startswith(), endswith(), contains() methods
print(df.category_2.str.contains("Elite"))
# Now select rows where "category 2" contains Elite
df[df.category_2.str.contains("Elite")]

# Select rows where the city starts with the letter "L"
df[df.city.str.startswith("L")]

# Select rows where the bikeshop name ends with "Equipment"
df[df.bikeshop_name.str.endswith("Equipment")]

# Query -------------------------------------------

# Select rows with total revenue is between 2000 and 3000
df.query("total_revenue >= 2000 and total_revenue <= 3000")

# Filtering Items in a List -------------------------------------------

# There are two useful methods for factors
# Get unique array from a categorical variable (factor)
df.category_2.unique()
# Get frequency count
df.category_2.value_counts()

# Suppose we wish to select a subset of factor levels
# The isin() method detects whether elements in a series are in values
# The argument values must be set or list-like
df[df.category_2.isin(values=set(["Trail", "Cross Country Race"]))]
# To exclude those two groups we can negate using ~
# This is similar to !TRUE == FALSE in R
df[~ df.category_2.isin(values=set(["Trail", "Cross Country Race"]))]

# Slicing -------------------------------------------

# Subset using the loc() method which selects by name
# All rows and only the price and revenue columns
(
    df.loc[:, ["price", "total_revenue"]]
    # Then sort by total revenue
    .sort_values(
        by=["total_revenue"],
        ascending=False
    )
)

# Select rows meeting logical condition and specific columns
(
    df.loc[
        # Order date must be after august of each year
        df["order_date"] >= pd.to_datetime("2012-08-01"),
        ["order_date", "price", "total_revenue"]
    ]
)

# Index Slicing -------------------------------------------

# Suppose we want the top 20 models based on total_revenues
(
    df.groupby(
        by="model"
    )
    .aggregate(
        func={"total_revenue": np.sum}
    )
    .sort_values(
        by="total_revenue",
        ascending=False
    )
    .iloc[
        0:20
    ]
)

# Unique / Distinct Values -------------------------------------------

# Find all unique combinations of model, category 1, and category 2
# We use a df method drop.duplicates()
# There are 97 unique combos of those three factors
df[["model", "category_1", "category_2"]].drop_duplicates()

# Return unique array of cities
df.city.unique()

# Top / Bottom -------------------------------------------

# Get the top 10 largest total_revenues
df.nlargest(n=10, columns=["total_revenue"])

# Get the bottom 10 smallest total_revenues
df.nsmallest(n=10, columns=["total_revenue"])

# Sampling Rows -------------------------------------------

# Randomly select 10 rows
# The random_state arg is similar to set.seed() in R
df.sample(
    n=10
)

# Randomly select 5 percent of total rows
df.sample(
    frac=0.05
)

# 4.0 ADDING CALCULATED COLUMNS (MUTATING) -------------------------------------------

# Create a copy
df2 = df.copy()

# Method 1 - Series Notations -------------------------------------------

# Create a new column using series assignment
df2["total_revenue_new"] = df2.total_revenue / 100
df2
# This type of mutation uses series
# Series notation does not support method chaining
type(df2["total_revenue_new"])

# Method 2 - assign (Great for method chaining) -------------------------------------------

# Using the assign() DataFrame method
# Also using an anonymous function
(
    df2.assign(
        frame_material_lower=lambda x: x["frame_material"].str.lower()
    )
)

# Practice log transformation -------------------------------------------
# Histogram of log prices
(
    df[["model", "price"]].drop_duplicates()
    # Overwrite price column
    .assign(price=lambda x: np.log(x["price"]))
    .hist()
)

# Adding Flags (True/False) -------------------------------------------

# Create a new factor
df2 = df2.assign(
    flag_supersix=lambda x: x["model"].str.contains("Supersix")
)

# Count the number of occurrences of "super six"
np.sum(
    df2["flag_supersix"]
)

# Even Width Binning -------------------------------------------

# Create groups based on price range
# This is a dtype: category, which is similar to R's factor
# The three levels are: low, medium, and high
df2[["price_range"]] = pd.cut(
    df.price,
    bins=3,
    labels=["low", "medium", "high"]
)
# The Dtype for this variable is indeed category
df2.info()

# A use case of categorical data is to use it to create a binning
# Create a heat table
# This shows that even width binning may not fit the price data
# The price data is not uniformly distributed
(
    df2[["model", "price"]].drop_duplicates()
    .assign(
        price_group=lambda x: pd.cut(
            x["price"],
            bins=3,
            labels=["low", "medium", "high"]
        )
    )
    .pivot(
        index="model",
        columns="price_group",
        values="price"
    )
    .style.background_gradient(
        cmap="Blues"
    )
)

# Quantile Binning -------------------------------------------

# This is a quantile-based discretization function
pd.qcut(
    x=df2.price,
    # Could be an array of quantiles
    # Could also be int like 10 for deciles and 4 for quartiles
    q=4,
    labels=[
        "first_quartile",
        "second_quatile",
        "third_quartile",
        "fourth_quatile"
    ]
)
# Create a new variable called "quantiles"
# The do a frequency count of how many rows fall into each quartile
(
    df2[["model", "price"]].drop_duplicates()
    .assign(
        quantile=lambda x: pd.qcut(
            x=x.price,
            q=4,
            labels=[
                "first_quartile",
                "second_quatile",
                "third_quartile",
                "fourth_quatile"
            ]
        )
    )
    .groupby(
        by="quantile"
    )
    .aggregate(
        func={"quantile": np.size}
    )
)
# Lastly, we can recreated the heat table
(
    df2[["model", "price"]].drop_duplicates()
    .assign(
        quantile=lambda x: pd.qcut(
            x=x.price,
            q=4,
            labels=[
                "first_quartile",
                "second_quatile",
                "third_quartile",
                "fourth_quatile"
            ]
        )
    )
    .pivot(
        index="model",
        columns="quantile",
        values="price"
    )
    .style.background_gradient(
        cmap="Blues"
    )
)

# 5.0 GROUPING  -------------------------------------------

# 5.1 Aggregations (No Grouping)
# Aggregation functions take a series and return a single value
# Transformation functions take a series and return a new series of the same length
df.total_revenue.sum()
# Or using [[]], which returns a series
# Convert returned series to data frame
df[["total_revenue"]].sum().to_frame()

# Select only the numeric columns
(
    df.select_dtypes(
        exclude=["object"]
    )
    .drop("order_date", axis=1)
    # This is a short hand for df.aggregate(np.sum)
    .sum()
)

# Using aggregate() method allows for multiple aggregation functions
# It also allows for targeting columns using dictionaries
(
    df.select_dtypes(
        exclude=["object"]
    )
    .drop(
        columns=[
            "order_line",
            "order_date",
            "order_id"
        ]
    )
    .aggregate(
        {
            "quantity": [np.sum, np.std, np.mean],
            "price": np.std,
            "total_revenue": np.mean
        }
    )
)

# Common Summaries -------------------------------------------

# Descriptive stats
df.describe()

# Frequency counts
df[["model"]].value_counts()
# Two factors
# Get count per combination of these two factors
df[["model", "category_1"]].value_counts()

# Find the number of unique elements in each column
df.nunique()

# Missingness
df.isna()
df.isnull()
# Count the number of missing values (TRUE's)
df.isna().sum()
df.isnull().sum()

# Shape of data
# Returns a tuple of the numbers of rows and columns
df.shape

# 5.2 Groupby + Agg -------------------------------------------

# Group by city and state
# Compute the sum and mean for quantity
# Compute the sum for total revenue
# This makes a multi-level column
# Total revenue and quantity at the highest level
# Then statistics type--- sum and/or mean--- at the second level
(
    df.groupby(
        by=[
            "city",
            "state"
        ]
    )
    .aggregate(
        {
            "total_revenue": np.sum,
            "quantity": [np.sum, np.mean]
        }
    )
)

# Get the sum and median by groups -------------------------------------------
summary_df_1 = pd.DataFrame(
    df[[
        "category_1", "category_2", "total_revenue"
    ]].groupby(
        by=["category_1", "category_2"]
    )
    .aggregate(
        func=[np.sum, np.median]
    )
    # Return grouped indices (category 1 and 2) as columns
    .reset_index()
)
print(summary_df_1.shape)

# Apply Summary Functions to Specific Columns -------------------------------------------
summary_df_2 = (
    df[[
        "category_1", "category_2",
        "total_revenue", "quantity"
    ]].groupby(
        by=["category_1", "category_2"]
    )
    .aggregate(
        dict(
            quantity=np.sum,
            total_revenue=np.sum
        )
    )
    .reset_index()
)
print(summary_df_2.shape)

# Detecting NA -------------------------------------------
summary_df_1.isna().sum().index

# There is multiindex
summary_df_1.columns


# 5.3 Groupby + Transform -------------------------------------------
# - Note: Groupby + Assign does not work. No assign method for groups.
summary_df_3 = (
    df[[
        "order_date", "category_2",
        "total_revenue", "quantity"
    ]].set_index(
        "order_date"
    )
    .groupby(
        by=["category_2"]
    )
    # Convert to weekly frequency
    .resample(
        rule="W",
        # Start of the week
        convention="start"
    )
    .aggregate(
        dict(
            total_revenue=np.sum,
            quantity=np.sum
        )
    )
    .reset_index()
)
summary_df_3 = pd.DataFrame(summary_df_3)

# Group by and apply to one column -------------------------------------------
(
    summary_df_3.set_index(
        "order_date"
    )
    .groupby(
        "category_2"
    )
    # Each "x" is a grouped/ nested data frame
    # Apply anonymous function to each grouped data frame
    # This is similar to purrr::map_df()
    .apply(
        lambda x: (x.total_revenue - x.total_revenue.mean())
        / x.total_revenue.std()
    )
    .reset_index()
    # Long to wide
    .pivot(
        index="order_date",
        columns="category_2",
        values="total_revenue"
    )
    .plot()
)

# Group by and apply to multiple columns -------------------------------------------
(
    summary_df_3.set_index(
        ["order_date", "category_2"]
    )
    .groupby(
        by="category_2"
    )
    # Each "x" is a grouped data frame
    # We are not targeting just total_revenue but also quantity
    # So we do not specify x.variable like we did previously
    .apply(
        lambda x: (x - x.mean()) / x.std()
    )
    .reset_index()
)

# 5.4 Groupby + Filter

# Last five obs for each group
(
    summary_df_3.groupby(
        ["category_2"]
    )
    .tail(n=5)
)

# Select the first 20 rows for each group and all columns
(
    summary_df_3.groupby(
        ["category_2"]
    )
    .apply(
        lambda x: x.iloc[1:20, :]
    )
)

# Skip 2 rows time for each group
(
    summary_df_3.groupby(
        ["category_2"]
    )
    .apply(
        # Skip 2 rows and select all columns
        lambda x: x.iloc[::3, :]
    )
)

# Select from the 10th row to the 15th row for each group
(
    summary_df_3.groupby(
        ["category_2"]
    )
    .apply(
        # Skip 2 rows and select all columns
        lambda x: x.iloc[10:16, :]
    )
)


# 6.0 RENAMING -------------------------------------------

summary_df_2

# Using anonymous function -------------------------------------------
(
    summary_df_2.rename(
        # Each x will be a column name
        columns=lambda x: x.replace(
            "_",
            " "
        )
        # Convert strings in series/index to titlecase
        .title(),
        inplace=False
    )
)
# The lambda function utilizes string methods
"string_2".replace("_", " ").title()

# Targeting specific columns -------------------------------------------
(
    summary_df_2.rename(
        columns={
            "total_revenue": "Total Revenue",
            "quantity": "Total Quantity",
            "category_1": "Cat 1",
            "category_2": "Cat 2"
        },
        inplace=False
    )
)

# - Multi-Index -------------------------------------------

# This data frame has multi-index
# Stacked with levels
summary_df_1

# The index object is a list container referencing tuples which reference other objects
summary_df_1.columns
# Each tuple in this MultiIndex object has two elements
for tup in summary_df_1.columns:
    print(len(tup))
# One element is level 1 index and the other is level 2 (e.g. mean and std)
# We use list comprehension to create a list to replace the multi-level index
# The method join() is a str method that can join strings (the two elements in each tuple)
# The rstrip() method removes any trailing characters (characters at the end of a string)
# The opposite is lstrip() which removes leading characters
# For both, space is the default trailing character to remove
[
    "_".join(col).rstrip("_") for col in summary_df_1.columns.tolist()
]
# Suppose we wish to flatten the stacked multi-level index
# The multi-level index should now be flattened
(
    summary_df_1.set_axis(
        # The labels takes list-like inputs
        # We use a list comprehension to create a list to supply here
        labels=[
            "_".join(col).rstrip("_") for col in summary_df_1.columns.tolist()
        ],
        axis=1,
        inplace=False
    )
)


# 7.0 RESHAPING (MELT & PIVOT_TABLE) -------------------------------------------

# Aggregate Revenue by Bikeshop by Category 1
bikeshop_revenue_df = pd.DataFrame(
    df[["bikeshop_name", "total_revenue", "category_1"]]
    .groupby(
        by=["bikeshop_name", "category_1"]
    )
    .aggregate(
        {"total_revenue": np.sum}
    )
    .reset_index()
    .sort_values(
        by="total_revenue",
        ascending=False
    )
    .rename(
        columns=lambda x: x.replace(
            "_",
            " "
        )
        .title()
    )
)
# Examine shape
bikeshop_revenue_df.shape
# Descriptive stats
bikeshop_revenue_df.describe()

# 7.1 Pivot & Melt -------------------------------------------

# Pivot (Pivot Wider) -------------------------------------------
bikeshop_revenue_wide_df = pd.DataFrame(
    bikeshop_revenue_df
    .pivot(
        index=["Bikeshop Name"],
        columns=["Category 1"],
        values=["Total Revenue"]
    )
    .reset_index()
    .set_axis(
        labels=["Bikeshop Name", "Mountain", "Road"],
        axis=1,
        inplace=False
    )
)
# Examine shape
bikeshop_revenue_wide_df.shape

# Create stylized pandas table using styler and format methods -------------------------------------------
(
    bikeshop_revenue_wide_df.sort_values(
        by=["Mountain"],
        ascending=False
    )
    .style.highlight_max()
    .format(
        {
            # Each x is a column (Series) specified by "variable"
            "Mountain": lambda x: f'${x}',
            "Road": lambda x: f'${x}'
        }
    )
)
# Another option
(
    bikeshop_revenue_wide_df.sort_values(
        by=["Mountain"],
        ascending=False
    )
    .style.highlight_max()
    .format(
        {
            # Add dollar sign up front and comma separators
            "Mountain": "${:,}",
            "Road": "${:,}"
        }
    )
)
# Another option
(
    bikeshop_revenue_wide_df.sort_values(
        by=["Mountain"],
        ascending=False
    )
    .style.highlight_max()
    .format(
        {
            # Use anonymous function and formating
            "Mountain": lambda x: "$" + "{:,}".format(x),
            "Road": lambda x: "$" + "{:,}".format(x)
        }
    )
)
# Yet, another possibility using the mizani package
# Create a dollar formatter
usd = dollar_format(
    prefix="$",
    big_mark=","
)
# Test this formatter
# This formatter returns a list object so we would need to extract the formatted str elements
for num in usd(pd.Series([23232, 2322365323, 232323])):
    print(num)
# Format using this formatter
(
    bikeshop_revenue_wide_df.sort_values(
        by=["Mountain"],
        ascending=False
    )
    .style.highlight_max()
    .format(
        {
            # Use anonymous function and formating
            "Mountain": lambda x: usd([x])[0],
            "Road": lambda x: usd([x])[0]
        }
    )
    #    .to_excel(
    # "./03_pandas_core/bikeshop_revenue_wide.xlsx"
    #    )
)


# Melt (Pivoting Longer) -------------------------------------------

# Suppose we read in data that is wide
# Convert from wide to long
bikeshop_revenue_long_df = pd.DataFrame(
    pd.read_excel(
        "./03_pandas_core/bikeshop_revenue_wide.xlsx"
    )
    # Select all rows but start from column 2 and not the first 0 indexed "unnamed" column
    .iloc[:, 1:]
    # Pivot longer
    .melt(
        id_vars="Bikeshop Name",
        value_vars=["Mountain", "Road"],
        var_name="Category 1",
        value_name="Total Revenue"
    )
    .sort_values(
        by="Total Revenue",
        ascending=False
    )
)
# Examine shape
# This should match what it was before we reshaped by pivoting wider
bikeshop_revenue_df.shape
# Descriptive stats
bikeshop_revenue_df.describe()

# Bikeshop name in terms of total revenue in descending order
# This is a List object
bikeshop_order = (
    bikeshop_revenue_long_df.groupby(
        by=["Bikeshop Name"]
    )
    .aggregate(
        {
            "Total Revenue": np.sum
        }
    )
    .sort_values(
        by=["Total Revenue"],
        ascending=False
    )
    # Get the attribute--- the index object
    .index
    # Convert index object to list
    # This is the order of the bikeshop name sorted in terms of revenue
    .tolist()
)
# Create category in the same order as the list object above
bikeshop_revenue_long_df["Bikeshop Name"] = pd.Categorical(
    bikeshop_revenue_long_df["Bikeshop Name"],
    # Specify the unique categories for this categorical variable
    categories=bikeshop_order
)
bikeshop_revenue_long_df.info()

# Create a plot
(
    ggplot(
        data=bikeshop_revenue_long_df,
        mapping=aes(
            x="Bikeshop Name",
            y="Total Revenue",
            fill='Category 1'
        )
    ) +
    geom_col() +
    coord_flip() +
    facet_wrap("Category 1") +
    labs(
        x="Bikeshop Name",
        y="Total Revenue (USD)",
        title="Total Revenue by Bike Type"
    ) +
    theme(
        panel_grid=element_blank(),
        panel_background=element_rect(fill="white"),
        legend_position="none"
    )
)

# 7.2 Pivot Table (Pivot + Summarization, Excel Pivot Table) -------------------------------------------
(
    df.pivot_table(
        values=["total_revenue"],
        index=["category_1"],
        columns=["frame_material"],
        aggfunc=np.sum
    )
)
# Two indices similar to Tableau when you add granularity
(
    df.pivot_table(
        values=["total_revenue"],
        index=["category_1", "frame_material"],
        columns=None,
        aggfunc=np.sum
    )
)

# Create a year variable
# Sales by categories

# Two indices similar to Tableau when you add granularity
# The two categories are dimensions and revenue is the numerical data
# The sum function is used to aggregate
sales_by_categories_and_year = pd.DataFrame(
    df.assign(
        # Use the dt accessor to extrat the year from the data variable
        year=lambda x: x.order_date.dt.year
    )
    .pivot_table(
        values=["total_revenue"],
        index=["category_1", "category_2"],
        columns="year",
        aggfunc=np.sum
    )
)

# 7.3 Stack & Unstack -------------------------------------------

# Unstack - Pivots Wider 1 Level (Pivot)
(
    sales_by_categories_and_year.unstack(
        # Specify the column to pivot wider
        # This can also be 0, 1, ....
        # Where 0 is the outermost column and so on so forth
        level="category_1",
        # If there are NaN's, replace those with 0
        fill_value=0
    )
)

# Stack - Pivots Longer 1 Level (Melt)
(
    sales_by_categories_and_year.stack(
        level="year",
        dropna=False
    )
)
# We can combine stack and unstack to transpose a data frame
(
    sales_by_categories_and_year.stack(
        level="year",
        dropna=False
    )
    .unstack(
        level=["category_1", "category_2"],
        fill_value=0
    )
)
# Compare the above pivot tables to the original
# Year was wide but is now long
# The categories were indices but are now wide
sales_by_categories_and_year

# 8.0 JOINING DATA -------------------------------------------

# Read in raw data
orderline_df = (
    pd.read_excel(
        "./00_data_raw/orderlines.xlsx"
    )
    # Start indexing from second column
    # We drop the first "unnamed" column
    # Keep all rows
    .iloc[:, 1:]
)
bikes_df = (
    pd.read_excel(
        "./00_data_raw/bikes.xlsx"
    )
)


# Merge (Joining) -------------------------------------------
# Left join bikes_df onto order_line_df
left_joined = (
    orderline_df.merge(
        right=bikes_df,
        how="left",
        left_on="product.id",
        right_on="bike.id"
    )
)
# Right join but same results
right_joined = (
    bikes_df.merge(
        right=orderline_df,
        how="right",
        left_on="bike.id",
        right_on="product.id"
    )
)
# Reorder the left joined data frame to match the right joined data frame
right_joined.columns.tolist()
# Select from the left joined data frame in the order above
left_joined = left_joined[right_joined.columns.tolist()]
# Now compare the left-and-right joined data frames
# All True's and so the two data frame are the same
(right_joined == left_joined).sum()
# Another to check for equality is using the method
right_joined.equals(left_joined)


# Concatenate (Binding) -------------------------------------------

# Columns -------------------------------------------
# Middle column is ?
middle = int(left_joined.shape[1] / 2)
# Split the data frame in half column-wise
left_half = left_joined.iloc[:, :middle]
right_half = left_joined.iloc[:, middle:]
# Now column bind the two halves to get the original data frame back
# Ensure the two df's have the same row index or there would be NaN's
col_bind = pd.concat(
    [left_half, right_half],
    axis=1
)
# This new data frame should be the same as the original
col_bind.equals(left_joined)

# Rows -------------------------------------------
# Middle row is
middle = int(left_joined.shape[0] / 2)
# Split data frame in half row-wise
top_half = left_joined.iloc[:middle, :]
bottom_half = left_joined.iloc[middle:, :]
# Now row bind the two halves
row_bind = pd.concat(
    [top_half, bottom_half]
)
# Check for equality
row_bind.equals(left_joined)

# 9.0 SPLITTING (SEPARATING) COLUMNS AND COMBINING (UNITING) COLUMNS -------------------------------------------

# Separate -------------------------------------------
(
    df.order_date.astype(
        "str"
    )
    .str.split(
        pat="-",
        # Expand the split strings into separate columns
        expand=True,
    )
    .rename(
        columns={
            0: "year",
            1: "month",
            2: "day"
        }
    )
)
# Another way to rename the columns is to use set_axis()
date_data = pd.DataFrame(
    df.order_date.astype(
        "str"
    )
    .str.split(
        pat="-",
        # Expand the split strings into separate columns
        expand=True,
    )
    .set_axis(
        labels=[
            "year",
            "month",
            "day"
        ],
        axis=1,
        inplace=False
    )
)
date_data

# Combine -------------------------------------------
# Initialize a data frame
date_date2 = pd.DataFrame()
# Combine columns into one
date_date2["order_date"] = (
    date_data[[
        "year",
        "month",
        "day"
    ]].aggregate(
        "-".join,
        axis=1
    )
)
# Now this date column is a string
date_date2.info()
# Convert string to datetime object
date_date2.order_date = pd.to_datetime(
    date_date2.order_date,
)
# Now the date column should be a datetime object
date_date2.info()

# 10.0 APPLY -------------------------------------------
# Create a data frame to practice
sales_by_category2_daily = pd.DataFrame(
    df[["category_2", "order_date", "total_revenue"]]
    .set_index(
        ["order_date"]
    )
    .groupby(
        by=["category_2"]
    )
    # Sample up to daily frequency
    .resample(
        rule="D"
    )
    .aggregate(
        {
            "total_revenue": np.sum
        }
    )
)
sales_by_category2_daily

# Aggregation takes a series and returns a single value
sales_by_category2_daily.apply(
    func=np.mean
)
# Transformation takes a series and returns a series of the same length
sales_by_category2_daily.apply(
    # Each x is column
    # Since category_2 and order_date are not numeric, it is just total revenue
    func=lambda x: x ** 2
)

# Broadcasting is the methodology adopted in NumPy used to
# perform arithmetic operations on arrays with differing dimensions.
# General arithmetic operations such as addition,
# multiplication, subtraction, etc. tend to broadcast arrays
# before performing the operations on arrays with variations in size.
sales_by_category2_daily.apply(
    func=np.mean,
    result_type="broadcast"
)
# This is equivalent to
sales_by_category2_daily.apply(
    # Each x is a series
    func=lambda x: np.repeat(
        # The aggregation function takes the revenue series
        # It returns a single value
        a=np.mean(x),
        # Repeat the single mean value this many times
        # Then fill the places instead of using 0
        repeats=len(x)
    )
)

# Apply function by group
# Compute mean revenue by group
(
    sales_by_category2_daily.groupby(
        by=["category_2"]
    )
    .apply(
        func=np.mean
    )
)
# Broadcasting by group
(
    sales_by_category2_daily.groupby(
        by=["category_2"]
    )
    .apply(
        # Each x is a data frame belonging to one group
        # In the above example we had one single "ungrouped" data frame
        func=lambda x: np.repeat(
            a=np.mean(x),
            repeats=len(x)
        )
    )
)
# Another solution that does not involve losing the order date column
(
    sales_by_category2_daily.groupby(
        by=["category_2"]
    )
    .transform(
        # This passes each grouped column to the function np.mean
        # That is, the revenue series column rather than the data frame
        # So transform() returns the other columns not passed to the aggregation function
        func=np.mean
    )
)


# 11.0 PIPE -------------------------------------------
# - Functional programming helper for "data" functions

# Create a function that adds a column
def add_col(data, **kwargs):
    # Make a copy
    data_copy = data.copy()
    # Create new column
    # The kwargs are key-value pairs, which are stored as dictionaries
    # The user supply the expressions {new_var = ...} as kwargs
    # Then, this kwargs expression is stored as a dictionary
    # Finally, the dictionary is supplied to pd.DataFrame
    data_copy[list(kwargs.keys())] = pd.DataFrame(
        kwargs
    )
    # Output
    return data_copy


# See it in action
add_col(
    data=df,
    rescaled_revenue=df.total_revenue / 100
)

# The pipe method allows for using custom "data function" in method chain
# A "data function" takes a data frame as its first argument and returns a data frame
(
    df.pipe(
        func=add_col,
        # This is the argument to add_col()
        rescaled_revenue=df.total_revenue / 100
    )
    .sort_values(
        by=["rescaled_revenue"],
        ascending=False
    )
)
# Another example
(
    df.pipe(
        func=add_col,
        # This is the argument to add_col()
        lower_case_cat=df.category_2.str.lower()
    )
    # Select the last column, which is our created column
    .iloc[
        :, -1
    ]
)
