from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import author, book

@app.route('/')
@app.route('/authors')
def authors():
    all_authors = author.Author.get_all_authors()
    return render_template('author-add.html', authors = all_authors)

@app.route('/add-author', methods=["POST"])
def add_author():
    author.Author.add_author(request.form)
    return redirect('/')

@app.route('/authors/<int:id>')
def show_author(id):
    data = author.Author.get_books_favorited(id)
    print(data.favorites)
    not_fav = book.Book.get_books_not_favorited(id)
    return render_template("author-show.html", data=data, not_fav=not_fav)

@app.route('/add-favorite/<id>', methods=["POST"])
def add_fav(id):
    author.Author.add_favorite(request.form)
    return redirect(f"/authors/{id}")