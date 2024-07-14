# import numpy as np
# import torch
# from tqdm import tqdm
#
# from business.utils.milvus import init_milvus, milvus_insert
# from business.utils.vector_embedding import get_sci_bert, get_all_paper, text_embedding
#
#
# # 文献向量嵌入
# def insert_vector_database(request):
#     t, m = get_sci_bert()
#     collection = init_milvus("SE2024")
#     infos = []
#     for keyword, paper_id in tqdm(get_all_paper()):
#         embedding = text_embedding(keyword, t, m).cpu().detach().numpy()
#         infos.append({
#             'vector': embedding.astype(np.float32),
#             'normal_id': str(paper_id)
#         })
#         torch.cuda.empty_cache()
#     milvus_insert(collection, infos)