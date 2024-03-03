#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np


# In[6]:


def compute_entropy(arr):
    ratio = np.sum(arr)/len(arr)
    if ratio == 0 or ratio == 1:
        return 0
    return -np.log(ratio) * ratio - np.log(1-ratio) * (1-ratio)


# In[7]:


def compute_entropy_table(table):
    entropies = []
    for j in range(table.shape[1]):
        entropies.append(compute_entropy(table[:,j]))
    return entropies


# In[9]:


#testing random table
randomTable = np.random.randint(2, size=(5,10))
entropies = compute_entropy_table(randomTable)
print("Random Table")
print(randomTable)
print("Entropies")
print(np.round(entropies,2))


# In[ ]:


'''
Helper Functions That Need Implementing:
1. get_max_index
2. subset
'''

question_order = []
#Psuedocode For Computing Question Ordering
def overall_recursive_strategy(table):
    #First Compute the Entropy for Each Question (Each Column)
    
    overall_entropy = compute_entropy_table(table)
    
    if np.sum(overall_entropy) == 0:
        #If we cannot divide the table anymore we break
        break
    
    #Next compute the question with the highest entropy
    question_col_highest_entropy = get_max_index(overall_entropy)
    
    #Append to question_order the question we should ask. Note that we need to be careful
    #when we finally interpret question_order
    question_order.append(question_col_highest_entropy)
    
    #Divide Table Into Two Pieces
    subset_table_yes = subset(table, col_index, 1)
    subset_table_no = subset(table, col_index, 0)
    
    #Proceed recursively
    overall_recursive_strategy(subset_table_yes)
    overall_recursive_strategy(subset_table_no)


# In[ ]:


#Helper Functions
def get_max_index(arr):
    #Return the index with maximum value in the array
    return None

def subset(table, col_index, value):
    #subset the table by all rows where the col given by col_index, is equal to value
    return None
    
    

