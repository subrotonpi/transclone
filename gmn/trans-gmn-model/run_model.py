import sys
sys.settrace
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm, trange
from models import GMNnet
#from losses import SupConLoss
from graph_src import get_xml_asts, get_vocab_dict, get_graph_data, create_gmn_dataset
dir = '/home/egk204/projects/vizsciflow-tool/gmn/trans-gmn-model/'

def create_batches(data):
    batches = [data[graph:graph+batch_size] for graph in range(0, len(data), batch_size)]
    return batches

def get_prediction(data,label):
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
    return prediction, label

def test(dataset):
    count=0
    correct=0
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    results=[]
    for data,label in dataset:
        prediction, label=get_prediction(data,label) #model(data)
        cossim=F.cosine_similarity(prediction[0],prediction[1])
        results.append(cossim.item())
        prediction = torch.sign(cossim).item()

        if prediction>threshold and label.item()==1:
            tp+=1
        if prediction<=threshold and label.item()==-1:
            tn+=1
        if prediction>threshold and label.item()==-1:
            fp+=1
        if prediction<=threshold and label.item()==1:
            fn+=1
    print(tp,tn,fp,fn)
    p=0.0
    r=0.0
    f1=0.0
    if tp+fp==0:
        print('precision is none')
        return
    p=tp/(tp+fp)
    if tp+fn==0:
        print('recall is none')
        return
    r=tp/(tp+fn)
    f1=2*p*r/(p+r)
    print('precision', p , 'recall', r, 'F1', f1)
    file_object = open('result.txt', 'a')
    t = 'precision: '+str(p) +' recall: '+ str(r)+ ' F1: '+ str(f1)+'\n'
    file_object.write(t)
    return results
#--------------------------------------------------------------------------------------------------------

#hyperparameters
batch_size = 32
num_layers = 4
num_epochs = 10 #default 10
lr = 0.001
threshold = 0

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
#data goes here 
#train_data = valid_data = test_data = datalist_toy
fldr = 'alt_small/'
dstype = 'alt_dataset_small'
xml_asts = get_xml_asts()
vocab_dict, vocab_len = get_vocab_dict(xml_asts)
graph_data = get_graph_data(xml_asts, vocab_dict)
train_data, valid_data, test_data = create_gmn_dataset(graph_data, device)
model = GMNnet(vocablen=vocab_len,embedding_dim=100,num_layers=num_layers,device=device).to(device)
optimizer = optim.Adam(model.parameters(), lr=lr)
criterion=nn.CosineEmbeddingLoss()

temp = 0.1
criterion2=nn.MSELoss()#SupConLoss(temperature=temp)#

epochs = trange(num_epochs, leave=True, desc = "Epoch")
for epoch in epochs:# without batching
    print('epoch', epoch)
    batches=create_batches(train_data)
    totalloss=0.0
    main_index=0.0
    for index, batch in tqdm(enumerate(batches), total=len(batches), desc = "Batches"):
        optimizer.zero_grad()
        batchloss= 0
        
        for data,label in batch:
            prediction, label = get_prediction(data, label)
            cossim=F.cosine_similarity(prediction[0],prediction[1])
            batchloss=batchloss+criterion2(cossim,label)
            
        batchloss.backward(retain_graph=True)
        optimizer.step()
        loss = batchloss.item()
        totalloss+=loss
        main_index = main_index + len(batch)
        loss=totalloss/main_index
        epochs.set_description("Epoch (Loss=%g)" % round(loss,5))
    print('test result at epoch - ', epoch)
    test(test_data)
    
    
    torch.save(model.state_dict(),'gmn_'+str(epoch+1))
    print('model saved...')
    print(epoch, 'epoch done')
print('train, done...')
