# Library Management System (CLI)

A command-line application to manage library operations, built with Python and MySQL using object-oriented design.

## Features
- Add, search, and list books
- Issue and return books with due-date tracking
- Automatic fine calculation for overdue returns
- View all currently overdue books

## Tech Stack
- Python
- MySQL
- OOP (Book, Transaction, Library classes)

## Project Structure
library_project/
├── db.py # MySQL connection handling
├── models.py # Book and Transaction classes
├── library.py # Core business logic (Library class)
├── main.py # CLI entry point
├── schema.sql # Database schema
└── README.md

## Setup

1. Clone the repo and create a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate
   pip install mysql-connector-python
```

2. Create the database and run the schema:
```sql
   CREATE DATABASE library_db;
   -- then run schema.sql inside it
```

3. Update your MySQL credentials in `db.py`.

4. Run the app:
```bash
   python main.py
```

## Example Usage
Add Book
Search Book
List All Books
Issue Book
Return Book
View Overdue Books
Exit