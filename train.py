import json
import numpy as np
from nltk_utils import tokenize, stem, bag_of_words
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open('data.json', 'r') as f:
    data=json.load(f)


all_words=[]
tags=[]
xy=[]

for i in data['intents']:
        tag = i['tag']
        tags.append(tag)
        for p in i['patterns']:
            w=tokenize(p)
            all_words.extend(w)
            xy.append((w,tag))

all_words=stem(all_words)
all_words=sorted(set(all_words))
tags=sorted(set(tags))

x_train=[]
y_train=[]

for (p,tag) in xy:
        bag=bag_of_words(p,all_words)
        x_train.append(bag)
        label=tags.index(tag)
        y_train.append(label)

x_train=np.array(x_train)
y_train=np.array(y_train)
# y_train = y_train.dtype(torch.LongTensor)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_sam=len(x_train)
        self.x_data=x_train
        self.y_data=y_train

    def __getitem__(self,index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_sam

batch_size=8
hidden_size=8
output_size=len(tags)
input_size=len(x_train[0])
learning_rate=0.001
n_epochs=1000

dataset = ChatDataset()
train_loader=DataLoader(dataset=dataset,batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model =NeuralNet(input_size,hidden_size,output_size).to(device)

criterion= nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

for epoch in range(n_epochs):
    for (words,labels) in train_loader:
        words=words.to(device)
        labels=labels.to(device)
        labels=labels.long()

        #forword
        outputs=model(words)
        loss=criterion(outputs,labels)

        #backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if (epoch+1)%100 ==0:
        print(f'epoch {epoch+1}/{n_epochs}, loss = {loss.item():.4f}')

print(f'final loss = {loss.item():.4f}')

data={
    "model_state":model.state_dict(),
    "input_size":input_size,
    "output_size":output_size,
    "hidden_size":hidden_size,
    "all_words":all_words,
    "tags":tags
}

# FILE = "data.pth"
# torch.save(model,FILE)
# print(f'Training complete. File saved to {FILE}')

# with open('output.json', 'w') as f:
#     json.dump(data,f)
# print("Done")