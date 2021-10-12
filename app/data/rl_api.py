import datetime
import json
import os
import time
import uuid

import torch
from azure.cognitiveservices.personalizer import PersonalizerClient
from azure.cognitiveservices.personalizer.models import (RankableAction,
                                                         RankRequest,
                                                         RewardRequest)
from msrest.authentication import CognitiveServicesCredentials
from parrot import Parrot

# Get reproducible paraphrases  
def random_state(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)


key = "202fa2f3b54c43eda9aa6e0873f59c3b"
endpoint = "https://personalizer-reddit.cognitiveservices.azure.com/"
random_state(1234)

# Create an instance of parror
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")
# Create a personalizer client
client = PersonalizerClient(endpoint, CognitiveServicesCredentials(key))


def get_query_paraphrases_ranked_by_adequacy(query):
   return parrot.augment(input_phrase=query, 
                        diversity_ranker="levenshtein",
                        do_diverse=False, 
                        max_return_phrases = 10, 
                        max_length=32, 
                        adequacy_threshold = 0.90, 
                        fluency_threshold = 0.70)

def get_query_paraphrases_ranked_by_fluency(query):
  return parrot.augment(input_phrase=query, 
                        diversity_ranker="levenshtein",
                        do_diverse=False, 
                        max_return_phrases = 10, 
                        max_length=32, 
                        adequacy_threshold = 0.70, 
                        fluency_threshold = 0.90)

def get_query_paraphrases_ranked_by_diversity(query):
  return parrot.augment(input_phrase=query, 
                        diversity_ranker="levenshtein",
                        do_diverse=True, 
                        max_return_phrases = 10, 
                        max_length=32, 
                        adequacy_threshold = 0.70, 
                        fluency_threshold = 0.70)


def get_query_paraphrases_ranked_by_type(query, rank_by_type):
  if (rank_by_type == "Adequacy"):
    return get_query_paraphrases_ranked_by_adequacy(query)
  elif (rank_by_type == "Fluency"):
    return get_query_paraphrases_ranked_by_fluency(query)
  else:
    return get_query_paraphrases_ranked_by_diversity(query)


def get_agent_reward(client, query_paraphrases, context, agent_actions):
    event_id = str(uuid.uuid4())
    rank_request = RankRequest(actions=agent_actions, context_features=context, event_id=event_id)
    response = client.rank(rank_request=rank_request)
    rankedList = response.ranking
    for ranked_query in rankedList:
        print('Suggestion :', ranked_query.id, ':',ranked_query.probability)

    print("CBQA recommended improved question : ", response.reward_action_id+".")
    user_feedback = input("Is this question acceptable?(y/n)\n")[0]

    reward_val = "0.0"
    if(user_feedback.lower()=='y'):
        reward_val = "1.0"
    elif(user_feedback.lower()=='n'):
        reward_val = "0.0"
    else:
        print("Your entered selection is invalid. Did you not like the recommended improvement?")

    return event_id, ranked_query, reward_val


def get_agent_actions(query_paraphrases):
    actions = []
    for paraphrase, score in query_paraphrases:
      a = RankableAction(id=paraphrase, features=[{"score":score}])
      actions.append(a)
    return actions


def get_user_preference(rl_option):
    res = {}
    res['question_impr_preference'] = rl_option
    return res


def get_max_reward(reward_a, reward_b, reward_c):
    list = [reward_a, reward_b, reward_c]
    return max(list)


def get_rl_text_impl(query, rl_option):
    improved_query_event_id = 0
    improved_query_reward = 0
    agent_actions = ""

    # Get user preference for question refinement technique
    user_preference = get_user_preference(rl_option)
    context =[user_preference]
    
    if (rl_option == "Adequacy"):
        rank_by_type = "Adequacy"
        query_paraphrases_ranked_by_adequacy = get_query_paraphrases_ranked_by_type(query, rank_by_type)

        # Get agent actions, reward for Adequacy
        agent_actions = get_agent_actions(query_paraphrases_ranked_by_adequacy)
        improved_query_event_id, improved_query, improved_query_reward = get_agent_reward(client, query_paraphrases_ranked_by_adequacy, context, agent_actions)
    elif (rl_option == "Fluency"):
        # Get ranked paraphrased queries by type Fluency
        rank_by_type = "Fluency"
        query_paraphrases_ranked_by_fluency = get_query_paraphrases_ranked_by_type(query, rank_by_type)
        
        # Get agent actions, reward for Fluency
        agent_actions = get_agent_actions(query_paraphrases_ranked_by_fluency)
        improved_query_event_id, improved_query, improved_query_reward = get_agent_reward(client, query_paraphrases_ranked_by_fluency, context, agent_actions)
    elif (rl_option == "Diversity"):
        # Get ranked paraphrased queries by type Diversity
        rank_by_type = "Diversity"
        query_paraphrases_ranked_by_diversity = get_query_paraphrases_ranked_by_type(query, rank_by_type)
        
        # Get agent actions, reward for Diversity
        agent_actions = get_agent_actions(query_paraphrases_ranked_by_diversity)
        improved_query_event_id, improved_query, improved_query_reward = get_agent_reward(client, query_paraphrases_ranked_by_diversity, context, agent_actions)
    else:
        # Get ranked paraphrased queries by type Diversity
        rank_by_type = "Adequacy"
        query_paraphrases_ranked_by_adequacy = get_query_paraphrases_ranked_by_type(query, rank_by_type)

        rank_by_type = "Fluency"
        query_paraphrases_ranked_by_fluency = get_query_paraphrases_ranked_by_type(query, rank_by_type)

        rank_by_type = "Diversity"
        query_paraphrases_ranked_by_diversity = get_query_paraphrases_ranked_by_type(query, rank_by_type)

        # Get agent actions, reward for Adequacy, Fluency, and Diversity
        agent_actions_adequacy  = get_agent_actions(query_paraphrases_ranked_by_adequacy)
        agent_actions_fluency   = get_agent_actions(query_paraphrases_ranked_by_fluency)
        agent_actions_diversity = get_agent_actions(query_paraphrases_ranked_by_diversity)
        event_id_adequacy, query_adequacy, reward_adequacy = get_agent_reward(client, query_paraphrases_ranked_by_adequacy, context, agent_actions_adequacy)
        event_id_fluency, query_fluency, reward_fluency = get_agent_reward(client, query_paraphrases_ranked_by_fluency, context, agent_actions_fluency)
        event_id_diversity, query_diversity, reward_diversity = get_agent_reward(client, query_paraphrases_ranked_by_diversity, context, agent_actions_diversity)
    
        # Get best among Adequacy, Fluency, and Diversity based on reward
        max_reward = get_max_reward(reward_adequacy, reward_fluency, reward_diversity)
        if (max_reward == reward_adequacy):
            improved_query_event_id = event_id_adequacy
            improved_query = query_adequacy
            improved_query_reward = reward_adequacy 
        elif (max_reward == reward_fluency):
            improved_query_event_id = event_id_fluency
            improved_query = query_fluency
            improved_query_reward = reward_fluency
        else: 
            improved_query_event_id = event_id_diversity
            improved_query = query_diversity
            improved_query_reward = reward_diversity
        
    return improved_query_event_id, improved_query_reward, improved_query


def get_rl_text(query, rl_option):
    user_preference = get_user_preference(rl_option)
    context =[user_preference]
    
    query_paraphrases_ranked = get_query_paraphrases_ranked_by_type(query, rl_option)

    agent_actions = get_agent_actions(query_paraphrases_ranked)

    event_id = str(uuid.uuid4())
    rank_request = RankRequest(actions=agent_actions, context_features=context, event_id=event_id)
    response = client.rank(rank_request=rank_request)
    return response.reward_action_id, event_id

def update_model(yes, no, event_id):
    reward_val = "0.0"
    if(yes == True):
        reward_val = "1.0"
    else:
        reward_val = "0.0"
    client.events.reward(event_id=event_id, value=reward_val)


