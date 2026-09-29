from db import get_connection
from library import Library

def print_menu():
    print("\n===== Library Management System =====")
    print("1. Add Book")
    print("2. Search Book")
    print("3. List All Books")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. View Overdue Books")
    print("7. Exit")

def main():
    connection = get_connection()
    if connection is None:
        print("Could not connect to database. Exiting.")
        return

    library = Library(connection)

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                isbn = input("ISBN: ").strip()
                copies = int(input("Total copies: ").strip())
                library.add_book(title, author, isbn, copies)

            elif choice == "2":
                keyword = input("Search by title or author: ").strip()
                results = library.search_book(keyword)
                if not results:
                    print("No books found.")
                for book in results:
                    print(book)

            elif choice == "3":
                books = library.list_books()
                if not books:
                    print("No books in the library.")
                for book in books:
                    print(book)

            elif choice == "4":
                book_id = int(input("Book ID to issue: ").strip())
                member_name = input("Member name: ").strip()
                library.issue_book(book_id, member_name)

            elif choice == "5":
                transaction_id = int(input("Transaction ID to return: ").strip())
                library.return_book(transaction_id)

            elif choice == "6":
                library.view_overdue()

            elif choice == "7":
                print("Goodbye!")
                connection.close()
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input — please enter numbers where expected.")
        except Exception as e:
            print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()