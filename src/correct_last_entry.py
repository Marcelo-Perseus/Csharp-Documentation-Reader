import sqlite3

# Connect to the database
conn = sqlite3.connect("Projects/C# Documentation Scraper/res/database.db")
cur = conn.cursor()

# Correct the final page
sql = """
    UPDATE Article
    SET end_page = 1929
    WHERE id = 621
"""
cur.execute(sql)

# Commit the change
conn.commit()