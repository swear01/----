import praw
import json
from praw.reddit import Subreddit
from tqdm import tqdm

sub_name = "shapezio"
submission_limit = 10

subreddit = praw.Reddit (
    client_id = "J7tuNylJ6qvYQNXMhSrM2g",
    client_secret = "f1OhB2biWcbKKyoF98AWeQGkbtnovA",
    user_agent = "windows:grap_bot (by u/swear01)"
).subreddit(sub_name)

stored = []
stored.append(sub_name)
top_submissions = subreddit.top("all",limit=submission_limit)

for submission in tqdm(top_submissions,total=submission_limit) :
    s_data = []
    s_data.append(submission.id)
    submission.comments.replace_more(limit=200) ; #get a list of comment tree
    for comment_t in submission.comments :
        s_data.append([comment_t.id,comment_t.body,comment_t.score])
    stored.append(s_data) ;

with open("./shapezio.json","w") as f :
    json.dump(stored,f,indent=2) ;
