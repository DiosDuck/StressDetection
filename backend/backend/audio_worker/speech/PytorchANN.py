import torch
import torch.nn as nn
import torch.nn.functional as F


class Net4(nn.Module):
    def __init__(self,n=64,o=4):
        super().__init__()
        aux=int(n/2)+2
        self.fc1=nn.Linear(n, aux)
        self.fc2=nn.Linear(aux,aux)
        self.fc3=nn.Linear(aux,aux)
        #self.fc4=nn.Linear(aux,aux)
        self.fc5 = nn.Linear(aux, o)

    def forward(self, x):
        x=F.relu(self.fc1(x))
        x=F.relu(self.fc2(x))
        x=F.relu(self.fc3(x))
        #x=F.relu(self.fc4(x))
        x=self.fc5(x)

        return F.log_softmax(x,dim=1)