# book_cli_menu.py
import json
from book_service import (
    get_all_books, get_book_by_isbn, add_book, validate_book_data, update_book_by_isbn,
    delete_book_by_isbn, search_books, get_books_by_author, get_random_book, initialize_db
)

def display_menu():
    print("\n----- Interface CLI du Service de Livres -----")
    print("1. Afficher tous les livres")
    print("2. Chercher un livre par ISBN")
    print("3. Ajouter un livre")
    print("4. Rechercher des livres")
    print("5. Obtenir un livre aléatoire")
    print("0. Quitter")
    choice = input("\nChoisissez une option: ")
    return choice

def main():
    while True:
        choice = display_menu()

        if choice == "1":
            try:
                books = get_all_books()
                print(json.dumps(books, indent=4))
            except Exception as e:
                print(f"Erreur: {str(e)}")

        elif choice == "2":
            isbn = input("Entrez l'ISBN du livre: ")
            try:
                book = get_book_by_isbn(int(isbn))
                if book:
                    print(json.dumps(book, indent=4))
                else:
                    print(f"Aucun livre trouvé avec l'ISBN {isbn}.")
            except Exception as e:
                print(f"Erreur: {str(e)}")

        elif choice == "3":
            book_data_str = input("Entrez les données du livre au format JSON: ")
            try:
                book_data = json.loads(book_data_str)
                book_id = add_book(book_data)
                print(f"Livre ajouté avec l'ID: {book_id}")
            except Exception as e:
                print(f"Erreur: {str(e)}")

        elif choice == "4":
            query = input("Entrez votre requête de recherche: ")
            try:
                books = search_books(query)
                print(json.dumps(books, indent=4))
            except Exception as e:
                print(f"Erreur: {str(e)}")

        elif choice == "5":
            try:
                book = get_random_book()
                print(json.dumps(book, indent=4))
            except Exception as e:
                print(f"Erreur: {str(e)}")

        elif choice == "0":
            print("Sortie...")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
