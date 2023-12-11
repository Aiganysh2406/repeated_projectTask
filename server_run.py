from flask import Flask, jsonify, request
from main import db, Book, BookPydantic

app = Flask(__name__)


@app.route("/get_books/", methods=['GET'])
def get_books():
    books = get_book()
    return jsonify({'data': books})

@app.route("/create_book/", methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        book = BookPydantic(
            title=data.get('title'),
            author=data.get('author'),
            genre=data.get('genre'),
            created_at=data.get('created_at')
        )
        
        db.session.add(book)
        db.session.commit()
        return jsonify({'message': "created successfully"})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/retrieve_book/<int:book_id>/", methods=['GET'])
def get_one_book(book_id):
    item = retrieve(book_id)
    if not item:
        return jsonify({'message': 'not found'})
    return jsonify({'data': item})

@app.route("/update_book/<int:book_id>/", methods=['PUT'])
def update_book_rq(book_id):
    try:
        data = request.get_json()
        update_book_data = BookPydantic(
            title=data.get('title'),
            author=data.get('author'),
            genre=data.get('genre'),
            created_at=data.get('created_at')
        )
        db_book = Book.query.get(book_id)
        if not db_book:
            return jsonify({'error': 'book not found'})
        
        db_book.title = update_book_data.title
        db_book.author = update_book_data.author
        db_book.genre = update_book_data.genre
        db_book.created_at = update_book_data.created_at

        db.session.commit()

        return jsonify({'message': 'updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/delete_book/<int:book_id>/", methods=['DELETE'])
def delete_book(book_id):
    try:
        deleted_book = delete_book(book_id)  
        if deleted_book:
            return jsonify({'message': "deleted successfully"})
        else:
            return jsonify({'error': 'book not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    db.create_all()
    app.run(host='localhost', port=1234)