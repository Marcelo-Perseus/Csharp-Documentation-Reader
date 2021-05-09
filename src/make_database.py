'''
Information
-----------
Author: Marcelo Luciano
Organization: Perseus

Summary
-------
Builds up the database with a table called Article that will hold
information pertaining to a particular article in the master
documentation PDF.

Imports
-------
sqlite3
    For interacting with a local SQLite database.
'''

import sqlite3

# Define a project folder
proj_folder = "Projects/Csharp-Documentation-Reader"

# Connect to / create the database
conn = sqlite3.connect(f"{proj_folder}/res/database.db")

# Create the actual table
sql  = """
    CREATE TABLE Article (
        id integer PRIMARY KEY,
        title text NOT NULL,
        start_page integer NOT NULL,
        end_page integer NOT NULL,
        read bool DEFAULT 0
    )
"""
conn.execute(sql)

# Note: Changes don't need to be committed when the table is created.
# Changes only need to be committed when data is added or removed from
# the table.