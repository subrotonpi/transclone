import sys
import os
from pathlib import Path
project_root = str(Path(__file__).parents[1])

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
import argparse
from tqdm import tqdm, trange
# from gmn.createclone import createast,creategmndata,createseparategraph #for javalang version
from gmn.graph_src import get_xml_asts, get_vocab_dict, get_graph_data, create_gmn_dataset #srcML
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
    
    # javalang version
    # astdict,_,vocabdict=createast(args) #load saved voabdict for original dataset it was trained on (BCB)
    # treedict=createseparategraph(args, astdict, vocabsize, vocabdict,device,mode='astonly')#,nextsib=args.nextsib,ifedge=args.ifedge,whileedge=args.whileedge,foredge=args.foredge,blockedge=args.blockedge,nexttoken=args.nexttoken,nextuse=args.nextuse)
    # testdata=creategmndata(args, 0,treedict,vocabsize,vocabdict,device) #58520 #77535
    
    #srcML version
    xml_asts = get_xml_asts(args)
    vocab_dict, vocab_len = get_vocab_dict(xml_asts, args)
    graph_data = get_graph_data(xml_asts, vocab_dict, args)
    test_data = create_gmn_dataset(graph_data, device, args)
    
    num_layers= 4#int(args.num_layers)
    model=gmn.models.GMNnet(vocablen=vocabsize,embedding_dim=100,num_layers=num_layers,device=device).to(device)
    model.load_state_dict(torch.load(args.src_gmn_path, map_location=device))
    model.eval()

    res, scores = test(args, model, test_data, device)
    
    import pandas as pd
    pairs_df = pd.read_csv(args.pairs, names=['code1', 'code2'])
    pairs_df['prediction'] = pd.Series(res)
    pairs_df['score'] = pd.Series(scores)
    res_df = pairs_df
    
    # df_res = pd.DataFrame(res, columns=['item']) #output.item(), add this in test
    # r = pd.concat([pairs_df, df_res], axis=1)
    res_df.to_csv(args.data+'/predictions.csv', index=None)
    res_df.to_xml(args.data+'/predictions.xml', index=None)
    for_muttion_framework(args, res_df)
    return res, res_df

def for_muttion_framework(args, res_df):
    com = pd.read_csv(args.data + "/combined_functions.csv")
    x = ""
    for ind, row in res_df.iterrows(): #code1,code2,prediction,score
        c1 = com[com.uid==row.code1]
        f1 = "/".join(c1.file_path.item().split("/")[1:])
        s1 = c1.start.item() 
        e1 = c1.end.item()
        
        c2 = com[com.uid==row.code2]
        f2 = "/".join(c2.file_path.item().split("/")[1:])
        s2 = c2.start.item() 
        e2 = c2.end.item()
        
        
        if row.prediction == "clone":
            # /Path/to/File1.java,5,10,/Path/to/File2,20,25\
            tmp = f"{f1}, {s1}, {e1}, {f2}, {s2}, {e2}\n"
            x += tmp
    wp = f"{args.data}/mutation_formatted.txt"
    with open(wp, 'w') as file:
        # Write the string to the file
        file.write(x)    
    print(wp)
    
            
        
        
    