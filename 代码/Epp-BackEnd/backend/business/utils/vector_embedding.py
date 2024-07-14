import os
import django

from transformers import AutoTokenizer, AutoModel
import torch
from tqdm import tqdm
import requests
from vector_database.chatglm_translate import translate_zh2en
from vector_database.milvus_test import *
from business.models import Paper
from django.conf import settings

model_dir = "vector_database/sci_bert"


def get_sci_bert():
    model = AutoModel.from_pretrained(model_dir)
    print(f'Model loaded from {model_dir} OK!')
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    print(f'Tokenizer loaded from {model_dir} OK!')

    if torch.cuda.is_available():
        device = torch.device("cuda")  # 使用 CUDA
        model.to(device)  # 将模型移动到 GPU
    else:
        device = torch.device("cpu")  # 仅使用 CPU
        print("CUDA is not available. Using CPU instead.")
    return tokenizer, model


def text_embedding(text, tokenizer, model):
    # 使用分词器编码文本
    inputs = tokenizer(text, return_tensors="pt")
    # print(inputs)
    for k, _ in inputs.items():
        inputs[k] = inputs[k].cuda()
    # 3. 获取词嵌入
    # 传入编码后的文本到模型，得到输出
    outputs = model(**inputs)

    # 输出的 `outputs` 是一个包含多个层的输出的元组，我们通常使用最后一层的隐藏状态
    last_hidden_states = outputs.last_hidden_state

    # last_hidden_states 的形状是 [batch_size, sequence_length, hidden_size]
    # 这里 batch_size=1, sequence_length 是输入文本的长度（包括特殊字符）

    # print("Shape of output embeddings:", last_hidden_states.shape)
    # print("Output tensor:", last_hidden_states)

    # 4. (可选) 使用输出
    # 例如，你可以取第一个 token (通常是 [CLS] token) 的嵌入来做文本分类任务
    # cls_embedding = last_hidden_states[:, 0, :]
    cls_embedding = last_hidden_states[0, 0, :]
    # print("CLS token embedding:", cls_embedding)
    return cls_embedding


def text_embedding_1024_remote(texts):
    if not isinstance(texts, list):
        texts = [texts]
    url = f'http://{settings.REMOTE_MODEL_BASE_PATH}/other/embed_texts'
    data = {
        "texts": texts
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        # 打印响应内容（假设响应是 JSON 格式）
        embeddings = response.json()['data']
        return embeddings, 200
    else:
        return "Wrong response code!", 400


def search_paper_with_query(text, limit=20):
    t, m = get_sci_bert()
    collection = init_milvus("SE2024")
    # text = translate_zh2en(text)  # 任意语言到英文翻译
    # print(text)
    # query_embedding = text_embedding(text, t, m).cpu().detach().numpy()

    # 目前张量形状对不上
    query_embeddings, code = text_embedding_1024_remote(text)  # query_embedding [N, 1024]
    search_results = milvus_search(collection, query_embeddings, limit)
    entities = [x.entity.to_dict() for x in search_results[0]]
    ids = [i['entity']['normal_id'] for i in entities]
    filtered_paper = Paper.objects.filter(paper_id__in=ids)
    # for paper in filtered_paper:
    #     print(paper.title)
    return filtered_paper


def get_all_paper():
    papers = Paper.objects.all()
    for paper in papers:
        keyword = paper.title + '.' + paper.abstract
        paper_id = paper.paper_id
        yield keyword, paper_id


def insert_paper_info_2_vector_database():
    t, m = get_sci_bert()
    collection = init_milvus("SE2024")
    infos = []
    for keyword, paper_id in tqdm(get_all_paper()):
        embedding = text_embedding(keyword, t, m).cpu().detach().numpy()
        infos.append({
            'vector': embedding.astype(np.float32),
            'normal_id': str(paper_id)
        })
        torch.cuda.empty_cache()
    milvus_insert(collection, infos)

# insert_paper_info_2_vector_database()
