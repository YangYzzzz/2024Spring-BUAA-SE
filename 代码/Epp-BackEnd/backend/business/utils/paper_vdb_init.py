import json
import os.path

import numpy as np
import faiss
import pickle

import requests
from django.conf import settings
from business.models import Paper
from business.utils import reply


def get_all_paper():
    papers = Paper.objects.all()
    for paper in papers:
        keyword = paper.title + '.' + paper.abstract
        paper_id = paper.paper_id
        yield keyword, paper_id


def embed(texts):
    if not isinstance(texts, list):
        texts = [texts]

    url = f'http://{settings.REMOTE_MODEL_BASE_PATH}/other/embed_texts'
    payload = json.dumps({
        "texts": texts
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['data']


def local_vdb_init(request):
    d = settings.VECTOR_DIM

    # db_vectors = np.random.random((nb, d)).astype('float32')
    texts = []
    metadata = []
    for keyword, paper_id in get_all_paper():
        texts.append(keyword)
        metadata.append(paper_id)

    embed_texts = embed(texts)

    db_vectors = np.array(embed_texts).astype(np.float32)

    # 创建索引
    index = faiss.IndexFlatL2(d)  # 使用 L2 距离
    print("Is index trained?", index.is_trained)  # 对于 IndexFlatL2，总是 True

    # 添加向量到索引
    index.add(db_vectors)

    # 打印结果
    # for i in range(nq):
    #     print(f"Query {i}:")
    #     for j in range(k):
    #         print(f"  Neighbor {j}: ID = {indices[i, j]}, Distance = {distances[i, j]}, Metadata = {metadata[indices[i, j]]}")

    # 保存索引和元数据
    print(os.path.join(settings.LOCAL_VECTOR_DATABASE_PATH, settings.LOCAL_FAISS_NAME))
    faiss.write_index(index, os.path.join(settings.LOCAL_VECTOR_DATABASE_PATH, settings.LOCAL_FAISS_NAME))
    with open(os.path.join(settings.LOCAL_VECTOR_DATABASE_PATH, settings.LOCAL_METADATA_NAME), "wb") as f:
        pickle.dump(metadata, f)

    return reply.success({"success": "成功"})


def get_filtered_paper(text, k, threshold=None):
    os.environ['KMP_DUPLICATE_LIB_OK'] = "TRUE"
    # 1. 加载索引和元数据(是否可在初始化中加载) 2. 进行查询
    index = faiss.read_index(os.path.join(settings.LOCAL_VECTOR_DATABASE_PATH, settings.LOCAL_FAISS_NAME))
    with open(os.path.join(settings.LOCAL_VECTOR_DATABASE_PATH, settings.LOCAL_METADATA_NAME), "rb") as f:
        metadata = pickle.load(f)
    embed_texts = embed(text)
    print(embed_texts)
    distances, indices = index.search(np.array(embed_texts).astype(np.float32), k)
    i2d_dict = {}
    for d, i in zip(distances[0], indices[0]):
        i2d_dict[metadata[i]] = d
    paper_ids = [metadata[i] for i in indices[0]]
    filtered_papers = Paper.objects.filter(paper_id__in=paper_ids)
    ht_threshold_papers = []
    for p in filtered_papers:
        sim = i2d_dict[p.paper_id]
        if threshold is not None and sim < threshold:
            continue
        # p_dict = p.to_dict()
        # p_dict['similarity'] = float(sim)
        ht_threshold_papers.append(p)
    return ht_threshold_papers


def easy_vector_query(request):
    os.environ['KMP_DUPLICATE_LIB_OK'] = "TRUE"
    # 1. 加载索引和元数据(是否可在初始化中加载) 2. 进行查询
    index = faiss.read_index(os.path.join(settings.LOCAL_VECTOR_DATABASE_PATH, settings.LOCAL_FAISS_NAME))
    with open(os.path.join(settings.LOCAL_VECTOR_DATABASE_PATH, settings.LOCAL_METADATA_NAME), "rb") as f:
        metadata = pickle.load(f)

    request_data = json.loads(request.body)
    texts = request_data["texts"]
    k = request_data["k"]
    if not k:
        k = 20
    if not isinstance(texts, list):
        texts = [texts]

    embed_texts = embed(texts)

    # 查找，返回相似论文
    # distances: [1, K], indices: [1, k]
    distances, indices = index.search(np.array(embed_texts).astype(np.float32), k)
    i2d_dict = {}
    for d, i in zip(distances[0], indices[0]):
        i2d_dict[metadata[i]] = d
    paper_ids = [metadata[i] for i in indices[0]]
    filtered_paper = Paper.objects.filter(paper_id__in=paper_ids)
    paper_dict = []
    for p in filtered_paper:
        p_dict = p.to_dict()
        p_dict['similarity'] = float(i2d_dict[p.paper_id])
        print(p_dict)
        paper_dict.append(p_dict)

    return reply.success({"papers": paper_dict})
