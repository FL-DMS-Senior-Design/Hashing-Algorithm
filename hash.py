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
    table = c.fetchall()
    for i in range(len(table)):
        pre_image = str(table[i][1]) + str(table[i][2]) + str(table[i][3])
        sha256 = hashlib.sha256()
        sha256.update(pre_image.encode('utf-8'))
        hashie = sha256.hexdigest()
        print(hashie)

        #c.execute("""
        #    UPDATE florida
        #    SET hash = str(hashie)
        #    WHERE rowid = i;
        #          """) # THIS DOESN'T QUITE WORK
        # add this key to the table?
        # can i do this for a million things?
def refresh_hashes(c):
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

def get_column_names(cursor, table_name):
    cursor.execute(f'PRAGMA table_info({table_name})')
    column_info = cursor.fetchall()
    return [column[1] for column in column_info]

## MAIN CODE ##
connection = sqlite3.connect('wyly_db')
# create a cursor 
c = connection.cursor()
        
hash_sql_table(c)
refresh_hashes(c)

# commit changes to db
connection.commit()
connection.close()
