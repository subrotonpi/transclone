import pandas as pd
import xml.etree.ElementTree as ET
import os, sys
import difflib
import ctypes
import stat
from pylibsrcml import srcml
import subprocess
import torch
# dstype = 'dataset_large'

dir = ''
device=torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
#dictionary helper functions
def print_dict(d):
    for k,v in d.items():
        print('\n-----------\nkey: ', k, '\nvalue:', v, '\n-----------\n')
def count_dict(d):
    count=0
    for _ in d.items():
        count+=1
    return count
def is_dict_empty(d):
    return True if count_dict(d)==0 else False

def get_xml_tree(code, args):
    def forc(j_path, c):
        f = open(j_path, "w")
        f.write(c)
        f.close()
    j_path = args.data+'/temp/temp_g1.java'
    xml_path = args.data+'/temp/temp_g1.java.xml'

    try:
        forc(j_path, code)
        r = subprocess.run(['srcml', j_path,'-o',xml_path], timeout=5)      
    except subprocess.TimeoutExpired as e:
        forc(j_path,'')
        r = subprocess.run(['srcml', j_path,'-o',xml_path], timeout=5) 
    tree = ET.parse(xml_path)
    # rt = tree.getroot()      
    return tree

def get_code_fragments_dictionary(args):
    # fi.columns =['id', 'code']
    codes = pd.read_csv(args.data+"/combined_functions.csv")
    merged = codes[['uid', 'code']]
    code_dict = dict(merged.values) 
    return code_dict

def get_xml_asts(args):
    vocab_dict = {}
    code_fragments = get_code_fragments_dictionary(args)
    xml_asts = {}
    for uid, fragment in code_fragments.items():
        # print(uid)
        individual_xml = get_xml_tree(fragment, args)
        xml_asts[uid]= individual_xml
    return xml_asts
#original implementation from gnn clone paper
def create_pair_data(graph_dict,pair_info, device):
    datalist=[]
    for row in range(len(pair_info)):
        code1path = pair_info.iloc[row]['c1'] 
        code2path = pair_info.iloc[row]['c2']
        # label = pair_info.iloc[row]['label']        
        if code1path in graph_dict and code2path in graph_dict:
            data1 = graph_dict[code1path]
            data2 = graph_dict[code2path]
            x1,edge_index1,edge_attr1,ast1length=data1[0][0],data1[0][1],data1[0][2],data1[1]
            x2,edge_index2,edge_attr2,ast2length=data2[0][0],data2[0][1],data2[0][2],data2[1]
            if edge_attr1==[]:
                edge_attr1 = None
                edge_attr2 = None
            data = [[x1, x2, edge_index1, edge_index2, edge_attr1, edge_attr2], -1]
            datalist.append(data)
    return datalist
def create_gmn_dataset(graph_dict, device, args):
    test_list =  pd.read_csv(args.data+"/pairs.csv", names=['c1', 'c2'])
    #check
    test_list=test_list.head(10)

    test_data=create_pair_data(graph_dict,test_list,device=device)
    return test_data
    
def get_tokens(current_node, vocab_dict):
    def add_vocab(item, vocab_dict):
        if item not in vocab_dict.keys():
            vocab_dict[item]=len(vocab_dict.keys())
    #process current node
    token = str(current_node.tag).replace("{http://www.srcML.org/srcML/src}","")
    add_vocab(token, vocab_dict) 
    #special case, for current node, attribute, literal value should be added as children to make each path distinct
    cattr = current_node.attrib
    ctoken = current_node.text
    if token != 'unit':
        if bool(cattr):
            for _, token_ in cattr.items():
                add_vocab(token_, vocab_dict)
        if bool(ctoken):
            add_vocab(ctoken, vocab_dict)        
    #visit all children            
    for child in current_node:
        get_tokens(child, vocab_dict)

def get_vocab_dict(xml_asts, args):
    vocab_dict = { }
    for id_, tree in xml_asts.items():
        get_tokens(tree.getroot(), vocab_dict)

    # print('vocab_dict:', vocab_dict)
    vocab_len = len(vocab_dict.keys())
    print('vocab len for test data ',vocab_len)
    return vocab_dict, vocab_len

def add_edge(parent_id, n_id, edge_src, edge_tgt):
    edge_src.append(parent_id)
    edge_tgt.append(n_id)
    edge_src.append(n_id)
    edge_tgt.append(parent_id)
    
def tour_de_tree(current_node, vocab_dict, node_list, node_index_list, edge_src, edge_tgt, parent_id=-1):           
    #process current node
    token = str(current_node.tag).replace("{http://www.srcML.org/srcML/src}","")  
    current_node_id = len(node_list)
    node_list.append(current_node_id)
    node_index = vocab_dict[token]
    node_index_list.append([node_index])
    if current_node_id != 0 :
        #add edge
        add_edge(parent_id, current_node_id, edge_src, edge_tgt) 
        #special case, for current node, attribute, literal value should be added as children to make each path distinct
        cattr = current_node.attrib
        ctoken = current_node.text  
        if bool(cattr):
            for _, token_ in cattr.items():
                n_id = len(node_list)
                node_list.append(n_id)
                nindli = vocab_dict[token_]
                node_index_list.append([nindli])
                add_edge(parent_id, n_id, edge_src, edge_tgt)
                
        if bool(ctoken):
                n_id = len(node_list)
                node_list.append(n_id)
                nindli = vocab_dict[ctoken]
                node_index_list.append([nindli])
                add_edge(parent_id, n_id, edge_src, edge_tgt)
    #visit all children            
    for child in current_node:
        tour_de_tree(child, vocab_dict, node_list, node_index_list, edge_src, edge_tgt, current_node_id)
    
    #add src tgt to edge index
    edge_index=[edge_src, edge_tgt]
            
    return node_list, node_index_list, edge_index

def get_graph_data(xml_asts, vocab_dict, args, graph_data={}):
    for id_, tree in xml_asts.items():
        node_list, node_index_list, edge_index = tour_de_tree( tree.getroot(),vocab_dict, node_list=[], node_index_list=[],edge_src=[], edge_tgt=[], parent_id=-1 )        
        edge_attr = []
        ast_length = len(node_index_list)
        
        graph_data[id_] = [[node_index_list, edge_index, edge_attr ], ast_length]
    return graph_data

