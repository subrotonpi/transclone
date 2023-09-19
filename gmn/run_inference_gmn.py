import sys
import os
from pathlib import Path
project_root = str(Path(__file__).parents[1])

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import argparse
from tqdm import tqdm, trange
from gmn.createclone import createast,creategmndata,createseparategraph
import gmn.models
import random, os
import numpy as np



def test(args, model, dataset, device):
    count=0
    correct=0
    results=[]
    scores = []
    for data,label in dataset:
        label=torch.tensor(label, dtype=torch.float, device=device)
        x1, x2, edge_index1, edge_index2, edge_attr1, edge_attr2=data
        x1=torch.tensor(x1, dtype=torch.long, device=device)
        x2=torch.tensor(x2, dtype=torch.long, device=device)
        edge_index1=torch.tensor(edge_index1, dtype=torch.long, device=device)
        edge_index2=torch.tensor(edge_index2, dtype=torch.long, device=device)
        if edge_attr1!=None:
            edge_attr1=torch.tensor(edge_attr1, dtype=torch.long, device=device)
            edge_attr2=torch.tensor(edge_attr2, dtype=torch.long, device=device)
        data=[x1, x2, edge_index1, edge_index2, edge_attr1, edge_attr2]
        prediction=model(data)
        output=F.cosine_similarity(prediction[0],prediction[1])
        prediction = output.item()#torch.sign(output).item()
        # print(f"{prediction}>{args.threshold}?")
        scores.append(prediction)
        if prediction > float(args.threshold):
            results.append("clone")#, output.item()]) 
        else:
            results.append("non-clone")#, output.item()]) 
    return results, scores
def detect_clones(args):
    vocabsize = 58520 #77535
    device=torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    astdict,_,vocabdict=createast(args) #load saved voabdict for original dataset it was trained on (BCB)
    treedict=createseparategraph(args, astdict, vocabsize, vocabdict,device,mode='astonly')#,nextsib=args.nextsib,ifedge=args.ifedge,whileedge=args.whileedge,foredge=args.foredge,blockedge=args.blockedge,nexttoken=args.nexttoken,nextuse=args.nextuse)
    testdata=creategmndata(args, 0,treedict,vocabsize,vocabdict,device) #58520 #77535
    num_layers= 4#int(args.num_layers)
    model=gmn.models.GMNnet(vocablen=vocabsize,embedding_dim=100,num_layers=num_layers,device=device).to(device)
    model.load_state_dict(torch.load(args.src_gmn_path, map_location=device))
    model.eval()

    res, scores = test(args, model, testdata, device)
    
    import pandas as pd
    pairs_df = pd.read_csv(args.pairs, names=['code1', 'code2'])
    pairs_df['prediction'] = pd.Series(res)
    pairs_df['score'] = pd.Series(scores)
    res_df = pairs_df
    
    # df_res = pd.DataFrame(res, columns=['item']) #output.item(), add this in test
    # r = pd.concat([pairs_df, df_res], axis=1)
    res_df.to_csv(args.data+'predictions.csv', index=None)
    res_df.to_xml(args.data+'predictions.xml', index=None)
    return res, res_df
