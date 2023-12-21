from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.exceptions import BadRequest
import pandas as pd
import random
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')

db = SQLAlchemy(app)

books_table = pd.read_csv('BooksTable.csv')
books = list(books_table['title'])

class Borrower(db.Model):
    __tablename__ = 'borrowers'
    borrower_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)
    __table_args__ = (db.Index('idx_borrower', 'borrower_id', 'name', 'email', 'phone', 'book_name'),)

class Book(db.Model):
    __tablename__ = 'books'
    bid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    __table_args__ = (db.Index('idx_book', 'title', 'status'),)

class Loan(db.Model):
    __tablename__ = 'loans'
    book_id = db.Column(db.Integer, db.ForeignKey('books.bid'), primary_key=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrowers.borrower_id'), primary_key=True)
    checkout_date = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    __table_args__ = (db.Index('idx_loan', 'book_id', 'borrower_id', 'checkout_date', 'due_date'),)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_borrower_form')
def show_add_borrower_form():
    return render_template('add_borrower.html')

@app.route('/borrower/add', methods=['POST'])
def add_borrower():
    try:
        data = request.form
        
        # Check if all required keys are in the submitted form data
        if not all(k in data for k in ['name', 'email', 'phone', 'book_name']):
            raise BadRequest('Missing data for borrower.')

        # Check if the submitted book name is in the list of books loaded from the CSV
        if data['book_name'] not in books:
            return render_template('error.html', error='Book does not exist'), 400
        
        borrowers = Borrower.query.order_by(Borrower.name).all()

        # Query to get all borrower_ids
        rowNew_id = [borrower.borrower_id for borrower in borrowers]

        # Query to get all names
        rowNew_name = [borrower.name for borrower in borrowers]

        # Query to get all emails
        rowNew_email = [borrower.email for borrower in borrowers]

        # Query to get all phone numbers
        rowNew_phone = [borrower.phone for borrower in borrowers]

        # Query to get all book names
        rowNew_book = [borrower.book_name for borrower in borrowers]

        randomID = random.randint(1, 999)

        while randomID in rowNew_id:
            randomID = random.randint(1, 999)

        if data['name'] in rowNew_name or data['email'] in rowNew_email or data['phone'] in rowNew_phone or data['book_name'] in rowNew_book:
            return render_template('error.html', error="Duplicate Entry"), 400

        # Create a new borrower instance
        new_borrower = Borrower(
            borrower_id=randomID,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            book_name=data['book_name']
        )

        # Add the new borrower to the session and commit
        db.session.add(new_borrower)
        db.session.commit()

        # Redirect to the list_borrowers route after successful insertion
        return redirect(url_for('list_borrowers'))
        
    except Exception as e:
        '''
        # Ensure to close the connection even when there's an error
        if conn:
            conn.close()
        '''
        # Render an error template with the exception message
        return render_template('error.html', error=str(e)), 400
    '''
    # Ensure to close the connection after successful operation
    finally:
        if conn:
            conn.close()
    '''


@app.route('/borrowers', methods=['GET'])
def list_borrowers():
    # Fetch borrowers and their borrowed books
    borrowers = Borrower.query.order_by(Borrower.name).all()

    booksUsed = set(borrower.book_name for borrower in borrowers)
    booksNotUsed = set(books).difference(booksUsed)

    # Update status to 'issued' for used books
    if booksUsed:
        Book.query.filter(Book.title.in_(booksUsed)).update({'status': 'issued'}, synchronize_session=False)

    # Update status to 'available' for not used books
    if booksNotUsed:
        Book.query.filter(Book.title.in_(booksNotUsed)).update({'status': 'available'}, synchronize_session=False)

    db.session.commit()

    return render_template('borrowers_list.html', borrowers=borrowers)


@app.route('/books', methods=['GET'])
def view_books():
    # Get search terms from query parameters
    search_title = request.args.get('search_title', '')
    search_author = request.args.get('search_author', '')
    search_category = request.args.get('search_category', '')
    search_status = request.args.get('search_status', '')

    # Build the query using SQLAlchemy
    query = Book.query

    # Apply filters if search criteria are provided
    if search_title:
        query = query.filter(Book.title.like(f'%{search_title}%'))
    if search_author:
        query = query.filter(Book.author.like(f'%{search_author}%'))
    if search_category:
        query = query.filter(Book.category.like(f'%{search_category}%'))
    if search_status:
        query = query.filter(Book.status.like(f'%{search_status}%'))

    # Execute the query and order by title
    books = query.order_by(Book.title).all()

    return render_template('books.html', 
                            books=books, 
                            search_title=search_title,
                            search_author=search_author,
                            search_category=search_category,
                            search_status=search_status)

@app.route('/book/issue', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM borrowers')
        borrowers = cursor.fetchall()
        cursor.execute('SELECT * FROM books WHERE status = "available"')
        books = cursor.fetchall()
        conn.close()
        return render_template('issue_book.html', borrowers=borrowers, books=books)
    else:
        borrower_id = request.form['borrower_id']
        book_id = request.form['book_id']
        due_date = request.form['due_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO loans (book_id, borrower_id, checkout_date, due_date) VALUES (?, ?, CURRENT_DATE, ?)',
                       (book_id, borrower_id, due_date))
        cursor.execute(
            'UPDATE books SET status = "issued" WHERE bid = ?', (book_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('list_loans'))


@app.route('/loans', methods=['GET'])
def list_loans():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT l.*, b.title, br.name
        FROM loans l
        JOIN books b ON l.book_id = b.bid
        JOIN borrowers br ON l.borrower_id = br.borrower_id
    ''')
    loans = cursor.fetchall()
    conn.close()
    return render_template('loans_list.html', loans=loans)


@app.route('/delete_borrower_form')
def show_delete_borrower_form():
    return render_template('delete_borrower.html')


@app.route('/delete_borrower', methods=['POST'])
def delete_borrower():
    data = request.form
    borrower_id = data['borrower_id']

    # Query to find the borrower by ID
    borrower_to_delete = Borrower.query.get(borrower_id)

    if borrower_to_delete:
        # If the borrower exists, delete them from the database
        db.session.delete(borrower_to_delete)
        db.session.commit()
    else:
        # Handle the case where the borrower does not exist
        return render_template('error.html', error="Borrower not found."), 404
    
    return redirect(url_for('list_borrowers'))


@app.route('/update_borrower_form')
def show_update_borrower_form():
    return render_template('update_borrower.html')


@app.route('/update_borrower', methods=['POST'])
def update_borrower():
    data = request.form

    borrower_id = int(data['borrower_id'])
    new_book_name = data['new_book_name']

    borrowers = Borrower.query.order_by(Borrower.name).all()
    rowNew_id = [borrower.borrower_id for borrower in borrowers]
    rowNew_book = [borrower.book_name for borrower in borrowers]
    
    if borrower_id not in rowNew_id or new_book_name not in books or new_book_name in rowNew_book:
       return render_template('error.html', error="Invalid Entry"), 400

    borrower = Borrower.query.get(borrower_id)
    borrower.book_name = new_book_name
    db.session.commit()
    
    return redirect(url_for('list_borrowers'))

@app.route('/about')
def about():
    return render_template('aboutus.html')



if __name__ == '__main__':
    app.run(debug=True)