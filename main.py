import json
import transformers
from tqdm import tqdm
import torch
import numpy as np
from transformers import BertTokenizerFast, AutoModel, BertConfig
from sklearn.cluster import KMeans,AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import davies_bouldin_score

dataset_path = './0big.json'


tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
config = BertConfig.from_pretrained("ckiplab/bert-base-chinese", output_hidden_states=True)
model = AutoModel.from_pretrained('ckiplab/bert-base-chinese',config=config)


with open(dataset_path,"r",encoding="utf-8") as f :
    pdata= json.load(f) 

pdata_p = []    
for sub in pdata:
    if not sub : continue
    # print(sub)
    cdata_p=[]
    cluster_list = []
    temp = {}
    for comment in sub['comments'] :
        #print(pdata[0]['comments'][0])
        #test_comment = pdata[0]['comments'][0]['comment']
        tokened_comment = tokenizer.encode(comment['comment'], padding=True, truncation=True, return_tensors="pt")
        #print(tokened_comment)
        #padded_comment =
        output = model(tokened_comment)
        #print(output)
        hidden_state = output[2]
        #print(hidden_state)
        embed_list = (hidden_state[-1]+hidden_state[-2]+hidden_state[-3])[0]
        #print(embed_list)
        embed_sum = embed_list[0].clone()
        for embed in embed_list[1:] :
            embed_sum += embed 
        #print(type(embed_sum))            
        embed_sum_list = torch.div(embed_sum,len(embed_list)).detach().numpy().tolist()
        #print(embed_sum)
        cluster_list.append(np.array(embed_sum_list))
        
    # pca and clustering
    pca = PCA(n_components=16)
    pca.fit(cluster_list)
    pca_cluster_list = pca.transform(cluster_list)
    #print(pca_cluster_list)
    clustering = AgglomerativeClustering(n_clusters= 5)###### 找好方法 分cluster
    clustering.fit(pca_cluster_list)
    label = clustering.labels_

    score = davies_bouldin_score(pca_cluster_list, labels)

    #sub['comments'] = cdata_p

    for i, comment in tqdm(enumerate(sub['comments'])) :
        comment['pca_embed'] = pca_cluster_list[i].tolist()
        comment['label'] = int(label[i])
        print(label)
        cdata_p.append(comment)
    sub['comments'] = cdata_p
    pdata_p.append(sub)

with open(f"./0embed.json","w",encoding="utf-8") as f :
    json.dump(pdata_p,f,indent=2,ensure_ascii=False)    

