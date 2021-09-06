# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# SQL DATABASES (Module 2): Working with SQLAlchemy ----

# IMPORTS ----

# Import packages
import pandas as pd
import sqlalchemy as sql
import os

# Create a database directory under the root project directory
os.mkdir(path="00_database")

# CREATING A DATABASE ----

# Instatiate a database
# Four initial slashes in total plus one more to point it to the file location
# Generally, "create_engine('sqlite:////absolute/path/to/foo.db')"
engine = sql.create_engine(
    f'sqlite://///{os.getcwd()}/00_database/bike_orders_database.sqlite'
)

# Create connection object
# The engine is now a class of the sqlite database
# This is file databse, where it is permanent
# There is also in-memory database, which is temporary
conn = engine.connect()

# Read Excel Files
bikes_df = pd.DataFrame(pd.read_excel("./00_data_raw/bikes.xlsx"))
bikeshops_df = pd.DataFrame(pd.read_excel("./00_data_raw/bikeshops.xlsx"))
orderlines_df = pd.DataFrame(pd.read_excel("./00_data_raw/orderlines.xlsx"))


# Create Tables
# Bikes table
bikes_df.to_sql(
    name="bikes",
    con=conn
)
# Check to see if bikes table has been created
# Use SELECT * FROM statement
pd.read_sql(
    sql="SELECT * FROM bikes",
    con=conn
)

# Bikeshop table
bikeshops_df.to_sql(
    name="bikeshops",
    con=conn
)
# Check to see if bikes table has been created
# Use SELECT * FROM statement
pd.read_sql(
    sql="SELECT * FROM bikeshops",
    con=conn
)

# Orderlines table
# Exclude the "unamed 0" column
# Use ":" to include all rows or columns
orderlines_df.iloc[:, 1:].to_sql(
    name="orderlines",
    con=conn,
    # Repace the existing table
    if_exists="replace"
)
# Check to see if bikes table has been created
# Use SELECT * FROM statement
pd.read_sql(
    sql="SELECT * FROM orderlines",
    con=conn
)

# Close Connection
# Good practice to close connection when finish reading/writing data
# Only connect when necessary
conn.close()

# RECONNECTING TO THE DATABASE

# Connecting is the same as creating
engine = sql.create_engine(
    f'sqlite://///{os.getcwd()}/00_database/bike_orders_database.sqlite'
)
conn = engine.connect()

# GETTING DATA FROM THE DATABASE

# Get the table names
# This function is deprecated
engine.table_names()

# Another way to get table names by creating inspector object
inspector = sql.inspect(conn)
# Get scheme names
# SQL schema as a logical collection of database objects
inspector.get_schema_names()
# Get table names
inspector.get_table_names("main")

# Read the data
# Create a list of names (three str elements)
table = inspector.get_table_names("main")
# Read tables
pd.read_sql(
    sql=f'SELECT * FROM {table[0]}',
    con=conn
)
pd.read_sql(
    sql=f'SELECT * FROM {table[1]}',
    con=conn
)
pd.read_sql(
    sql=f'SELECT * FROM {table[2]}',
    con=conn
)

# Close conenction
conn.close()
