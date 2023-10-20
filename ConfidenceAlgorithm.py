import pandas as pd
import numpy as np

##establishing penalties
firstname= .1
lastname= .15
month= 1
day= 1
year= 1
ss= 1
dl= .1
gender= .1
chunk_penalty=[firstname, lastname, month, day, year, ss, dl, gender]

##Confidence Calculation
def confidence_interval_for_key_comparison(key1, key2, chunk_penalty):
    chunk_size = 1
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
    percentConfidence= 1-np.dot(chunk_similarity, chunk_penalty)

    return percentConfidence

def possible_matches(key1,key2, percentConfidence):
    if percentConfidence>=.8:
        matchdict[key2]=[key1, percentConfidence]

def compare_keys(key1, key2):
    percentConfidence = confidence_interval_for_key_comparison(key1, key2, chunk_penalty)
    possible_matches(key1, key2, percentConfidence)

def key_selection(key1, db2):
    for i in db2['pk2']:
        key2= i
        compare_keys(key1,key2)

matchdict={}
DMVdb= pd.read_excel('PKConfidenceTest.xlsx')
DMVdb=DMVdb.astype(str)
key1='44444444'
key_selection(key1, DMVdb)

#check if there is only one 100% match: 
count= sum(1 for value in matchdict.values() if value[1] == 1)
if count==1:
    for i in matchdict:
        match=matchdict[i]
        if match[1]==1:
            print("Primary key ", i, " in DMV database is an exact match")
else: 
    for i in matchdict:
        match=matchdict[i]
        print("Primary key ", i, " is ", match[1]*100, "% likely a unique match with key ", key1)

