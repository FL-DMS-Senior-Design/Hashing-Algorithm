import sqlite3

conn = sqlite3.connect('people.db')

# Create a cursor
cursor = conn.cursor()

# cretate a table
cursor.execute("""CREATE TABLE people (
               first_name text, 
               last_name text, 
               DOB text,
               SSN text,
            )""")

# Datatypes:
# NULL
# INTEGER
# REAL
# TEXT
# BLOB

# Commit our command
conn.commit()

# Close our connection
conn.close()

#adding comment