import json
import pathlib
import regex
from pathlib import Path

source = "./ptt/politics/"
epoch=0
dest = "./"

pdata_p = []
with open(f"{source}{epoch}.json","r",encoding="utf-8") as f :
    pdata= json.load(f) 

for sub in pdata:
    if not sub : continue
    # print(sub)
    cdata_p=[]
    temp = {}
    for comment in sub['comments'] :
        if not comment : continue
        if not comment['comment'] : continue
        if temp and temp['user'] == comment['user'] : 
            comment['comment'] = temp['comment'] + comment['comment']
        else:
            #if 'comment' not in temp : continue
            #temp['comment'] = regex.sub('\n','',temp['comment'])
            if temp :
                cdata_p.append(temp)
        temp = comment
    sub['comments'] = cdata_p ;
    sub['content'] = regex.sub('\n','',sub['content'])
    sub['content'] = regex.sub('\s','',sub['content'])
    pdata_p.append(sub) ;

with open(f"{dest}{epoch}.json","w",encoding="utf-8") as f :
    json.dump(pdata_p,f,indent=2,ensure_ascii=False) 

    
             

        