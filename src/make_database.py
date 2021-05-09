'''
Builds up the database with a table called Article that will hold
columns:

Article
-------
id          int
title       string
start_page  int
end_page    int
read        bool
'''

import sqlite3

# Connect to / create the database
conn = sqlite3.connect("Projects/C# Documentation Scraper/database.db")

# Create the actual table
conn.execute("""
             CREATE TABLE Article (
                 id integer PRIMARY KEY,
                 title text NOT NULL,
                 start_page integer NOT NULL,
                 end_page integer NOT NULL,
                 read bool DEFAULT 0
             )
             """)
print("Table successfully created")