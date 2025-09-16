# -------------------------------------------------------------------------
# AUTHOR: Noah Ojeda
# FILENAME: similarity.py
# SPECIFICATION: This program reads a collection of documents from a CSV file, builds a binary document-term matrix, 
# and computes the pairwise cosine similarity between all documents to identify the most similar pair.
# FOR: CS 4440 (Data Mining) - Assignment #1
# TIME SPENT: ~2hr
# -----------------------------------------------------------*/
#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH
#AS numpy or pandas.
#You have to work here only with standard dictionaries, lists, and arrays
# Importing some Python libraries

import csv
from sklearn.metrics.pairwise import cosine_similarity
import math

documents = []

#reading the documents in a csv file
with open('cleaned_documents.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0: #skipping the header
            documents.append(row)

ids = []
texts = []
for row in documents:
    ids.append(row[0]) #storing every ID
    texts.append(row[1].strip().lower() if len(row)> 1 else "") #storing the text content


#Building the document-term matrix by using binary encoding.
#You must identify each distinct word in the collection using the white space as your character delimiter.
#--> add your Python code here

#creating a vocabulary set that has every word in document
vocab = set()
for text in texts:
    for word in text.split():
        vocab.add(word)
#creating a dictionary with the index of evry word
w2i = {}
index = 0
for word in vocab:
    w2i[word] = index
    index+=1

#creating a documentt term matrix
docTermMatrix = []
docOneCount = []

#if the word in texts exists in the document, then that position will be set to 1
#also counting the sums of 1's (words) in each document (for cosine similarity later)
for text in texts:
    vector = [0] * len(w2i)
    words = text.split()
    for w in words:
        if w in w2i:
            vector[w2i[w]] = 1
    docTermMatrix.append(vector)
    docOneCount.append(sum(vector))

               
# Compare the pairwise cosine similarities and store the highest one
# Use cosine_similarity([X], [Y]) to calculate the similarities between 2 vectors
# --> Add your Python code here
def cosineSimilarity(x, y):
    #find the dot product for the numerator
    dot = 0
    for i in range(len(x)):
        if x[i]==1 and y[i] == 1:
            dot+=1
    #get lenghths of both vectors
    len_x = math.sqrt(sum(x))
    len_y = math.sqrt(sum(y))

    #Avoid dividing by zero
    if len_x == 0 or len_y == 0:
        return 0.0
    
    return dot / (len_x * len_y)

# Print the highest cosine similarity following the information below
# The most similar documents are document 10 and document 100 with cosine similarity = x
# --> Add your Python code here

#Using the cosineSimilarity function
best_result = 0
best_docs = []
for i in range(len(docTermMatrix)):
    for j in range(i + 1, len(docTermMatrix)):
        result = cosineSimilarity(docTermMatrix[i], docTermMatrix[j])
        if result > best_result:
            best_result = result
            best_docs = [i, j]

print(f"The most similar documents are document {ids[best_docs[0]]} and document {ids[best_docs[1]]} with a cosine similarity = {best_result:0.6f}")
