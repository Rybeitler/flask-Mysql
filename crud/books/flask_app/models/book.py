from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    DB = "books"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []
    
    @classmethod
    def add_book(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUE (%(title)s, %(num_of_pages)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books"
        results = connectToMySQL(cls.DB).query_db(query)
        books = []
        for row in results:
            books.append(cls(row))
        return books

    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (author_id,book_id) VALUES (%(author_id)s,%(book_id)s);"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_fav_books(cls, id):
        data = {'id':id}
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        book = cls(results[0])
        for row in results:
            if row["authors.id"] == None:
                break
            author_data={
                "id":row["authors.id"],
                "name":row["name"],
                "created_at":row["authors.created_at"],
                "updated_at":row["authors.updated_at"]
            }
            book.favorites.append(author.Author(author_data))
        return book

    @classmethod
    def get_books_not_favorited(cls, id):
        data = {'id':id}
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s)"
        results = connectToMySQL(cls.DB).query_db(query, data)
        books = []
        for row in results:
            books.append(cls(row))
        return books