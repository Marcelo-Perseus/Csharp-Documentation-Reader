# Csharp-Documentation-Reader
### Version: 1.0.0
A tool for reading C# documentation and for keeping track of what I've
already read.

## Long Description
---
This project is a tool that I use to track progress working through the
long C# documentation master PDF found by exploring microsoft.com's
C# documentation page. To start, it looped through the PDF outline
manually and determined links to each page, then populated a local
SQLite database with the article titles and their page bounds within
the overall master documentation PDF. The main script
"load_next_article.py" will check to see what the next article in the
database is and will automatically load it and mark the already existing
one as read before deleting the PDF. The database is not included in
the repository.

## Development
---

### Built With

1. sqlite3
2. codecs
3. PyPDF2
4. os

### Versioning

#### 1.0.0

Initial commit with basic program functionality.

## License
---
MIT License