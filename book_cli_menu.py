# book_cli_menu.py
import json
from book_service import (
    get_all_books, get_book_by_isbn, add_book, validate_book_data, update_book_by_isbn,
    delete_book_by_isbn, search_books, get_books_by_author, get_random_book, initialize_db
)


def display_menu():
    print("\n----- Book Service CLI -----")
    print("1. Get all books")
    print("2. Get a book by ISBN")
    print("3. Add a book")
    # Add other functions as needed...
    print("4. Search for books")
    print("5. Get a random book")
    print("0. Exit")
    choice = input("\nSelect an option: ")
    return choice


def main():
    while True:
        choice = display_menu()

        if choice == "1":
            books = get_all_books()
            print(json.dumps(books, indent=4))
        elif choice == "2":
            isbn = input("Enter the ISBN of the book: ")
            book = get_book_by_isbn(isbn)
            if book:
                print(json.dumps(book, indent=4))
            else:
                print(f"No book found with ISBN {isbn}.")
        elif choice == "3":
            book_data_str = input("Enter the book data in JSON format: ")
            book_data = json.loads(book_data_str)
            validate_book_data(book_data)
            book_id = add_book(book_data)
            print(f"Added book with ID: {book_id}")
        elif choice == "4":
            query = input("Enter your search query: ")
            books = search_books(query)
            print(json.dumps(books, indent=4))
        elif choice == "5":
            book = get_random_book()
            print(json.dumps(book, indent=4))
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
