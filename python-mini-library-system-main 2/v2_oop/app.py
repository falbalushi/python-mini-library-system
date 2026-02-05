from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional


# ---------- Paths (same data folder at repo root) ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")
LOANS_FILE = os.path.join(DATA_DIR, "loans.json")


# ---------- Models ----------
@dataclass
class Book:
    book_id: int
    title: str
    author: str
    is_available: bool = True


@dataclass
class Member:
    member_id: int
    name: str


@dataclass
class Loan:
    loan_id: int
    member_id: int
    book_id: int
    date: str  # ISO date string


# ---------- App ----------
class LibraryApp:
    def __init__(self) -> None:
        self.books: list[Book] = []
        self.members: list[Member] = []
        self.loans: list[Loan] = []

    # ---- Utilities ----
    def read_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Please enter a number.")

    def show_menu(self) -> None:
        print("\nMini Library System (V2 - OOP):")
        print("1) Add Book")
        print("2) List Books")
        print("3) Register Member")
        print("4) List Members")
        print("5) Borrow Book")
        print("6) Return Book")
        print("7) Search Book")
        print("8) Save & Exit")

    # ---- Find helpers ----
    def find_book(self, book_id: int) -> Optional[Book]:
        for b in self.books:
            if b.book_id == book_id:
                return b
        return None

    def find_member(self, member_id: int) -> Optional[Member]:
        for m in self.members:
            if m.member_id == member_id:
                return m
        return None

    def find_loan_by_book(self, book_id: int) -> Optional[Loan]:
        for l in self.loans:
            if l.book_id == book_id:
                return l
        return None

    # ---- JSON (objects <-> dict) ----
    def _load_list(self, path: str) -> list[dict]:
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print(f"Warning: could not load {path}. Starting empty.")
            return []

    def _save_list(self, path: str, data: list[dict]) -> None:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_data(self) -> None:
        self.books = [Book(**d) for d in self._load_list(BOOKS_FILE)]
        self.members = [Member(**d) for d in self._load_list(MEMBERS_FILE)]
        self.loans = [Loan(**d) for d in self._load_list(LOANS_FILE)]

    def save_data(self) -> None:
        self._save_list(BOOKS_FILE, [asdict(b) for b in self.books])
        self._save_list(MEMBERS_FILE, [asdict(m) for m in self.members])
        self._save_list(LOANS_FILE, [asdict(l) for l in self.loans])

    # ---- Menu actions ----
    def add_book(self) -> None:
        book_id = self.read_int("Enter book id: ")
        title = input("Enter title: ").strip()
        author = input("Enter author: ").strip()

        if title == "" or author == "":
            print("Error: title/author cannot be empty.")
            return

        if self.find_book(book_id) is not None:
            print("Error: Book ID already exists.")
            return

        self.books.append(Book(book_id=book_id, title=title, author=author, is_available=True))
        print("Book added successfully!")

    def list_books(self) -> None:
        if len(self.books) == 0:
            print("No books found.")
            return

        print("\n--- Books List ---")
        for b in self.books:
            status = "Available" if b.is_available else "Borrowed"
            print(f"ID: {b.book_id} | Title: {b.title} | Author: {b.author} | Status: {status}")

    def register_member(self) -> None:
        member_id = self.read_int("Enter member id: ")
        name = input("Enter member name: ").strip()

        if name == "":
            print("Error: name cannot be empty.")
            return

        if self.find_member(member_id) is not None:
            print("Error: Member ID already exists.")
            return

        self.members.append(Member(member_id=member_id, name=name))
        print("Member registered successfully!")

    def list_members(self) -> None:
        if len(self.members) == 0:
            print("No members found.")
            return

        print("\n--- Members List ---")
        for m in self.members:
            print(f"ID: {m.member_id} | Name: {m.name}")

    def borrow_book(self) -> None:
        member_id = self.read_int("Enter member id: ")
        book_id = self.read_int("Enter book id: ")

        member = self.find_member(member_id)
        if member is None:
            print("Error: Member not found.")
            return

        book = self.find_book(book_id)
        if book is None:
            print("Error: Book not found.")
            return

        if not book.is_available:
            print("Error: Book is already borrowed.")
            return

        loan_id = (max([l.loan_id for l in self.loans], default=0) + 1)
        self.loans.append(
            Loan(
                loan_id=loan_id,
                member_id=member_id,
                book_id=book_id,
                date=date.today().isoformat(),
            )
        )
        book.is_available = False
        print("Book borrowed successfully!")

    def return_book(self) -> None:
        book_id = self.read_int("Enter book id to return: ")

        book = self.find_book(book_id)
        if book is None:
            print("Error: Book not found.")
            return

        active_loan = self.find_loan_by_book(book_id)
        if active_loan is None:
            print("Error: This book is not currently borrowed.")
            return

        self.loans.remove(active_loan)
        book.is_available = True
        print("Book returned successfully!")

    def search_book(self) -> None:
        keyword = input("Enter title or author keyword: ").strip().lower()
        if keyword == "":
            print("Keyword cannot be empty.")
            return

        results = []
        for b in self.books:
            if keyword in b.title.lower() or keyword in b.author.lower():
                results.append(b)

        if len(results) == 0:
            print("No matching books found.")
            return

        print("\n--- Search Results ---")
        for b in results:
            status = "Available" if b.is_available else "Borrowed"
            print(f"ID: {b.book_id} | Title: {b.title} | Author: {b.author} | Status: {status}")

    def run(self) -> None:
        self.load_data()
        while True:
            self.show_menu()
            choice = self.read_int("Choose an option (1-8): ")

            if choice == 1:
                self.add_book()
            elif choice == 2:
                self.list_books()
            elif choice == 3:
                self.register_member()
            elif choice == 4:
                self.list_members()
            elif choice == 5:
                self.borrow_book()
            elif choice == 6:
                self.return_book()
            elif choice == 7:
                self.search_book()
            elif choice == 8:
                self.save_data()
                print("Saving... Goodbye")
                break
            else:
                print("Invalid option. Choose 1-8.")


if __name__ == "__main__":
    LibraryApp().run()

