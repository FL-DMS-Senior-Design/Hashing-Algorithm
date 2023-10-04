import sqlite3
import pandas as pd
import hashlib
import numpy as np


def read_excel_to_sql(connection, table_name):
    # note that you need to 'pip install openpyxl' to continue
    df = pd.read_excel('Example Databases.xlsx', sheet_name='Format 1') # this may need to change
    print(df)
    df.to_sql(table_name, connection, if_exists="replace")

def add_hash_key(c, table_name):
    # Now... can i clean, hash, and test this for collisions?
    c.execute(f"""
            ALTER TABLE {table_name}
            ADD COLUMN hash text
        """)
    
# hashy hashy time
def hash_sql_table(c, table_name):
    c.execute(f'SELECT * FROM {table_name}')
    rows = c.fetchall()
    hash_list = []
    for row in rows:
        pre_image = str(row[1]) + str(row[2]) + str(row[3])
        sha256 = hashlib.sha256()
        sha256.update(pre_image.encode('utf-8'))
        hashie = sha256.hexdigest()
        hash_list.append(hashie)

    # Update the "hash" column with values from hash_list
    for i, hash_value in enumerate(hash_list):
        c.execute(f'UPDATE {table_name} SET hash = ? WHERE rowid = ?', (hash_value, i+1))
    print("Successfully hashed SQL table.")


def get_column_names(cursor, table_name):
    cursor.execute(f'PRAGMA table_info({table_name})')
    column_info = cursor.fetchall()
    return [column[1] for column in column_info]

def num_collisions(list_l): # i want to change this to take a connection and a table name
    length = len(list_l[4])
    num_unique = len(np.unique(list_l[4]))
    return (length - num_unique)
    

## MAIN CODE ##
connection = sqlite3.connect('wyly_db')
# create a cursor 
c = connection.cursor()
hash_sql_table(c, 'florida')

# Print the number of collisions (LENGTH OF HASH COL of TABLE - LENGTH OF UNIQUE VALUES OF HASH COL)
c.execute("SELECT * FROM florida")
print("Collision Count: " + str(num_collisions(c.fetchall())))
# commit changes to db
connection.commit()
connection.close()
