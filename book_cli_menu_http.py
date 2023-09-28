import json
import requests
from config import PORT

BASE_URL = f"http://127.0.0.1:{PORT}"

def display_menu():
    print("\n----- Book Service CLI -----")
    print("1. Get all books")
    print("2. Get a book by ISBN")
    print("3. Add a book")
    print("4. Search for books")
    print("5. Get a random book")
    print("0. Exit")
    choice = input("\nSelect an option: ")
    return choice

def main():
    while True:
        choice = display_menu()

        if choice == "1":
            response = requests.get(f"{BASE_URL}/books")
            books = response.json()
            print(json.dumps(books, indent=4))

        elif choice == "2":
            isbn = input("Enter the ISBN of the book: ")
            response = requests.get(f"{BASE_URL}/books/isbn/{isbn}")
            if response.status_code == 200:
                book = response.json()
                print(json.dumps(book, indent=4))
            else:
                print(f"No book found with ISBN {isbn}.")

        elif choice == "3":
            book_data_str = input("Enter the book data in JSON format: ")
            book_data = json.loads(book_data_str)
            response = requests.post(f"{BASE_URL}/books", json=book_data)
            if response.status_code == 201:
                book_id = response.json().get('_id')
                print(f"Added book with ID: {book_id}")
            else:
                print("Error adding the book:", response.json().get('error'))

        elif choice == "4":
            query = input("Enter your search query: ")
            response = requests.get(f"{BASE_URL}/books/search", params={'q': query})
            books = response.json()
            print(json.dumps(books, indent=4))

        elif choice == "5":
            response = requests.get(f"{BASE_URL}/books/random")
            book = response.json()
            print(json.dumps(book, indent=4))

        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
