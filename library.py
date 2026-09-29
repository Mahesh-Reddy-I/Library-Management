from models import Book
from datetime import date, timedelta

class Library:
    def __init__(self, connection):
        self.connection = connection

    def add_book(self, title, author, isbn, total_copies):
        cursor = self.connection.cursor()
        query = """
            INSERT INTO books (title, author, isbn, total_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (title, author, isbn, total_copies, total_copies))
        self.connection.commit()
        cursor.close()
        print(f"Added book: {title}")

    def search_book(self, keyword):
        cursor = self.connection.cursor()
        query = """
            SELECT id, title, author, isbn, total_copies, available_copies
            FROM books
            WHERE title LIKE %s OR author LIKE %s
        """
        like_pattern = f"%{keyword}%"
        cursor.execute(query, (like_pattern, like_pattern))
        rows = cursor.fetchall()
        cursor.close()
        return [Book(*row) for row in rows]

    def list_books(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title, author, isbn, total_copies, available_copies FROM books")
        rows = cursor.fetchall()
        cursor.close()
        return [Book(*row) for row in rows]

    def issue_book(self, book_id, member_name, loan_days=14):
        cursor = self.connection.cursor()

        # Check availability
        cursor.execute("SELECT available_copies FROM books WHERE id = %s", (book_id,))
        result = cursor.fetchone()
        if not result or result[0] <= 0:
            cursor.close()
            print("No copies available for this book.")
            return

        issue_date = date.today()
        due_date = issue_date + timedelta(days=loan_days)

        # Insert transaction
        cursor.execute("""
            INSERT INTO transactions (book_id, member_name, issue_date, due_date)
            VALUES (%s, %s, %s, %s)
        """, (book_id, member_name, issue_date, due_date))

        # Decrease available copies
        cursor.execute("""
            UPDATE books SET available_copies = available_copies - 1 WHERE id = %s
        """, (book_id,))

        self.connection.commit()
        cursor.close()
        print(f"Issued book {book_id} to {member_name}, due {due_date}")

    def return_book(self, transaction_id, fine_per_day=5):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT book_id, due_date, return_date FROM transactions WHERE id = %s
        """, (transaction_id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            print("Transaction not found.")
            return
        book_id, due_date, return_date = result
        if return_date:
            cursor.close()
            print("This book has already been returned.")
            return

        today = date.today()
        fine = 0
        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * fine_per_day

        cursor.execute("""
            UPDATE transactions SET return_date = %s, fine_amount = %s WHERE id = %s
        """, (today, fine, transaction_id))

        cursor.execute("""
            UPDATE books SET available_copies = available_copies + 1 WHERE id = %s
        """, (book_id,))

        self.connection.commit()
        cursor.close()
        print(f"Book returned. Fine: ₹{fine}")
    def view_overdue(self):
        cursor = self.connection.cursor()
        query = """
            SELECT t.id, b.title, t.member_name, t.due_date
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            WHERE t.return_date IS NULL AND t.due_date < %s
        """
        cursor.execute(query, (date.today(),))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            print("No overdue books.")
            return

        print("Overdue books:")
        for row in rows:
            transaction_id, title, member_name, due_date = row
            print(f"  [{transaction_id}] '{title}' — {member_name}, was due {due_date}")