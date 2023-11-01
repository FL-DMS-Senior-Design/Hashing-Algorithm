
import numpy as np
import sqlite3

chunk_penalty= [0.1,0.1,0.2,0.2,0.2, 0.1, 0.05, 0.05]

def expectedConfidence(inputs1, inputs2):
    #compares inputs
    same_elements = [x != y for x, y in zip(inputs1, inputs2)]
    #calculates confidence
    confidenceInputs= 100-100*chunk_penalty.dot(same_elements)

    return confidenceInputs

def confidenceKeys(key1,key2):
    substring_length = len(key1) // 8
    # Use list comprehension to divide the string into 8 equal-length strings
    chunks1 = [key1[i:i+substring_length] for i in range(0, len(key1), substring_length)]
    chunks2 = [key2[i:i+substring_length] for i in range(0, len(key2), substring_length)]
    #perform comparison
    same_elements = [x != y for x, y in zip(chunks1, chunks2)]
    #calculate confidence
    percentConfidenceKeys= 1-np.dot(same_elements, chunk_penalty)

    return percentConfidenceKeys


#puts database inputs into list format
def record_row(primaryKey):
    #select person1, select person2
    conn = sqlite3.connect('Database 20 Million')

    # Create a cursor
    cursor = conn.cursor()

    # Define the row you want to retrieve (change 'your_table' to the table name and 'your_primary_key' to the primary key value)
    target_row_id = primaryKey

    # Execute a SELECT query to retrieve the specific row (change 'your_table' and 'your_primary_key_column' accordingly)
    cursor.execute("SELECT * FROM 'Database 20 Million' WHERE PrimaryKey = ?", (target_row_id,))

    # Fetch the row
    row = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Check if the row exists and then extract the inputs from the row
    if row:
        # You can access specific columns by index or by column name
        rowcontents = [row[0], row[1], row[2], row[3],row[4],row[5],row[6], row[7]]  # Needs to be updated in the case some rows don't exist, etc.
        # Should we use column names?
    else:
        print("Row not found.")

    # 'rowcontents' now contains a list of inputs from the specified row NOT INCLUDING PRIMARY  KEY, assuming primary key is the row[8] value
    return rowcontents

#Main code

count=0
totalComparisons=0
# some sort of for loop that loops through the database and picks out 2 different primkeys to compare 'primkey1', 'primkey2'
    inputs1= record_row('primkey1')
    inputs2= record_row('primkey2')
    if expectedConfidence(inputs1, inputs2)== confidenceKeys('primkey1', 'primkey2'):
        count+=1 #keeps track of the total number of times our key correctly calculated confidence
    totalComparisons+=1

print("Our confidence interval is correct ", (count/totalComparisons)*100, "% of the time")




