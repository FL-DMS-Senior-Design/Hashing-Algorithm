import sqlite3
from faker import Faker
import random
import datetime

# Function to generate a random date of birth between two given dates
def generate_birthdate(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    birth_date = start_date + datetime.timedelta(days=random_number_of_days)
    return birth_date.strftime('%Y-%m-%d')

# Function to generate a random Social Security Number (SSN)
def generate_ssn():
    ssn = f'{random.randint(100, 999):03}-{random.randint(10, 99):02}-{random.randint(1000, 9999):04}'
    return ssn

# Initialize the Faker instance
fake = Faker()

# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect("names.db")
cursor = conn.cursor()

# Create a table for the full names, SSNs, and birthdates
cursor.execute('''CREATE TABLE IF NOT EXISTS full_names (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    ssn TEXT,
                    birthdate DATE
                )''')

# Set the range for birthdate generation (e.g., between 1950-01-01 and 2005-12-31)
start_date = datetime.date(1950, 1, 1)
end_date = datetime.date(2005, 12, 31)

# Generate and insert 20 million full names, SSNs, and birthdates into the table
for _ in range(5000000):
    first_name = fake.first_name()
    last_name = fake.last_name()
    ssn = generate_ssn()
    birthdate = generate_birthdate(start_date, end_date)
    cursor.execute("INSERT INTO full_names (first_name, last_name, ssn, birthdate) VALUES (?, ?, ?, ?)", (first_name, last_name, ssn, birthdate))

# Commit the changes and close the connection
conn.commit()
conn.close()

# Connect to the SQLite database
conn = sqlite3.connect("names.db")  # Replace "names.db" with the actual name of your database file
cursor = conn.cursor()

# Query the first 500 rows of the "full_names" table
cursor.execute("SELECT * FROM full_names LIMIT 500")

# Fetch and print the results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the database connection
conn.close()
