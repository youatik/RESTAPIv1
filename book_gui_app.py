from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from book_service import (
    get_all_books, get_book_by_isbn, add_book, search_books, get_random_book
)
import json


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)
        layout.add_widget(Button(text="Get all books", on_press=self.go_to_all_books, size_hint_y=None, height=44))
        layout.add_widget(Button(text="Get a book by ISBN", on_press=self.go_to_get_book, size_hint_y=None, height=44))
        layout.add_widget(Button(text="Add a book", on_press=self.go_to_add_book, size_hint_y=None, height=44))
        layout.add_widget(Button(text="Search for books", on_press=self.go_to_search_books, size_hint_y=None, height=44))
        layout.add_widget(Button(text="Get a random book", on_press=self.go_to_random_book, size_hint_y=None, height=44))
        layout.add_widget(Button(text="Exit", on_press=App.get_running_app().stop, size_hint_y=None, height=44))
        self.add_widget(layout)

    def go_to_all_books(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'all_books_screen'

    def go_to_get_book(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'get_book_screen'

    def go_to_add_book(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'add_book_screen'

    def go_to_search_books(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'search_books_screen'

    def go_to_random_book(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'random_book_screen'


class AllBooksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)

        self.results_box = TextInput(background_color='white', readonly=True, size_hint=(1, 0.7))
        layout.add_widget(self.results_box)

        layout.add_widget(Button(text="Back", on_press=self.go_back, size_hint_y=None, height=44))
        self.add_widget(layout)
        self.fetch_all_books()

    def fetch_all_books(self):
        try:
            books = get_all_books()
            self.results_box.text = json.dumps(books, indent=4)
        except Exception as e:
            self.results_box.text = f"Error: {str(e)}"

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu_screen'


class GetBookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)
        layout.add_widget(Label(text="Enter ISBN"))
        self.isbn_input = TextInput(hint_text="Enter ISBN", multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.isbn_input)
        layout.add_widget(Button(text="Submit", on_press=self.get_book, size_hint_y=None, height=44))

        self.results_box = TextInput(background_color='white', readonly=True, size_hint=(1, 0.7))
        layout.add_widget(self.results_box)

        layout.add_widget(Button(text="Back", on_press=self.go_back, size_hint_y=None, height=44))
        self.add_widget(layout)

    def get_book(self, instance):
        isbn = self.isbn_input.text
        try:
            book = get_book_by_isbn(int(isbn))
            if book:
                self.results_box.text = json.dumps(book, indent=4)
            else:
                self.results_box.text = f"No book found with ISBN {isbn}."
        except Exception as e:
            self.results_box.text = f"Error: {str(e)}"

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu_screen'


class AddBookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)
        layout.add_widget(Label(text="Enter book data in JSON format:"))
        self.book_data_input = TextInput(hint_text='{"title": "...", "author": "..."}', multiline=True)
        layout.add_widget(self.book_data_input)
        layout.add_widget(Button(text="Add Book", on_press=self.add_book, size_hint_y=None, height=44))

        self.results_box = TextInput(background_color='white', readonly=True, size_hint=(1, 0.7))
        layout.add_widget(self.results_box)

        layout.add_widget(Button(text="Back", on_press=self.go_back, size_hint_y=None, height=44))
        self.add_widget(layout)

    def add_book(self, instance):
        book_data_str = self.book_data_input.text
        try:
            book_data = json.loads(book_data_str)
            book_id = add_book(book_data)
            self.results_box.text = f"Added book with ID: {book_id}"
        except Exception as e:
            self.results_box.text = f"Error: {str(e)}"

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu_screen'


class SearchBooksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)
        layout.add_widget(Label(text="Enter your search query:"))
        self.search_input = TextInput(hint_text="Search...", multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.search_input)
        layout.add_widget(Button(text="Search", on_press=self.search_books, size_hint_y=None, height=44))

        self.results_box = TextInput(background_color='white', readonly=True, size_hint=(1, 0.7))
        layout.add_widget(self.results_box)

        layout.add_widget(Button(text="Back", on_press=self.go_back, size_hint_y=None, height=44))
        self.add_widget(layout)

    def search_books(self, instance):
        query = self.search_input.text
        try:
            books = search_books(query)
            self.results_box.text = json.dumps(books, indent=4)
        except Exception as e:
            self.results_box.text = f"Error: {str(e)}"

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu_screen'


class RandomBookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10), spacing=10)

        self.results_box = TextInput(background_color='white', readonly=True, size_hint=(1, 0.7))
        layout.add_widget(self.results_box)

        layout.add_widget(Button(text="Get another random book", on_press=self.get_random_book, size_hint_y=None, height=44))
        layout.add_widget(Button(text="Back", on_press=self.go_back, size_hint_y=None, height=44))
        self.add_widget(layout)
        self.get_random_book(None)

    def get_random_book(self, instance):
        try:
            book = get_random_book()
            self.results_box.text = json.dumps(book, indent=4)
        except Exception as e:
            self.results_box.text = f"Error: {str(e)}"

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu_screen'


class BookApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu_screen'))
        sm.add_widget(AllBooksScreen(name='all_books_screen'))
        sm.add_widget(GetBookScreen(name='get_book_screen'))
        sm.add_widget(AddBookScreen(name='add_book_screen'))
        sm.add_widget(SearchBooksScreen(name='search_books_screen'))
        sm.add_widget(RandomBookScreen(name='random_book_screen'))
        return sm

if __name__ == '__main__':
    BookApp().run()
