"""
Information
-----------
Author: Marcelo Luciano
Organization: Perseus

Summary
-------
This file serves a single purpose as a script. It is meant to correct
an error in the output of the get_bounds.py script where the final
article entry didn't include the final page of the master file in the
listed page range.

Imports
-------
sqlite3
    For modifying a local SQLite database.
"""

import sqlite3

# Define the project folder.
proj_folder = "Projects/Csharp-Documentation-Reader"

# Connect to the database.
conn = sqlite3.connect(f"{proj_folder}/res/database.db")
cur = conn.cursor()

# Correct the final page.
sql = """
    UPDATE Article
    SET end_page = 1929
    WHERE id = 621
"""
cur.execute(sql)

# Commit the change to the database.
conn.commit()