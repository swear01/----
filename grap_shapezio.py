from re import S
import praw
from psaw import PushshiftAPI
from datetime import datetime
import json
from tqdm import tqdm
from pathlib import Path 

sub_name = "shapezio"
submission_limit = 10
year = 2020

reddit = praw.Reddit(
    client_id = "J7tuNylJ6qvYQNXMhSrM2g",
    client_secret = "f1OhB2biWcbKKyoF98AWeQGkbtnovA",
    user_agent = "windows:grap_bot (by u/swear01)"
)
api = PushshiftAPI(reddit)
p = Path(".")
if not (p / sub_name).is_dir() :(p/sub_name).mkdir()

for month in tqdm(range(4,12)) :
    time_start = int(datetime(year,month,1).timestamp()) 
    time_end = int(datetime(year,month+1,1).timestamp())
    stored = []
    for submission_id in tqdm(api.search_submissions(
        after = time_start,
        before = time_end,
        subreddit = sub_name,
        #num_comments = 1,
        #filter = [] ,
    )):        
        s_data = []
        submission = reddit.submission(submission_id) 
        s_data.append(str(submission.id))
        submission.comments.replace_more(limit=None) ; #get a list of comment tree
        for comment_t in submission.comments :
            s_data.append([comment_t.id,comment_t.body,comment_t.score])
        stored.append(s_data) ;

    with open(f"./{sub_name}/{year}_{month}.json","w") as f :
        json.dump(stored,f,indent=2) ;
