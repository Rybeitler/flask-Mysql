from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import author, book

@app.route('/books')
def books():
    all_books = book.Book.get_all_books()
    return render_template('book-add.html', books = all_books)

@app.route('/add-book', methods=["POST"])
def add_book():
    book.Book.add_book(request.form)
    return redirect('/books')

@app.route('/books/<int:id>')
def show_book(id):
    data = book.Book.get_fav_books(id)
    print(data)
    not_fav = author.Author.get_authors_not_favorited(id)
    return render_template("book-show.html", data=data, not_fav=not_fav)

@app.route('/books/add-favorite/<id>', methods=["POST"])
def add_fav_author(id):
    book.Book.add_favorite(request.form)
    return redirect(f"/books/{id}")