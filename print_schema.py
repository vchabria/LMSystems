import sqlite3

def print_schema(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Retrieve a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Iterate over the list of tables
    for table in tables:
        print(f"Schema for {table[0]}:")
        # Retrieve the schema for each table
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        for col in columns:
            print(col)
        print("\n")  # Print a newline for better readability

    # Close the connection to the database
    conn.close()

# Replace 'library.db' with the path to your database file
print_schema('library.db')
