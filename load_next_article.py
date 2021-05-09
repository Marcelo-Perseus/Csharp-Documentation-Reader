import sqlite3
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

# Define the project folder
proj_folder = "Projects/C# Documentation Scraper"

# Connect to the database
conn = sqlite3.connect(f"{proj_folder}/res/database.db")
cur = conn.cursor()

def get_unread_articles():
    # Build the query
    sql = """
        SELECT * FROM Article
        WHERE read = 0
        ORDER BY id
    """

    # Execute the query
    cur.execute(sql)

    # Return the result
    return cur.fetchall()

def get_next_unread_article():
    # Get all unread articles
    articles = get_unread_articles()

    return articles[0]

# Find the next unread article
next_unread = get_next_unread_article()

# If there is a PDF, delete it and mark it as read
for filename in os.listdir(f"{proj_folder}/"):

    # Only look for PDFs
    if ".pdf" in filename:

        # Check if the file name contains the title of the next unread
        if next_unread[1] in filename:

            # Delete the file
            os.remove(f"{proj_folder}/{filename}")

            # Mark the file as read in the database
            sql = """
                UPDATE Article
                SET read = 1
                WHERE id = ?
            """
            cur.execute(sql, [next_unread[0]])

# Queue up the next article
next_unread = get_next_unread_article()
with open(f"{proj_folder}/res/C# Documentation.pdf", "rb") as f:
    master_pdf = PdfFileReader(f)
    writer = PdfFileWriter()
    for i in range(next_unread[2], next_unread[3]+1):
        page = master_pdf.getPage(i-1)
        writer.addPage(page)
    with open(f"{proj_folder}/{next_unread[1]}.pdf", "wb") as f2:
        writer.write(f2)

# Commit changes to the database
conn.commit()