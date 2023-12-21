import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Open and read the schema script
with open('schema.sql', 'r') as schema_file:
    schema_script = schema_file.read()

# Execute the schema script
cursor.executescript(schema_script)

# Commit changes and close the connection
conn.commit()
conn.close()
