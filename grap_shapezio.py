from re import S
from pmaw import PushshiftAPI
from datetime import datetime, tzinfo, timezone
import json
from tqdm import tqdm
from pathlib import Path 

sub_name = "shapezio"
submission_limit = 10
year = 2020
workers = 60

'''
reddit = praw.Reddit(
    client_id = "J7tuNylJ6qvYQNXMhSrM2g",
    client_secret = "f1OhB2biWcbKKyoF98AWeQGkbtnovA",
    user_agent = "windows:grap_bot (by u/swear01)",
)
#'''

api = PushshiftAPI(num_workers = workers) #we don't need enrichment
p = Path(".")
if not (p / sub_name).is_dir() :(p/sub_name).mkdir()
time_start = int(datetime(year,1,1,tzinfo=timezone.utc).timestamp()) 
time_end = int(datetime(year+1,1,1,tzinfo=timezone.utc).timestamp()) 
print(time_start,time_end)
epoch = 0  
while 1 :
    stored = []
    submission_ids = list(api.search_submissions(
        subreddit = sub_name,        
        after = time_start,
        before = time_end,
        limit = 10,
        mem_safe = True
    ))
    print(1,epoch)
    for submission_id in tqdm(submission_ids):  
        print(4,epoch)      
        s_data = []
        s_data.append(str(submission_id))
        comment_ids = api.search_submission_comment_ids(ids=submission_id)
        print(5,epoch)  
        for comment in tqdm(api.search_comments(ids=comment_ids)) :
            print(3,epoch)
            s_data.append([comment["id"],comment["body"],comment["score"]])
        stored.append(s_data) 
    print(2,epoch)
    with open(f"./{sub_name}/{epoch}.json","w") as f :
        json.dump(stored,f,indent=2) 

    if api.search_submissions(ids=submission_ids[-1]).time >= time_end : break
    epoch+=1
