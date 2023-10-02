import sqlite3
import pandas as pd
import hashlib


def read_excel_to_sql(connection):
    # note that you need to 'pip install openpyxl' to continue
    df = pd.read_excel('Example Databases.xlsx', sheet_name='Format 1')
    print(df)
    df.to_sql('florida', connection, if_exists="replace")

def add_hash_key(c):
    # Now... can i clean, hash, and test this for collisions?
    c.execute("""
            ALTER TABLE florida
            ADD COLUMN hash text
        """)
    
# hashy hashy time
def hash_sql_table(c):
    c.execute('SELECT * FROM florida')
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
        c.execute('UPDATE florida SET hash = ? WHERE rowid = ?', (hash_value, i+1))
    print("Successfully hashed SQL table.")


def get_column_names(cursor, table_name):
    cursor.execute(f'PRAGMA table_info({table_name})')
    column_info = cursor.fetchall()
    return [column[1] for column in column_info]

## MAIN CODE ##
connection = sqlite3.connect('wyly_db')
# create a cursor 
c = connection.cursor()
        
hash_sql_table(c)

# commit changes to db
connection.commit()
connection.close()
