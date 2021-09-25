import numpy as np
import pandas as pd


game_subreddits = {'pokemon': 90, 'Minecraft':80, 'hearthstone':70, 'wow':60, 'starcraft':50, 'pcgaming': 50}
coding_subreddits = {'AskProgramming': 99, 'LearnProgramming': 98, 'Coding': 95, 'JavaScript': 94, 'WebDev': 93, 'CSS': 92, 'LearnJavaScript': 91, 'ProWordPress': 90, 'Rails': 90, 'LearnPython': 90, 'BadCode': 90, 'CodingHelp': 90}
gardening_subreddits = {'plantclinic': 99, 'gardening': 98, 'plants': 97, 'houseplants': 89, 'DramaticHouseplants': 88, 'IndoorGarden': 70}

def find_subreddits(question):
    if 'game' in question:
        return game_subreddits
    elif 'coding' in question:
        return coding_subreddits 
    else:
        return gardening_subreddits