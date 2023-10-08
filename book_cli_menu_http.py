import json
import requests
from config import PROXY_PORT

BASE_URL = f"http://127.0.0.1:{PROXY_PORT}"

def display_menu():
    print("\n----- CLI du service de livres -----")
    print("1. Obtenir tous les livres")
    print("2. Obtenir un livre par ISBN")
    print("3. Ajouter un livre")
    print("4. Rechercher des livres")
    print("5. Obtenir un livre aléatoire")
    print("0. Quitter")
    choice = input("\nSélectionnez une option: ")
    return choice

def main():
    while True:
        choice = display_menu()

        if choice == "1":
            response = requests.get(f"{BASE_URL}/books")
            books = response.json()
            print(json.dumps(books, indent=4))

        elif choice == "2":
            isbn = input("Entrez l'ISBN du livre: ")
            response = requests.get(f"{BASE_URL}/books/isbn/{isbn}")
            if response.status_code == 200:
                book = response.json()
                print(json.dumps(book, indent=4))
            else:
                print(f"Aucun livre trouvé avec l'ISBN {isbn}.")

        elif choice == "3":
            book_data_str = input("Entrez les données du livre au format JSON: ")
            book_data = json.loads(book_data_str)
            response = requests.post(f"{BASE_URL}/books", json=book_data)
            if response.status_code == 201:
                book_id = response.json().get('_id')
                print(f"Livre ajouté avec l'ID: {book_id}")
            else:
                print("Erreur lors de l'ajout du livre:", response.json().get('error'))

        elif choice == "4":
            query = input("Entrez votre requête de recherche: ")
            response = requests.get(f"{BASE_URL}/books/search", params={'q': query})
            books = response.json()
            print(json.dumps(books, indent=4))

        elif choice == "5":
            response = requests.get(f"{BASE_URL}/books/random")
            book = response.json()
            print(json.dumps(book, indent=4))

        elif choice == "0":
            print("Sortie...")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
