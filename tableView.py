import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('library.db')  # Replace with your database file

# Create a cursor object
cursor = conn.cursor()

# SQL query to select all data from the table
query = "SELECT * FROM borrowers"  # Replace 'my_table' with your actual table name

# Execute the query
cursor.execute(query)

# Fetch all the rows
rows = cursor.fetchall()

# Iterate and print each row
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
