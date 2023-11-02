import sqlite3
import pandas as pd
import hashlib
import numpy as np
import csv
import random
from datetime import datetime, timedelta
from names_dataset import NameDataset
import string
import time

def read_excel_to_sql(connection, table_name, excel_file_path):
    # note that you need to 'pip install openpyxl' to continue
    df = pd.read_excel(excel_file_path, sheet_name='Format 1') # this may need to change
    df.to_sql(table_name, connection, if_exists="replace")
    print("Successfully created the " + table_name + " table in SQL")

def read_csv_to_sql(connection, table_name, csv_file_path):
    df = pd.read_csv(csv_file_path)
    df.to_sql(table_name, connection, if_exists="replace")
    print("Successfully created the " + table_name + " table in SQL")

def add_hash_key(cursor, table_name):
    cursor.execute(f"""
            ALTER TABLE {table_name}
            ADD COLUMN hash text
        """)

def add_4096_key(cursor, table_name):
    cursor.execute(f"""
            ALTER TABLE {table_name}
            ADD COLUMN key_4096 text
        """)

def hash_sql_table(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    hash_list = []
    for row in rows:
        pre_image = str(row[1]) + str(row[2]) + str(row[3])
        sha256 = hashlib.sha256()
        sha256.update(pre_image.encode('utf-8'))
        hashie = sha256.hexdigest()
        hash_list.append(hashie)

    # Update the "hash" column with values from hash_list
    for i, hash_value in enumerate(hash_list):
        cursor.execute(f'UPDATE {table_name} SET hash = ? WHERE rowid = ?', (hash_value, i+1))
    print("Successfully hashed SQL table.")

def generate_4096_keys(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = c.fetchall()
    key_list = []
    print(rows[0][2])
    print(rows[0][3])
    for row in rows:
            # hash 1st name
            sha256 = hashlib.sha256()
            pre_image = str(row[2].split()[0])
            sha256.update(pre_image.encode('utf-8'))
            hashie = sha256.hexdigest()
            print("First Name? " + str(row[2].split()[0]))

            # hash last name
            pre_image = str(row[2].split()[-1])
            sha256.update(pre_image.encode('utf-8'))
            hashie += sha256.hexdigest()
            print("Last Name? " + str(row[2].split()[-1]))
            
            # hash birth year
            pre_image = str(row[3].split('-')[0])
            sha256.update(pre_image.encode('utf-8'))
            hashie += sha256.hexdigest()
            print("Br=irth year? " + str(row[3].split('-')[0]))

            # hash birth month
            pre_image = str(row[3].split('-')[1])
            sha256.update(pre_image.encode('utf-8'))
            hashie += sha256.hexdigest()

            # hash birth year
            pre_image = str(row[3].split('-')[-1])
            sha256.update(pre_image.encode('utf-8'))
            hashie += sha256.hexdigest()

            # hash last 4 SSN
            pre_image = str(row[4])
            sha256.update(pre_image.encode('utf-8'))
            hashie += sha256.hexdigest()

             # hash Driver's License
            pre_image = str(row[5])
            sha256.update(pre_image.encode('utf-8'))
            hashie += sha256.hexdigest()

             # hash Gender
            pre_image = str(row[6])
            sha256.update(pre_image.encode('utf-8'))
            hashie += sha256.hexdigest()

            key_list.append(hashie)

            # Update the "hash" column with values from hash_list
    for i, key_value in enumerate(key_list):
        cursor.execute(f'UPDATE {table_name} SET key_4096 = ? WHERE rowid = ?', (key_value, i+1))
    print("Successfully generated 4096 keys in SQL table.")

def get_column_names(cursor, table_name):
    cursor.execute(f'PRAGMA table_info({table_name})')
    column_info = cursor.fetchall()
    return [column[1] for column in column_info]

def num_collisions(cursor, table_name): # i want to change this to take a connection and a table name
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    length = len(data[4])
    num_unique = len(np.unique(data[4]))
    return (length - num_unique)

# TO DO TEST ALGORITHM ON 1 MILLION DATASET
# Function to generate a random date within a given date range
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def create_million_name_csv():
    nd = NameDataset()

    first_names_uncleaned = nd.get_top_names(n=1000,country_alpha2='US')
    last_names_uncleaned = nd.get_top_names(n=1000,country_alpha2='US', use_first_names=False)

    first_names = first_names_uncleaned['US']['M'] + first_names_uncleaned['US']['F']
    last_names = last_names_uncleaned['US']
    
    num_entries = 20000000  # 1 million entries
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2000, 12, 31)

    with open('name_locked_twenty_db.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Birthday', 'Last 4 SSN', 'Drivers License Num', 'Gender']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for _ in range(num_entries):
            if _ % 10 != 3: # force one in every 10 names to be exact matches 
                name = str(random.choice(first_names)) + " " + str(random.choice(last_names))
            birthday_ = random_date(start_date, end_date)
            birthday_string = birthday_.strftime('%Y-%m-%d')
            last_4_ssn = ''.join(random.choices('0123456789', k=4))

            # simulate the lack of presence of a drivers license
            # 10% of people plus those under 16 have no number
            if random.random() < 0.10 or ((datetime.now() - birthday_).days) // 365 < 16:
                d_num = str(0)
            else:
                d_num =  str(random.choice(string.ascii_letters).upper()) + ''.join([str(random.randint(0, 9)) for _ in range(12)])
            
            # simulate other as an option for gender
            if random.random() < .02:
                gender_ = 'other'
            elif random.random() < 0.5:
                gender_ = 'M'
            else:
                gender_ = 'F'

            
            writer.writerow({'Name': name, 'Birthday': birthday_string, 'Last 4 SSN': last_4_ssn, 'Drivers License Num': d_num, 'Gender':gender_})

    print("CSV file generated successfully.")

    ##establishing penalties
def define_penalties(FIRST, LAST, MM, DD, YYYY, SSN, DL, GEND):
    print("Defining chunk penalties.")
    return [FIRST, LAST, MM, DD, YYYY, SSN, DL, GEND]

##Confidence Calculation
def confidence_interval_for_key_comparison(key1, key2, chunk_penalty):
    chunk_size = 64 # this should be 64 character chunks
    key1 = str(key1)
    key2 = str(key2)
    num_chunks = len(key1) // chunk_size

    # Initialize lists to store results for each chunk
    chunk_similarity = []

    for i in range(num_chunks):
        # Extract chunks from both keys
        chunk1 = key1[i * chunk_size:(i + 1) * chunk_size]
        chunk2 = key2[i * chunk_size:(i + 1) * chunk_size]

        # Calculate similarity score for the chunk (e.g., 1 if different, 0 if identical)
        similarity = int(chunk1 != chunk2)
    
        # Append to the list
        chunk_similarity.append(similarity)
        
    #sumproduct to get confidence
    percentConfidence= 100 - 100 * np.dot(chunk_similarity, chunk_penalty)
    percentConfidence = max(0, percentConfidence)

    return percentConfidence

def compare_keys(key1, key2, chunk_penalty, matchdict):
    percentConfidence = confidence_interval_for_key_comparison(key1, key2, chunk_penalty)
    
    if percentConfidence > 0.0:
        matchdict[str(key2)]= str(percentConfidence) # this will overwrite if there are multiple of the same keys.
                                                     # which should be overwritten with the same percentConfidence

def key_selection(key1, key_list, chunk_penalty):
    matchdict = dict()
    for i in key_list:
        key2= i
        compare_keys(key1,key2, chunk_penalty, matchdict)
    return matchdict

def database_modifier(db1_data, db2_table_name, db2_connection):
    # create pool for new names
    nd = NameDataset()

    first_names_uncleaned = nd.get_top_names(n=1000,country_alpha2='US')
    last_names_uncleaned = nd.get_top_names(n=1000,country_alpha2='US', use_first_names=False)

    first_names = first_names_uncleaned['US']['M'] + first_names_uncleaned['US']['F']
    last_names = last_names_uncleaned['US']
    
    for index, row in db1_data.iterrows():
        if index % 5 == 0: # 20% chance a new first name is given
            new_name = str(random.choice(first_names)) + " " + str(row['Name']).split()[-1] 
            db1_data.at[index,'Name']  = new_name
        elif index % 5 == 1: # 20% chance a new last name is given
            new_name = str(row['Name']).split()[0] + " " + str(random.choice(last_names))
            db1_data.at[index,'Name'] = new_name

    db1_data.to_sql(db2_table_name, db2_connection, if_exists="replace")

def expectedConfidence(inputs1, inputs2, chunk_penalty):
    #compares inputs
    same_elements = [x != y for x, y in zip(inputs1, inputs2)]
    #calculates confidence
    confidenceInputs= 100 - 100 * np.dot(chunk_penalty, same_elements)
    print("EXPECTING: " + str(confidenceInputs))
    return confidenceInputs

def confidenceKeys(key1,key2, chunk_penalty):
    substring_length = len(key1) // 8
    # Use list comprehension to divide the string into 8 equal-length strings
    chunks1 = [key1[i:i+substring_length] for i in range(0, len(key1), 64)]
    chunks2 = [key2[i:i+substring_length] for i in range(0, len(key2), 64)]
    #perform comparison
    for x, y in zip(chunks1, chunks2):
        print(x + "   " + y)
    same_elements = [x != y for x, y in zip(chunks1, chunks2)]
    #calculate confidence
    percentConfidenceKeys= 100 - 100 * np.dot(same_elements, chunk_penalty)
    
    print(np.dot(same_elements, chunk_penalty))
    print(same_elements)
    print(chunk_penalty)
    print("GETTING: " + str(percentConfidenceKeys))
    return percentConfidenceKeys

## MAIN CODE ##
connection = sqlite3.connect('million_db')
# create a cursor 
c = connection.cursor()

count=0
totalComparisons=0
c.execute("SELECT * from fixed_name LIMIT 1000")
fixed_name_list = c.fetchall()
c.execute("SELECT * from fixed_name_mod1 LIMIT 1000")
fixed_name_mod1 = c.fetchall()
chunk_penalties = define_penalties(0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.05, 0.05)

for i in range(len(fixed_name_list)):
    if i == 0:
        continue
    temp1 = fixed_name_list[i][1:6]
    temp2 = fixed_name_mod1[i][2:7]
    key1 = fixed_name_list[i][6]
    key2 = fixed_name_mod1[i][7]
    # clean the lists
    inputs1 = list()
    inputs2 = list()
    
    inputs1.append(temp1[0].split()[0]) # separate first 
    inputs1.append(temp1[0].split()[-1]) # and last name
    inputs1.append(temp1[1].split('-')[0])
    inputs1.append(temp1[1].split('-')[1])
    inputs1.append(temp1[1].split('-')[2])
    inputs1.append(temp1[2])
    inputs1.append(temp1[3])
    inputs1.append(temp1[4])
    
    inputs2.append(temp2[0].split()[0]) # separate first 
    inputs2.append(temp2[0].split()[-1]) # and last name
    inputs2.append(temp2[1].split('-')[0])
    inputs2.append(temp2[1].split('-')[1])
    inputs2.append(temp2[1].split('-')[2])
    inputs2.append(temp2[2])
    inputs2.append(temp2[3])
    inputs2.append(temp2[4])
    if expectedConfidence(inputs1, inputs2, chunk_penalties) == confidenceKeys(key1, key2, chunk_penalties):
        count+=1 #keeps track of the total number of times our key correctly calculated confidence
    totalComparisons+=1
    
    if expectedConfidence(inputs1, inputs2, chunk_penalties) == 90.0:
        print("EXPECTED CONFIDENCE OF 90")
        substr = len(key1) // 8
        for i in range(8):
            print(str(inputs1[i]) + "   " + str(inputs2[i]))
            print(key1[i * substr:(i+1) * substr])
            print(key2[i * substr:(i+1) * substr])

print("Our confidence interval is correct ", (count/totalComparisons)*100, "% of the time")
# df = pd.read_sql_query("SELECT * FROM fixed_name", connection)
# database_modifier(df, 'fixed_name_mod1', connection)

# connection.commit()

# do the matching algorithm

# c.execute("SELECT key_4096 FROM twenty_4096 LIMIT 5000000")
# keys_4096 = c.fetchall()
# print("Length of keys is " + str(len(keys_4096)) + " | num unique is " + str(len(np.unique(keys_4096))))

# c.execute("SELECT Name FROM twenty_4096 LIMIT 5000000")
# names = c.fetchall()
# print("Length of names is " + str(len(names)) + " | num unique is " + str(len(np.unique(names))))

# c.execute("SELECT Birthday FROM twenty_4096 LIMIT 5000000")
# birthdays = c.fetchall()
# print("Length of birthdays is " + str(len(birthdays)) + " | num unique is " + str(len(np.unique(birthdays))))

# c.execute("SELECT Last 4 SSN FROM twenty_4096 LIMIT 500000")
# ssn = c.fetchall()
# print("Length of ssn is " + str(len(ssn)) + " | num unique is " + str(len(np.unique(ssn))))

# c.execute("SELECT Drivers License Num FROM twenty_4096 LIMIT 5000000")
# idnum = c.fetchall()
# print("Length of id is " + str(len(idnum)) + " | num unique is " + str(len(np.unique(idnum))))

# c.execute("SELECT Gender FROM twenty_4096 LIMIT 5000000")
# gender = c.fetchall()
# print("Length of gender is " + str(len(gender)) + " | num unique is " + str(len(np.unique(gender))))

# c.execute("SELECT key_4096 FROM fixed_name LIMIT 5000000")
# rows = c.fetchall()
# for i in range(1000):
#     key1 = rows[i]
#     matchdict = key_selection(key1, rows[i+1:], chunk_penalties) # Cool stuff, matchdict is passed by ref

#     #check if there is only one 100% match: 
#     if len(matchdict) == 1 and float(list(matchdict.values())[0]) == 1.0:
#         print("\nPrimary key ", key1, " in database is an exact match")
#     elif len(matchdict) == 0:
#         print("\nPrimary key ", key1, " has no match")
#     else:
#         for key, value in matchdict.items():
#             print("\nPrimary key " + str(key1) + " is " + str(value * 100) + "% likely a unique match with key " + str(key))


# # Write the data to the CSV file
# with open(csv_file_path, 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
    
#     # Write the header row with column names (optional)
#     column_names = [description[0] for description in c.description]
#     csv_writer.writerow(column_names)
    
#     # Write the data rows
#     csv_writer.writerows(rows)

# print(f'Data has been exported to {csv_file_path}')


# commit changes to db
connection.commit()
connection.close()

#end = time.time()

#print("Solution 2 finishes its search of 5 million in " + str(end - begin))