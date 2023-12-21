from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')

db = SQLAlchemy(app)

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

with app.app_context():
    borrowers = Borrower.query.order_by(Borrower.name).all()
    print(borrowers)
