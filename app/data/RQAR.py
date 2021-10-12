# Import standard and NLP libraries
import numpy as np
import pandas as pd
import pickle
from data.preprocessing import normalize_text
from sentence_transformers import SentenceTransformer
import faiss

# Load final train dataset
df_QA = pd.read_csv('data/dataset/main_data.csv')
corpus = list(np.unique(df_QA['question_vocab'].tolist()))
# Load Semantic Search Trained BERT
embedder = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
# Load Faiss
with open('data/faiss_index.pickle', "rb") as h:
     index = faiss.deserialize_index(pickle.load(h))

# Recommender System
def RQAR(new_question):

     num_rec = 10 # Number of related questions/neighbors to search for with Faiss
     question_type = 'question_vocab' # Using cleaned historical question

     # 0. Preprocess question and add topic inference
     new_question = normalize_text(new_question)

     # 1. Encode question and find relevant doc
     quest_embed = embedder.encode(new_question)
     distances, indices = index.search(np.asarray(quest_embed).reshape(1,quest_embed.shape[0]),num_rec)
     L2_distance = distances[0] 
     norm_L2_distance = L2_distance/np.linalg.norm(L2_distance) # scale distance to [0, 1]
     relevant_docs = [corpus[indices[0,idx]] for idx in range(num_rec)]

     # 2. Create a new dataframe for suggestion
     relevant = pd.DataFrame({'relevant_question':relevant_docs, 'semantic_similarity':norm_L2_distance})
     relevant_subreddit = relevant.merge(df_QA, left_on='relevant_question', right_on=question_type, how='inner')
     relevant_subreddit = relevant_subreddit[['relevant_question','suggested_subreddits', 'semantic_similarity', 'comment_upvotes']]

     # 3. Calculate total weight by combining upvotes, occurrences, similarity
     relevant_subreddit['occurrence'] = relevant_subreddit.groupby('suggested_subreddits')['suggested_subreddits'].transform('count')
     relevant_subreddit['norm_upvotes'] = (relevant_subreddit['comment_upvotes']-relevant_subreddit['comment_upvotes'].min())/(relevant_subreddit['comment_upvotes'].max()-relevant_subreddit['comment_upvotes'].min())
     # Polynomial method, tune to optimize result
     relevant_subreddit['total_weight'] = 0.75*(1 - relevant_subreddit['semantic_similarity']) + 0.10*relevant_subreddit['norm_upvotes'] + 0.15*(relevant_subreddit['occurrence']/num_rec)

     relevant_subreddit = relevant_subreddit[relevant_subreddit['total_weight'].notnull()]
     relevant_subreddit.total_weight = round((relevant_subreddit.total_weight * 100))
     relevant_subreddit = relevant_subreddit.drop_duplicates(subset='suggested_subreddits').sort_values(by='total_weight', ascending=False).reset_index(drop=True)

     # Formating
     RQAR_dict = dict(zip(relevant_subreddit.suggested_subreddits, relevant_subreddit.total_weight))
     RQAR_dict = sorted(RQAR_dict.items(), key=lambda x: (x[1],x[0]), reverse=True)
     return RQAR_dict
