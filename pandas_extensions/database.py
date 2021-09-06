# IMPORTS ----

import pandas as pd
import sqlalchemy as sql
import os
from sqlalchemy.engine import create_engine

# Collect data ----


def collect_data(
    conn_string=f'sqlite://///{os.getcwd()}/00_database/bike_orders_database.sqlite'
):
    """

    Collects and Joins bikes orderlines data.

    Args:
        conn_string ([type], optional): A sqlalchemy connection string to find the database. Defaults to f'sqlite://///{os.getcwd()}/00_database/bike_orders_database.sqlite'.

    Returns:
        Dataframe: A pandas data frame that combines data from tables:
            - bikes: Products information
            - bikeshops: Customers information
            - orderlines: Transactions information
    """
    # Body

    # 1 Connect to database

    # Engine creation
    engine = sql.create_engine(conn_string)
    # Connect to engine
    conn = engine.connect()
    # Retrieve table by hardcoding
    # This is a good idea here since the raw data will always reside in these 3 tables
    # Tables will grow but the raw data will be the same
    table_names = ['bikes', 'bikeshops', 'orderlines']
    # Initialize an empty dictionary container
    data_dict = {}
    # For loop to fill the dictionary with table key-value pairs
    # To examine keys, use data_dict.keys()
    for table in table_names:
        data_dict[table] = pd.read_sql(
            sql=f'SELECT * FROM {table}',
            con=conn
            # Drop index columns that are created
        ).drop(labels='index', axis=1)
    # Close connection
    conn.close()

    # 2 Combining tables

    joined_df = (data_dict['orderlines']
                 # Left join bikes data onto orderlines data
                 .merge(
        right=data_dict['bikes'],
        how="left",
        left_on="product.id",
        right_on="bike.id"
    )
        # Left join bikeship data on to the resultant data
        .merge(
            right=data_dict["bikeshops"],
            how="left",
            left_on="customer.id",
            right_on="bikeshop.id"
    ))

    # 3 Cleaning data
    # Subset and assignment to turn data column to date time object
    joined_df["order.date"] = pd.to_datetime(
        joined_df["order.date"]
    )
    # Now subset multiple elements and assign
    # Split description column into separate columns
    joined_df[[
        "category_1",
        "category_2",
        "frame_material"
    ]] = (joined_df["description"]
          .str.split(
        pat=" - ",
        expand=True
    ))
    # Split Location into City and State
    joined_df[[
        "city",
        "state"
    ]] = (joined_df["location"]
          .str.split(
        pat=", ",
        expand=True
    ))
    # Compute total revenue
    joined_df[
        "total_revenue"
    ] = joined_df.quantity * joined_df.price
    # Modify on copy is carried out here when we reorganize the columns
    joined_df = joined_df[[
        'order.id',
        'order.line',
        'order.date',
        'quantity',
        'price',
        'total_revenue',
        'model',
        'category_1',
        'category_2',
        'frame_material',
        'bikeshop.name',
        'city',
        'state'
    ]]
    # Replace all "." with "_"
    joined_df.columns = joined_df.columns.str.replace(
        pat=".",
        repl="_",
    )

    # 4 Return data frame
    return joined_df
