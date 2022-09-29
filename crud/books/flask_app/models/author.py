from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    DB = "books"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []
    
    @classmethod
    def add_author(cls, data):
        query = "INSERT INTO authors (name) VALUE (%(name)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL(cls.DB).query_db(query)
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors

    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (author_id,book_id) VALUES (%(author_id)s,%(book_id)s);"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_books_favorited(cls, id):
        data = {'id':id}
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        author = cls(results[0])
        for row in results:
            if row['books.id'] == None:
                print("__break__")
                break
            book_data={
                "id":row["books.id"],
                "title":row["title"],
                "num_of_pages":row["num_of_pages"],
                "created_at":row["books.created_at"],
                "updated_at":row["books.updated_at"]
            }
            author.favorites.append(book.Book(book_data))
        return author

    @classmethod
    def get_authors_not_favorited(cls, id):
        data = {'id':id}
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s)"
        results = connectToMySQL(cls.DB).query_db(query, data)
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors