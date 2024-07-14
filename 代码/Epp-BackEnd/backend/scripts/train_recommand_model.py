import torch
import torch.nn as nn
import torch.nn.functional as F

class SequencePoolingLayer(nn.Module):
    def __init__(self, sequence_mask_length):
        super(SequencePoolingLayer, self).__init__()
        self.sequence_mask_length = sequence_mask_length
    
    def forward(self, inputs):
        sequence_embeds, sequence_length = inputs
        mask = torch.arange(sequence_embeds.size(1)).expand_as(sequence_length) < sequence_length.unsqueeze(1)
        mask = mask.float().unsqueeze(2)
        masked_embeds = sequence_embeds * mask
        sum_embeds = torch.sum(masked_embeds, 1)
        return sum_embeds

class YouTubeNet(nn.Module):
    def __init__(self, sparse_input_length=1, dense_input_length=1, sparse_seq_input_length=50,
                 embedding_dim=64, neg_sample_num=10, user_hidden_unit_list=[128, 64]):
        super(YouTubeNet, self).__init__()
        
        self.embedding_dim = embedding_dim
        self.user_embedding = nn.Embedding(6040+1, embedding_dim)
        self.gender_embedding = nn.Embedding(2+1, embedding_dim)
        self.age_embedding = nn.Embedding(7+1, embedding_dim)
        self.occupation_embedding = nn.Embedding(21+1, embedding_dim)
        self.zip_embedding = nn.Embedding(3439+1, embedding_dim)
        self.item_id_embedding = nn.Embedding(3706+1, embedding_dim)
        
        self.sequence_pooling_layer = SequencePoolingLayer(sequence_mask_length=sparse_seq_input_length)
        
        self.user_fc_layers = nn.ModuleList()
        for i, hidden_unit in enumerate(user_hidden_unit_list):
            self.user_fc_layers.append(nn.Linear(embedding_dim * 6, hidden_unit))
        
        self.item_fc_layers = nn.Linear(embedding_dim * 2 * neg_sample_num, neg_sample_num)
        
    def forward(self, user_id, gender, age, occupation, zip_code, user_click_item_seq, user_click_item_seq_length,
                pos_item_sample, neg_item_sample):
        
        user_id_embedding = self.user_embedding(user_id)
        gender_embedding = self.gender_embedding(gender)
        age_embedding = self.age_embedding(age)
        occupation_embedding = self.occupation_embedding(occupation)
        zip_embedding = self.zip_embedding(zip_code)
        user_click_item_seq_embedding = self.item_id_embedding(user_click_item_seq)
        user_click_item_seq_embedding = self.sequence_pooling_layer([user_click_item_seq_embedding, user_click_item_seq_length])
        
        user_embedding = torch.cat([user_id_embedding, gender_embedding, age_embedding,
                                    occupation_embedding, zip_embedding, user_click_item_seq_embedding], dim=-1)
        
        for fc_layer in self.user_fc_layers:
            user_embedding = F.relu(fc_layer(user_embedding))
        
        pos_item_sample_embedding = self.item_id_embedding(pos_item_sample)
        neg_item_sample_embedding = self.item_id_embedding(neg_item_sample)
        
        item_embedding = torch.cat([pos_item_sample_embedding, neg_item_sample_embedding], dim=1)
        item_embedding = item_embedding.permute(0, 2, 1)
        
        dot_output = torch.matmul(user_embedding.unsqueeze(1), item_embedding)
        dot_output = F.softmax(dot_output, dim=-1)
        
        return dot_output

# 使用示例
model = YouTubeNet()
user_id = torch.LongTensor([1])
gender = torch.LongTensor([0])
age = torch.LongTensor([1])
occupation = torch.LongTensor([10])
zip_code = torch.LongTensor([1001])
user_click_item_seq = torch.LongTensor([[1, 2, 3, 4, 5]])
user_click_item_seq_length = torch.LongTensor([5])
pos_item_sample = torch.LongTensor([6])
neg_item_sample = torch.LongTensor([[7, 8, 9, 10, 11]])

output = model(user_id, gender, age, occupation, zip_code, user_click_item_seq, user_click_item_seq_length,
               pos_item_sample, neg_item_sample)
print(output.shape)  # Output shape: (batch_size, 1, 11)
