import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('library.db')  # Replace with your database file

# Create a cursor object
cursor = conn.cursor()

# SQL query to delete all rows
query = "DELETE FROM borrowers"  # Replace 'my_table' with your actual table name

# Execute the query
cursor.execute(query)

# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
