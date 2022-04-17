from attr import attr
import tweepy
import json
from tqdm import tqdm
import time 

# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = '966341743493840902-535jPu9bcOOg4ZVlWHLUTpwIpbbclsN'
ACCESS_SECRET = '9iZ786fesMufr0ByyKTfg4Stlv7wWV7UzWbyDeUoybdsF'
CONSUMER_KEY = 'AUskGWcK43ZHQ9qWiPn7GyQfK'
CONSUMER_SECRET = 'se3JFzCtgAbAU8AtJcavFsTY3PDly676E3rtIGnEBFnRq48dw4'
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACUCagEAAAAAcK78c4UtqPZGzuso55KTMcJrd5A%3DZ4DuKhfD2uQolnIJ9N4OqX7ORtgDU2FC1lTWKWDrpeRauVcXxh"

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


# You can provide the consumer key and secret with the access token and access
# token secret to authenticate as a user
client = tweepy.Client(
    consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET,
    bearer_token=BEARER_TOKEN
)

with open('/home/swear/tmp/Stance Detection/wtwt_ids.json',mode='r',encoding='utf-8') as f:
        tweet_attributess = json.load(f) ;

fin_dataset = []

for tweet_attributes in tqdm(split(tweet_attributess,600)) :
    #print(tweet_attributes)
    tweet_ids = [i['tweet_id'] for i in tweet_attributes]

    responses_data = client.get_tweets(tweet_ids, tweet_fields=["created_at"]).data

    for attribute ,content in zip(tweet_attributes,responses_data) :
        #print(type(content))
        #raise
        del attribute['tweet_id']
        attribute['tweet'] = str(content)
        fin_dataset.append(attribute)
    time.sleep(30)

with open('/home/swear/tmp/Stance Detection/wtwt.json',mode='w',encoding='utf-8') as f:
    json.dump(fin_dataset,f,indent=2)