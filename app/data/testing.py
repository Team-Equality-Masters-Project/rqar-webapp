# Import standard libraries
import numpy as np
import pandas as pd
from io import BytesIO
import pickle
import time
import os

# Import NLP libs
from sentence_transformers import SentenceTransformer
import scipy.spatial
import faiss
embedder = SentenceTransformer('bert-base-nli-mean-tokens')

# Load final train dataset
path = 'dataset/main_data.csv'
df_QA = pd.read_csv(path)
corpus = list(np.unique(df_QA['question'].tolist()))

with open('faiss_index.pickle', "rb") as h:
     index = faiss.deserialize_index(pickle.load(h))

quest_embed = embedder.encode('plant care')
distances, indices = index.search(np.asarray(quest_embed).reshape(1,768),5)
L2_distance = distances[0] 
norm_L2_distance = L2_distance/np.linalg.norm(L2_distance) # scale distance to [0, 1]
relevant_docs = [corpus[indices[0,idx]] for idx in range(5)]
print(relevant_docs)