import praw
import json
import requests
from urllib import request
from urllib.request import urlopen
from datetime import datetime, timezone
import pytz
from numerize import numerize 
import re


def utc_to_local(utc_dt):
    PST = pytz.timezone('US/Pacific')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=PST)


def get_details(sub_name):

    reddit = praw.Reddit(client_id='df1cB9BuzYrQtQ',
                     client_secret='dUYLPgSdhduMVi2OUYrbywO0jguOww',
                     user_agent='scraper')

    #find_a_reddit = reddit.subreddit('FindAReddit')

    url = 'https://www.reddit.com/{}/about.json'.format(sub_name)
    req = request.Request(url)
    req.add_header('User-Agent', 'red-bot')
    response = request.urlopen(req)
  
    data_json = json.loads(response.read())
    
    img_url = data_json["data"]["icon_img"]
    if img_url == '':
        img_url = 'https://b.thumbs.redditmedia.com/j3ZrH05Hb0PPoqYKjlPr6oYo47kFjqg7LF6_3QMijGk.png'
    
    desc = data_json["data"]["public_description"]

    desc = format_desc(desc)

    sub_url = 'https://www.reddit.com/'+ sub_name

    banner_img_url = data_json["data"]["banner_img"]

    subscriber_count = numerize.numerize(data_json["data"]["subscribers"])

    created_utc = data_json["data"]["created_utc"]

    created_time = created_utc #utc_to_local(created_utc)

    return img_url, sub_name, desc, sub_url, banner_img_url, subscriber_count, created_time

def format_desc(desc):
    clean = re.compile('<.*?>')
    desc = re.sub(clean, '', desc)
    desc = desc.replace('\n', '')
    return desc[:100] + (desc[100:] and '...')