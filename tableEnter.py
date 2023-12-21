import csv
import sqlite3

# Path to your CSV file
csv_file_path = 'BorrowersTable.csv'  # Replace with your CSV file path

# Connect to the SQLite database
conn = sqlite3.connect('library.db')  # Replace with your database file

# Create a cursor object
cursor = conn.cursor()

# Open the CSV file
with open(csv_file_path, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    # Skip the header row (if your CSV has headers)
    next(reader, None)

    # Iterate over the CSV rows
    for row in reader:
        # SQL query to insert each row
        query = "INSERT INTO borrowers (borrower_id, name, email, phone, book_name) VALUES (?, ?, ?, ?, ?)"  # Modify column names and query as needed
        cursor.execute(query, row)

# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
