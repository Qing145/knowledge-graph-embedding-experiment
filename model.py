import torch
import torch.nn as nn
import torch.nn.functional as F

class TransE(nn.Module):
    def __init__(self, ent_tot, rel_tot, em_dim = 100, p_norm = 2, norm_flag = False):
        super(TransE, self).__init__()
        self.name = 'TransE'
        self.dim = em_dim
        self.p_norm = p_norm
        self.norm_flag = norm_flag
        self.ent_embeddings = nn.Embedding(ent_tot, em_dim, max_norm = 1)
        self.rel_embeddings = nn.Embedding(rel_tot, em_dim)

        self.init_weights()
        
    def init_weights(self):
        nn.init.xavier_uniform_(self.ent_embeddings.weight.data)
        nn.init.xavier_uniform_(self.rel_embeddings.weight.data)
        


    def _calc(self, h, r, t):
        '''
            calculate ||h + r - t||_n 
        '''
        if self.norm_flag:
            h = F.normalize(h, 2, -1)
            r = F.normalize(r, 2, -1)
            t = F.normalize(t, 2, -1)

        score = torch.norm(h + r - t, self.p_norm, -1).flatten()
        return score

    def forward(self, h, r, t, batch_size):  
        batch_h = self.ent_embeddings(h)
        batch_r = self.rel_embeddings(r)
        batch_t = self.ent_embeddings(t)
        score = self._calc(batch_h, batch_r, batch_t)   
        pos_score = score[0: batch_size]
        neg_score = score[batch_size:]
        return pos_score, neg_score    

    def predict(self, h, r, t):
        batch_h = self.ent_embeddings(h)
        batch_r = self.rel_embeddings(r)
        batch_t = self.ent_embeddings(t)
        score = self._calc(batch_h, batch_r, batch_t)       
        return score
        

class DistMult(nn.Module):
    def __init__(self, ent_tot, rel_tot, em_dim = 50):
        super(DistMult, self).__init__()
        self.ent_embeddings = nn.Embedding(ent_tot, em_dim, max_norm=1)
        self.rel_embeddings = nn.Embedding(rel_tot, em_dim)

        # self.criterion = nn.Softplus()

        self.init_weights()


    def init_weights(self):
        nn.init.xavier_uniform_(self.ent_embeddings.weight.data)
        nn.init.xavier_uniform_(self.rel_embeddings.weight.data)

    def _calc(self, h, r, t):
        return torch.sum(h * t * r, -1)

    def forward(self, batch_h, batch_r, batch_t, batch_size, batch_y=0):
        h = self.ent_embeddings(batch_h)
        t = self.ent_embeddings(batch_t)
        r = self.rel_embeddings(batch_r)
        #y = torch.from_numpy(batch_y).type(torch.FloatTensor)

        score = self._calc(h, r, t)

        pos_score = score[0: batch_size]
        neg_score = score[batch_size: len(score)]

        # regul = torch.mean(h ** 2) + torch.mean(t ** 2) + torch.mean(r ** 2)
        # loss = torch.mean(self.criterion(score * y)) + self.params.lmbda * regul
        # loss = self.criterion(pos_score, neg_score, torch.Tensor([-1]))
        
        return pos_score, neg_score
    def predict(self, batch_h, batch_r, batch_t):
        h = self.ent_embeddings(batch_h)
        t = self.ent_embeddings(batch_t)
        r = self.rel_embeddings(batch_r)
        #y = torch.from_numpy(batch_y).type(torch.FloatTensor)

        score = self._calc(h, r, t)

        # regul = torch.mean(h ** 2) + torch.mean(t ** 2) + torch.mean(r ** 2)
        # loss = torch.mean(self.criterion(score * y)) + self.params.lmbda * regul
        # loss = self.criterion(pos_score, neg_score, torch.Tensor([-1]))
        
        return score


if __name__=='__main__':
    model = transE(100, 100, init_embed=True)
    h = torch.LongTensor([1])
    r = torch.LongTensor([1])
    t = torch.LongTensor([1])
    a = model(h, r, t)







