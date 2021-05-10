"""
Information
-----------
Author: Marcelo Luciano
Organization: Perseus

Summary
-------
The purpose of this script is to display the progress of the reading
using a progress bar displayed in the terminal when the script is run.

Imports
-------
sqlite3
    For interacting with a local SQLite database.
"""

import sqlite3

# Define the project folder location.
proj_folder = "Projects/Csharp-Documentation-Reader"

# Connect to the database.
conn = sqlite3.connect(f"{proj_folder}/res/database.db")
cur = conn.cursor()

# Define sql to query all elements in the table.
sql = """
    SELECT (read) FROM Article
"""
cur.execute(sql)
results = cur.fetchall()

# Calculate the percentage of articles read.
total = 0
read = 0
for result in results:
    total += 1
    read += result[0]
percentage = read / total

# Generate the string to display the progress.
num_spaces = 30
used_spaces = int(20*percentage)
progress_bar = f"[{'X'*used_spaces}{' '*(num_spaces-used_spaces)}]"

# Generate the string to display the numbers after the bar.
fraction = f"{read} / {total}"

# Create the print string
ps = f"{progress_bar} {fraction}"

# Print the printstring
print(ps)