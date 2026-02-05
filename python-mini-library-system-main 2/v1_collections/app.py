books = []  # list of dicts (each dict represents one book)
members = []  # list of dicts (each dict represents one member)
loans = []

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")
LOANS_FILE = os.path.join(DATA_DIR, "loans.json")


def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(" Please enter a number: ")


def show_menu():
    print("\n Mini Library System (V1 - Collections) : ")
    print("1) Add Book")
    print("2) List Books")
    print("3) Register Member")
    print("4) List Members")
    print("5) Borrow Book")
    print("6) Return Book")
    print("7) Search Book")
    print("8) Save & Exit")


#_______________________________________
def add_book():
    book_id = read_int("Enter book id: ")
    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()

    book = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "is_available": True
    }

    books.append(book)
    print("Book added successfully!")

    
def list_books():
    if len(books) == 0:
        print("No books found.")
        return

    print("\n--- Books List ---")
    for b in books:
        status = "Available" if b["is_available"] else "Borrowed"
        print(f'ID: {b["book_id"]} | Title: {b["title"]} | Author: {b["author"]} | Status: {status}')


#_______________________________________
def register_member():
    member_id = read_int("Enter member id: ")
    name = input("Enter member name: ").strip()

    member = {
        "member_id": member_id,
        "name": name
    }

    members.append(member)
    print("Member registered successfully!")

def list_members():
    if len(members) == 0:
        print("No members found.")
        return

    print("\n--- Members List ---")
    for m in members:
        print(f'ID: {m["member_id"]} | Name: {m["name"]}')


#_______________________________________
def find_book_by_id(book_id: int):
    for b in books:
        if b["book_id"] == book_id:
            return b
    return None

def find_member_by_id(member_id: int):
    for m in members:
        if m["member_id"] == member_id:
            return m
    return None

def find_active_loan_by_book_id(book_id: int):
    # active loan = book is currently borrowed
    for loan in loans:
        if loan["book_id"] == book_id:
            return loan
    return None


from datetime import date  
def borrow_book():
    member_id = read_int("Enter member id: ")
    book_id = read_int("Enter book id: ")

    member = find_member_by_id(member_id)
    if member is None:
        print("Error: Member not found.")
        return

    book = find_book_by_id(book_id)
    if book is None:
        print("Error: Book not found.")
        return

    if book["is_available"] is False:
        print("Error: Book is already borrowed.")
        return

    # create new loan
    loan_id = len(loans) + 1
    loan = {
        "loan_id": loan_id,
        "member_id": member_id,
        "book_id": book_id,
        "date": date.today().isoformat()
    }

    loans.append(loan)
    book["is_available"] = False
    print("Book borrowed successfully!")


def return_book():
    book_id = read_int("Enter book id to return: ")

    book = find_book_by_id(book_id)
    if book is None:
        print("Error: Book not found.")
        return

    active_loan = find_active_loan_by_book_id(book_id)
    if active_loan is None:
        print("Error: This book is not currently borrowed.")
        return

    # remove loan record
    loans.remove(active_loan)
    book["is_available"] = True
    print("Book returned successfully!")


#_______________________________________
def search_book():
    keyword = input("Enter title or author keyword: ").strip().lower()

    if keyword == "":
        print("Keyword cannot be empty.")
        return

    results = []
    for b in books:
        title = b["title"].lower()
        author = b["author"].lower()
        if keyword in title or keyword in author:
            results.append(b)

    if len(results) == 0:
        print("No matching books found.")
        return

    print("\n--- Search Results ---")
    for b in results:
        status = "Available" if b["is_available"] else "Borrowed"
        print(f'ID: {b["book_id"]} | Title: {b["title"]} | Author: {b["author"]} | Status: {status}')


#_______________________________________
def load_list(path: str):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"Warning: could not load {path}. Starting empty.")
        return []


def save_list(path: str, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_data():
    global books, members, loans
    books = load_list(BOOKS_FILE)
    members = load_list(MEMBERS_FILE)
    loans = load_list(LOANS_FILE)


def save_data():
    save_list(BOOKS_FILE, books)
    save_list(MEMBERS_FILE, members)
    save_list(LOANS_FILE, loans)

#_______________________________________
def main():
    load_data()
    while True:
        show_menu()
        choice = read_int("Choose an option (1-8): ")

        if choice == 1:
            add_book()
        elif choice == 2:
            list_books()
        elif choice == 3:
         register_member()
        elif choice == 4:
            list_members()
        elif choice == 5:
            borrow_book()
        elif choice == 6:
            return_book()
        elif choice == 7:
            search_book()
        elif choice == 8:
            save_data()
            print("Saving... Goodbye")
            break
        else:
            print("Invalid option. Choose 1-8.")


if __name__ == "__main__":
    main()

