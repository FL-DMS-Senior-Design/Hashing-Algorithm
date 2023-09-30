import sqlite3
import random
import string

# Function to generate random data
def generate_random_data():
    first_name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    last_name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    dob = f"{random.randint(1950, 2000)}-{random.randint(1, 12)}-{random.randint(1, 28)}"
    ssn = ''.join(random.choice(string.digits) for _ in range(9))
    return first_name, last_name, dob, ssn

# Create a database (or connect to an existing one)
conn = sqlite3.connect("sample.db")

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        first_name TEXT,
        last_name TEXT,
        DOB TEXT,
        SSN TEXT
    )
''')

# Insert random data into the table
for _ in range(10):  # You can change the number of rows as needed
    data = generate_random_data()
    cursor.execute('INSERT INTO people (first_name, last_name, DOB, SSN) VALUES (?, ?, ?, ?)', data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created and populated with random data.")




# Connect to the database
conn = sqlite3.connect("sample.db")

# Create a cursor object
cursor = conn.cursor()

# Execute a query to retrieve data
cursor.execute("SELECT * FROM people")

# Fetch and print the results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()

#holaaa