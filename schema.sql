-- schema.sql
-- SQL script to create the database schema for a library management system

-- Create the 'borrowers' table
CREATE TABLE IF NOT EXISTS borrowers (
    borrower_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    book_name TEXT NOT NULL,
);


-- Create the 'books' table
CREATE TABLE IF NOT EXISTS books (
    bid INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    status TEXT CHECK(status IN ('available', 'issued')) NOT NULL DEFAULT 'available'
);

-- Create the 'loans' table
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    borrower_id INTEGER NOT NULL,
    checkout_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(bid),
    FOREIGN KEY (borrower_id) REFERENCES borrowers(borrower_id)
);

DELETE FROM borrowers
WHERE borrower_id NOT IN (
    SELECT MIN(borrower_id)
    FROM borrowers
    GROUP BY email
)

