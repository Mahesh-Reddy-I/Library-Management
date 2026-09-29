class Book:
    def __init__(self, id, title, author, isbn, total_copies, available_copies):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = available_copies
    def __str__(self):
        return f"[{self.id}] {self.title} by {self.author} — {self.available_copies}/{self.total_copies} available"
class Transaction:
    def __init__(self, id, book_id, member_name, issue_date, due_date, return_date=None, fine_amount=0):
        self.id = id
        self.book_id = book_id
        self.member_name = member_name
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date
        self.fine_amount = fine_amount
    def __str__(self):
        status = "Returned" if self.return_date else "Issued"
        return f"[{self.id}] Book {self.book_id} → {self.member_name} ({status}, due {self.due_date})"